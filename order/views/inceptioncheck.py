# Create your views here.
# coding=utf8
import re
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from ulits.newBase import BaseView
from ulits.basemixins import PromptMxins
from workflow.serializers import WorkOrderSerializer, StepSerializer
from order.mixins import ActionMxins
from order.serializers import *
from order.models import *
from account.models import NewGroup
from rest_framework import status


class InceptionCheckView(PromptMxins, ActionMxins, BaseView):
    '''
        查询：根据登录者身份返回相关的SQL，支持日期/模糊搜索。操作：执行（execute）, 回滚（rollback）,放弃（reject操作）
    '''
    queryset = Inceptsql.objects.all()
    serializer_class = InceptionSerializer
    serializer_order = WorkOrderSerializer
    serializer_step = StepSerializer

    # inception的默认action
    action_type = '--enable-check'

    # 获取禁用关键字
    def check_forbidden_words(self, sql_content):
        forbidden_instance = ForbiddenWords.objects.first()
        if forbidden_instance:
            forbidden_word_list = [fword for fword in forbidden_instance.forbidden_words.split() if fword]
            forbidden_words = [fword for fword in forbidden_word_list if
                               re.search(re.compile(fword, re.I), sql_content)]
            if forbidden_words:
                raise ParseError({self.forbidden_words: forbidden_words})

    # 获取用户所属于的group
    def check_user_group(self, request):
        if request.data.get('env') == self.env_prd and not request.user.is_superuser:
            if not request.user.groups.exists():
                raise ParseError(self.not_exists_group)
            print(request.user.groups.first().id)
            return request.user.groups.first().id

    # 工单步骤
    def create_step(self, instance, work_id, users_id):
        # 检查是否需要开启审核
        print("检查是否需要开启审核")
        print(self.is_manual_review and instance.env == self.env_prd)
        if self.is_manual_review and instance.env == self.env_prd:
            # instance_id = instance.id
            print("users_id", users_id)
            for index, uid in enumerate(users_id):
                # status = 1 if index == 0 else 0
                status = 0
                # 保存step流程
                step_serializer = self.serializer_step(data={'work_order': work_id, 'user': uid, 'status': status})
                step_serializer.is_valid(raise_exception=True)
                step_serializer.save()

    # 判断是否需要审核
    def get_strategy_is_manual_review(self, env):
        strategy_instance = Strategy.objects.first()
        if not strategy_instance:
            return False
        return strategy_instance.is_manual_review if env == self.env_prd else False

    # 判断是否大于200行
    def get_step_user(self, instance, userlist, rows):

        # 获取SQL 语句的影响行数
        # rows = 201
        userlist = list(set(userlist))
        if len(userlist) == 1:
            try:
                developer_supremo = User.objects.filter(role="developer_supremo")[0]
            except IndexError:
                raise ParseError("当前实例中没有副总角色")
            instance.up = True
            instance.save()
            userlist.append(developer_supremo.id)
        if rows > 200:
            try:
                developer_supremo = User.objects.filter(role="developer_supremo")[0]
            except IndexError:
                raise ParseError("当前实例中没有副总角色")
            userlist.append(developer_supremo.id)
        print("userlist", userlist)
        return userlist

    # 重写create 方法
    def create(self, request, *args, **kwargs):
        # 处理 数据
        request_data = request.data

        db_id = request_data.get('db')
        sql_content = request_data.get('sql_content')
        user_group_id = self.check_user_group(request)
        try:
            leader_obj = NewGroup.objects.get(pk=user_group_id).leader
        except Exception as e:
            raise ParseError(self.not_group)
        approve_user_list = [request.user.id, leader_obj.id]
        # 去获取该次提交影响的行数
        rows = self.max_effect_rows(db_id, sql_content)
        # 获取提交的SQL 语句
        # 如果是select语句 返回request type,不执行check, 否则返回check 的结果，
        select = re.search(self.type_select_tag, sql_content, re.IGNORECASE)
        self.check_forbidden_words(sql_content)
        if bool(select):
            raise ParseError(self.forbidden_select)
            # handle_result = None
            # request_data['type'] = self.type_select_tag
        else:
            # inception 执行返回的结果
            handle_result = self.check_execute_sql(db_id, sql_content, self.action_type_check)[-1]

        # 初始化一个工单
        workorder_serializer = self.serializer_order(data={})
        workorder_serializer.is_valid()
        workorder_instance = workorder_serializer.save()

        # 封装数据
        request_data["exe_affected_rows"] = self.max_effect_rows(db_id, sql_content)
        request_data['group'] = user_group_id
        request_data['commiter'] = request.user.username
        try:
            request_data['treater'] = leader_obj.username
        except Exception as e:
            raise ParseError(self.not_group)
        request_data['users'] = approve_user_list
        request_data['is_manual_review'] = self.get_strategy_is_manual_review(request_data.get('env'))  # 流程
        request_data['handle_result'] = handle_result
        request_data['workorder'] = workorder_instance.id
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        # 保存model
        instance = serializer.save()
        # 判断是否需要副总审核
        work_step_list = self.get_step_user(instance, approve_user_list, rows)
        # 筛选审批流程人
        self.create_step(instance, request_data['workorder'], work_step_list[1:])
        self.mail(instance, self.action_type_check)
        # self.ret['data'] = {"id": instance.id}
        return Response(self.ret, status=status.HTTP_201_CREATED)
