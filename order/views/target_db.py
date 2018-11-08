from ulits.newBase import BaseView
from ..serializers import *
from order.models import Dbconf
from ulits.permissions import IsSuperUser
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    BasePermission
)
from rest_framework.decorators import action
from rest_framework.response import Response
from order.mixins import ActionMxins


class DbViewSet(ActionMxins, BaseView):
    # queryset = Dbconf.objects.all()
    serializer_class = DbSerializer
    # permission_classes = None
    permission_classes = [IsAuthenticated, IsSuperUser]

    # 判断是否有env传进来
    def get_queryset(self):
        env = self.request.GET.get('env')
        if env:
            queryset = Dbconf.objects.filter(env=env).order_by('-createtime')
        else:
            queryset = Dbconf.objects.all().order_by('-createtime')
        return queryset

    @action(detail=True, methods=["post"])
    def connect(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.id)
        self.test_connect(instance.id)
        return Response(self.ret)

