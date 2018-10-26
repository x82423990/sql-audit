# coding=utf8
import json
from rest_framework.response import Response
from rest_framework.decorators import detail_route, action
from rest_framework.exceptions import ParseError
from ulits.newBase import BaseView
from ulits.basemixins import PromptMxins
from ulits.sqltools import Inception, SqlQuery
from ulits.encode import DateEncoder
from order.mixins import ActionMxins
from order.permission import IsHandleAble
from order.serializers import *
from order.models import *


class InceptionMainView(PromptMxins, ActionMxins, BaseView):
    '''
        查询：根据登录者身份返回相关的SQL，支持日期/模糊搜索。操作：执行（execute）, 回滚（rollback）,放弃（reject操作）
    '''
    serializer_class = InceptionSerializer
    permission_classes = [IsHandleAble]
    search_fields = ['commiter', 'sql_content', 'env', 'treater', 'remark']

    def filter_date(self, queryset):
        date_range = self.request.GET.get('daterange')
        if date_range:
            return queryset.filter(createtime__range=date_range.split(','))
        return queryset

    def get_queryset(self):
        userobj = self.request.user
        print(userobj)
        if userobj.is_superuser or userobj.role == self.dev_spm:
            return self.filter_date(Inceptsql.objects.all())
        query_set = userobj.groups.first().inceptsql_set.all() if userobj.role == self.dev_spm else userobj.inceptsql_set.all()
        return self.filter_date(query_set)

    def check_approve_status(self, instance):
        step_instance = instance.workorder.step_set.all()[1]
        if step_instance.status != 0:
            raise ParseError(self.approve_warning)

    def filter_select_type(self, instance):
        type = instance.type
        if type == self.type_select_tag:
            raise ParseError(self.type_warning)

    def handle_approve(self, call_type, status, step_number):
        instance = self.get_object()
        if self.has_flow(instance):
            if call_type == 1:
                self.check_approve_status(instance)
                if status == 1:
                    instance.workorder.status = True
                    instance.workorder.save()
            step_instance = instance.workorder.step_set.order_by('id')[step_number]
            step_instance.status = status
            step_instance.save()
            if call_type == 3:
                steps = instance.workorder.step_set.all()
                steps_behind = steps.filter(id__gt=step_instance.id)
                for step in steps_behind:
                    step.status = -1
                    step.save()

    @action(detail=True)
    def execute(self, request, *args, **kwargs):
        print("我来了")
        instance = self.get_object()
        if instance.status != -1:
            self.ret = {'status': -2, 'msg': self.executed}
            return Response(self.ret)
        affected_rows = 0
        print("affected_rows", affected_rows)
        instance.status = 0
        if instance.type == self.type_select_tag:
            sql_query = SqlQuery(instance.db)
            data = sql_query.main(instance.sql_content)
            affected_rows = len(data)
            instance.handle_result = json.dumps([list(row) for row in data], cls=DateEncoder)
        else:
            execute_time = 0
            opids = []
            success_sqls, exception_sqls, handle_result = self.check_execute_sql(instance.db.id, instance.sql_content)
            for success_sql in success_sqls:
                instance.rollback_db = success_sql[8]
                affected_rows += success_sql[6]
                execute_time += float(success_sql[9])
                opids.append(success_sql[7].replace("'", ""))
            if exception_sqls:
                instance.status = 2
                instance.execute_errors = exception_sqls
                self.ret['status'] = -1
            instance.rollback_opid = opids
            instance.handle_result = handle_result
            self.ret['msg'] = exception_sqls
            self.ret['data']['execute_time'] = '%.3f' % execute_time
        instance.exe_affected_rows = affected_rows
        self.ret['data']['affected_rows'] = affected_rows
        self.mail(instance, self.action_type_execute)
        self.replace_remark(instance)
        self.handle_approve(2, 1, 2)
        return Response(self.ret)

    @detail_route()
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 1
        self.replace_remark(instance)
        role_step = self.get_reject_step(instance)
        self.handle_approve(3, 3, role_step)
        return Response(self.ret)

    @detail_route()
    def approve(self, request, *args, **kwargs):
        self.handle_approve(1, 1, 1)
        return Response(self.ret)

    @detail_route()
    def disapprove(self, request, *args, **kwargs):
        self.handle_approve(1, 2, 1)
        return Response(self.ret)

    @action(detail=True)
    def rollback(self, request, *args, **kwargs):
        instance = self.get_object()
        self.filter_select_type(instance)
        dbobj = instance.db
        rollback_opid_list = instance.rollback_opid
        rollback_db = instance.rollback_db
        back_sqls = ''
        for opid in eval(rollback_opid_list)[1:]:
            back_source = 'select tablename from $_$Inception_backup_information$_$ where opid_time = "{}" '.format(
                opid)
            back_table = Inception(back_source, rollback_db).get_back_table()
            back_content = 'select rollback_statement from {} where opid_time = "{}" '.format(back_table, opid)
            back_sqls += Inception(back_content, rollback_db).get_back_sql()
        db_addr = self.get_db_addr(dbobj.user, dbobj.password, dbobj.host, dbobj.port, self.action_type_execute)
        execute_results = Inception(back_sqls, dbobj.name).inception_handle(db_addr).get('result')
        instance.status = -3
        instance.roll_affected_rows = self.ret['data']['affected_rows'] = len(execute_results) - 1
        self.replace_remark(instance)
        return Response(self.ret)
