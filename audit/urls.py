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
from django.contrib import admin
from django.urls import path, include

# swagger package
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_jwt.views import obtain_jwt_token
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('api/docs/', schema_view),  # swagger doc
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # wagger login
    path('api/api-token-auth/', obtain_jwt_token),
    # path('api/api-token-auth/', ApiAuth),
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/order/', include('order.urls')),
    path('api/chart', include('dashboard.urls'))
]
# urlpatterns = format_suffix_patterns(urlpatterns)
