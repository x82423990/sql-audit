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
from django.db.models import Q
from pymysql import err
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    BasePermission
)


class InceptionMainView(PromptMxins, ActionMxins, BaseView):
    '''
        查询：根据登录者身份返回相关的SQL，支持日期/模糊搜索。操作：执行（execute）, 回滚（rollback）,放弃（reject操作）
    '''
    serializer_class = InceptionSerializer
    permission_classes = [IsAuthenticated, IsHandleAble]
    search_fields = ['status']

    def filter_date(self, queryset):
        date_range = self.request.GET.get('daterange')
        if date_range:
            return queryset.filter(createtime__range=date_range.split(','))
        return queryset

    def get_queryset(self):
        userobj = self.request.user
        print(userobj, userobj.role)
        # 如果是管理员显示全部工单
        if userobj.is_superuser:
            return self.filter_date(Inceptsql.objects.all())
        if userobj.role == self.dev_spm:
            return self.filter_date(Inceptsql.objects.filter(Q(status=0) | Q(up=True)))
        query_set = userobj.groups.first().inceptsql_set.all() if userobj.role == self.dev_mng else userobj.inceptsql_set.all()
        return self.filter_date(query_set)

    def perform_destroy(self, instance):
        print("-----------------------------执行了么------------------------------")
        try:
            instance.delete()
        except Exception as e:
            raise ParseError(e)

    def check_and_set_approve_status(self, instance, status_code):
        user = self.request.user
        try:
            stepobj = instance.workorder.step_set.get(user_id=user.id)
        except ObjectDoesNotExist:
            raise ParseError("你没有改工单的审批权限")
        # 求上级
        prestep = instance.workorder.step_set.filter(pk=stepobj.id - 1)[0] if instance.workorder.step_set.filter(
            pk=stepobj.id - 1) else None
        # 求下级
        nexsetp = instance.workorder.step_set.filter(pk=stepobj.id + 1)[0] if instance.workorder.step_set.filter(
            pk=stepobj.id + 1) else None
        if stepobj.status != 0:
            raise ParseError(self.approve_warning)

        if prestep and prestep.status != 1:
            raise ParseError("组长/经理还没有审批完成!")

        if status_code == 1:
            # 判断是否有上级
            if nexsetp:
                instance.up = True
            else:
                # 没有上级直接改变状态
                instance.workorder.status = 1
            # 改变自己步骤的状态
            stepobj.status = status_code
        # 拒绝工单
        elif status_code == 2:
            # 如果驳回， 也把上级的状态改为终止
            if nexsetp:
                nexsetp.status = -1
                nexsetp.save()
            stepobj.status = status_code
            instance.workorder.status = status_code

        instance.workorder.save()
        stepobj.save()
        instance.save()

    def filter_select_type(self, instance):
        type = instance.type
        if type == self.type_select_tag:
            raise ParseError(self.type_warning)

    def handle_approve(self, call_type, status, step_number):
        instance = self.get_object()
        if self.has_flow(instance):
            #  call_type 1 为审批, status 为审批状态, 1 为allow， 2 reject
            if call_type == 1:
                self.check_and_set_approve_status(instance, status)

            # step_instance = instance.workorder.step_set.order_by('id')[step_number]
            # step_instance.status = status
            # step_instance.save()
            # call_type 3 为放弃，
            # if call_type == 3:
            #     steps = instance.workorder.step_set.all()
            #     steps_behind = steps.filter(id__gt=step_instance.id)
            #     for step in steps_behind:
            #         step.status = -1
            #         step.save()

    @action(detail=True)
    def execute(self, request, *args, **kwargs):
        instance = self.get_object()
        # 判断工单是否为执行过
        if instance.status != -1:
            self.ret = {'status': -2, 'msg': self.executed}
            return Response(self.ret)
        affected_rows = 0
        #  工单的status 状态设置为0,0代表执行成功
        instance.status = 0
        # 如果为查询语句
        if instance.type == self.type_select_tag:
            sql_query = SqlQuery(instance.db)

            data = sql_query.main(instance.sql_content)
            if data is None:
                instance.status = 2
                instance.save()
                raise ParseError("执行失败！")
            affected_rows = len(data)
            instance.handle_result = json.dumps([list(row) for row in data], cls=DateEncoder)
        else:
            execute_time = 0
            opids = []
            success_sqls, exception_sqls, handle_result = self.check_execute_sql(instance.db.id,
                                                                                 instance.sql_content,
                                                                                 self.action_type_execute)
            print("success_sqls", success_sqls)
            for success_sql in success_sqls:
                instance.rollback_db = success_sql[8]
                affected_rows += success_sql[6]
                execute_time += float(success_sql[9])
                opids.append(success_sql[7].replace("'", ""))
            # 如果返回的列表有值，代表inception执行失败，并返回执行失败的错误
            if exception_sqls:
                # 如果执行设置， 将工单的状态status =2
                instance.status = 2
                instance.execute_errors = exception_sqls
                self.ret['status'] = -1
            instance.rollback_opid = opids
            instance.handle_result = handle_result
            self.ret['msg'] = exception_sqls
            self.ret['data']['execute_time'] = '%.3f' % execute_time
        instance.exe_affected_rows = affected_rows
        self.ret['data']['affected_rows'] = affected_rows
        # 邮件通知
        # self.mail(instance, self.action_type_execute)
        # self.replace_remark(instance)
        instance.save()
        print(instance.id)
        return Response(self.ret)

    # @detail_route()
    # def reject(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.status = 1
    #     self.replace_remark(instance)
    #     role_step = self.get_reject_step(instance)
    #     self.handle_approve(3, 3, role_step)
    #     return Response(self.ret)

    @action(detail=True)
    def approve(self, request, *args, **kwargs):
        self.handle_approve(1, 1, 1)
        return Response(self.ret)

    @action(detail=True)
    def disapprove(self, request, *args, **kwargs):
        self.handle_approve(1, 2, 1)
        return Response(self.ret)

    @action(detail=True)
    def rollback(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 0:
            raise ParseError(self.not_sucessed_order)
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
        # 检查数据库是否可达
        self.test_connect(instance.db.id)
        execute_results = Inception(back_sqls, dbobj.name).inception_handle(db_addr).get('result')
        instance.status = -3
        instance.roll_affected_rows = self.ret['data']['affected_rows'] = len(execute_results) - 1
        self.replace_remark(instance)
        return Response(self.ret)
