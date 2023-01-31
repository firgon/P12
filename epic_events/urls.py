"""epic_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from CRM.views import ClientViewSet, ContractViewSet, EventViewSet
from epic_events.admin import admin_site

router = routers.SimpleRouter()
router.register('clients', ClientViewSet, basename='clients')
# router.register('my-clients', MyClientViewSet, basename='my-clients')
router.register('contracts', ContractViewSet, basename='contracts')
# router.register('my-contracts', MyContractViewSet, basename='my-contracts')
router.register('events', EventViewSet, basename='events')
# router.register('my-events', MyEventViewSet, basename='my-events')

urlpatterns = [
    path('admin-tech/', admin.site.urls),
    path('admin/', admin_site.urls),
    path('', include(router.urls)),
    path('login/',
         TokenObtainPairView.as_view(),
         name='login'),
]
