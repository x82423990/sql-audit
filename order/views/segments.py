from ulits.newBase import BaseView
from ..serializers import *
from ulits.permissions import IsSuperUser
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    BasePermission
)
from order.mixins import ActionMxins


class SegmentsViewSet(ActionMxins, BaseView):
    serializer_class = SegmentsSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = BusinessSegments.objects.all()

