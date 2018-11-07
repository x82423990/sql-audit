# coding=utf8
from rest_framework.exceptions import ParseError
from ulits.tasks import send_mail
from ulits.basemixins import AppellationMixins
from ulits.dbcrypt import prpcrypt
from ulits.sqltools import Inception
from .models import *
import re
import json


class ActionMxins(AppellationMixins, object):
    type_select_tag = 'select'
    action_type_execute = '--enable-execute'
    action_type_check = '--enable-check'

    def get_reject_step(self, instance):
        user = self.request.user
        if self.has_flow(instance):
            if user.is_superuser:
                return 1 if instance.commiter == user.username else 2
            else:
                role = user.role
                return self.reject_steps.get(role)

    @staticmethod
    def get_current_step(instance):
        steps = instance.workorder.step_set.all()
        current = 0
        for step in steps:
            if step.status not in [-1, 0]:
                current += 1
        return current

    # 是否需要开启审核
    @property
    def is_manual_review(self):
        instance = Strategy.objects.first()
        if not instance:
            instance = Strategy.objects.create()
        return instance.is_manual_review

    def get_db_addr(self, user, password, host, port, actiontype=""):
        pc = prpcrypt()
        password = pc.decrypt(password)
        dbaddr = '--user={}; --password={}; --host={}; --port={}; {};'.format(user, password, host, port, actiontype)
        return dbaddr

    def has_flow(self, instance):
        return instance.is_manual_review == True and instance.env == self.env_prd

    def replace_remark(self, sqlobj):
        username = self.request.user.username
        uri = self.request.META['PATH_INFO'].split('/')[-2]
        if username != sqlobj.treater:
            sqlobj.remark += '   [' + username + self.action_desc_map.get(uri) + ']'
        if sqlobj.workorder.status:
            steps = sqlobj.workorder.step_set.all()
            step_obj_second = steps[0]
            if not (self.request.user == step_obj_second.user and uri == 'reject'):
                step_obj = steps[0]
                step_obj.user = self.request.user
                step_obj.save()
        sqlobj.save()

    def check_execute_sql(self, db_id, sql_content, action_type):
        dbobj = Dbconf.objects.get(id=db_id)
        db_addr = self.get_db_addr(dbobj.user, dbobj.password, dbobj.host, dbobj.port, action_type)
        sql_review = Inception(sql_content, dbobj.name).inception_handle(db_addr)
        result, status = sql_review.get('result'), sql_review.get('status')
        if status == -1 or len(result) == 1:
            raise ParseError({self.connect_error: result})
        success_sqls = []
        exception_sqls = []
        for sql_result in result:
            error_message = sql_result[4]
            if error_message == 'None' or re.findall('Warning', error_message):
                success_sqls.append(sql_result)
            else:
                exception_sqls.append(error_message)
        if exception_sqls and self.action_type == '--enable-check':
            raise ParseError({self.exception_sqls: exception_sqls})
        return success_sqls, exception_sqls, json.dumps(result)

    @staticmethod
    def max_effect_rows(db_id, sql_content):
        dbobj = Dbconf.objects.get(id=db_id)
        rows = Inception(sql_content, dbobj.name).rows_effect(user=dbobj.user, pwd=dbobj.password, host=dbobj.host,
                                                              port=int(dbobj.port), db=dbobj.name)
        return rows

    def mail(self, sqlobj, mailtype):
        if sqlobj.env == self.env_prd:
            print("--他和在执行")
            username = self.request.user.username
            treater = sqlobj.treater if username != sqlobj.treater else User.objects.filter(role="developer_supremo")[0]
            commiter = sqlobj.commiter
            db_name = sqlobj.db.name
            print(db_name)
            mailto_users = [treater, commiter]
            mailto_users = list(set(mailto_users))
            mailto_list = [u.email for u in User.objects.filter(username__in=mailto_users)]
            print(mailto_list, username, sqlobj.id, sqlobj.sql_backup, mailtype, sqlobj.sql_content)
            send_mail.delay(mailto_list, username, sqlobj.id, sqlobj.sql_backup, mailtype, sqlobj.sql_content,
                            sqlobj.db.name)
