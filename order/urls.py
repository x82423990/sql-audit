"""audit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from order.views.target_db import *
from .views.inceptioncheck import *
from .views.inceptionmainview import *

router = DefaultRouter()
# 如果没有viewset 没有指定queryset， 则需要指定base_name
router.register(r'db', DbViewSet, base_name=DbViewSet)
router.register(r'sql', InceptionCheckView)
router.register(r'inceptions', InceptionMainView, base_name='InceptionMainView')

# router.register(r'groups', GroupViewSet)
# router.register(r'users', NewInfo)
# router.register(r'groups', DepartmentInfo)
urlpatterns = [
    # path('login/', LoginAuth.as_view()),
    # url(r'users/(.*)', UserInfo.as_view()),
    url(r'^', include(router.urls)),
]
