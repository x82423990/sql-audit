from django.shortcuts import render
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    BasePermission
)
# from core.models import globalpermissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.http import HttpResponse
from ulits.baseview import BaseView
from ulits.sendmail import send_email
from account.models import User, NewGroup
from django.contrib.auth.models import Group, Permission
from .serializers import UserSerializer, DepartmentSerializer, PermissionsSerializer, PersonalCenterSerializer
import json
from ulits.newBase import BaseView as NewBaseView
from django.contrib.auth.models import Group
from ulits.basemixins import PromptMxins
from rest_framework.exceptions import ParseError
from rest_framework_jwt.views import JSONWebTokenAPIView
from datetime import datetime
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class NewInfo(NewBaseView):
    '''
    用户中心
    '''
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    # permission_classes = [IsSuperUser]
    search_fields = ['username']

    #  这个传入的serializer 是 GenericViewSet 定义的get_serializer 方法返回的值，默认返回上面定义的serializer_class，
    def perform_update(self, serializer):
        serializer.update(self.get_object(), self.request.data)

    #  在 create 之前先执行 UserSerializer 系列里面的crate方法，我们重写serializer 的create方法
    def perform_create(self, serializer):
        serializer.create(self.request.data)


class DepartmentInfo(NewBaseView):
    '''
    部门组
    '''
    queryset = NewGroup.objects.all().order_by('-id')
    serializer_class = DepartmentSerializer
    search_fields = ['name']


class PermissionsViewSet(NewBaseView):
    '''
    权限
    '''
    queryset = Permission.objects.all()
    # search_fields = [""]
    serializer_class = PermissionsSerializer


class PersonalCenterViewSet(PromptMxins, NewBaseView):
    '''
        个人中心
    '''
    serializer_class = PersonalCenterSerializer
    permission_classes = [IsAuthenticated]

    def check_password(self, params):
        # user = authenticate(username=self.request.user.username, password=params.get('old_pass'))
        # if not user:
        #     raise ParseError(self.old_password_warning)
        new_pass = params.get('new_pass')
        rep_pass = params.get('rep_pass')
        if not (new_pass and rep_pass and new_pass == rep_pass):
            raise ParseError(self.new_rep_password_warning)
        return new_pass

    def list(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        new_pass = self.check_password(request_data)
        instance = request.user
        # instance.email = request_data.get("email")
        instance.set_password(new_pass)
        instance.save()
        return Response(self.ret)



