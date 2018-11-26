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
    ddl_tag = 'create'
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
        # try:
        sql_review = Inception(sql_content, dbobj.name).inception_handle(db_addr)
        # except Exception as e:
        #     raise ParseError(e)
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

    @staticmethod
    def test_connect(db_id):
        try:
            dbobj = Dbconf.objects.get(id=db_id)
        except Exception as e:
            raise ParseError(e)
        try:
            ret = Inception().rows_effect(user=dbobj.user, pwd=str(dbobj.password), host=dbobj.host,
                                          port=int(dbobj.port), db=dbobj.name, test=True)

            return ret
        except Exception:
            raise ParseError("host -%s-, -%s-" % (dbobj.host, "链接错误"))

    def mail(self, sqlobj, mailto, mailtype, max_rows=None):
        if sqlobj.env == self.env_prd:
            user_obj = self.request.user
            if user_obj.role == 'developer_manager' and mailtype == self.action_type_check:
                mailto = [i.email for i in User.objects.filter(role='developer_supremo')]
            # username = user_obj.username
            username = sqlobj.commiter
            # mailto_users = list(set(mailto_users))
            # mailto_list = [u.email for u in User.objects.filter(username__in=mailto_users)]
            mailto_conv = [mailto]
            mail_list = []
            mail_list.extend(mailto_conv)
            print(mail_list, max_rows)
            send_mail.delay(mail_list, username, sqlobj.id, sqlobj.sql_backup, mailtype, sqlobj.sql_content,
                            sqlobj.db.name, max_rows)
