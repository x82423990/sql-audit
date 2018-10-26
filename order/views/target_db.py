from ulits.newBase import BaseView
from ..serializers import *
from order.models import Dbconf


class DbViewSet(BaseView):
    # queryset = Dbconf.objects.all()
    serializer_class = DbSerializer
    # permission_classes = None

    # 判断是否有env传进来
    def get_queryset(self):
        env = self.request.GET.get('env')
        if env:
            queryset = Dbconf.objects.filter(env=env).order_by('-createtime')
        else:
            queryset = Dbconf.objects.all().order_by('-createtime')
        return queryset

