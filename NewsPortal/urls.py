"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from allauth.account.views import LogoutView
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from main.views import PersonalView

import logging

logger = logging.getLogger('django.request')

logger.debug('DEBUG level message')
logger.info('INFO level message')
logger.warning('WARNING level message')
logger.error('ERROR level message')
logger.critical('CRITICAL level message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('celery_results/', include('django_celery_results.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', PersonalView.as_view()),
    path('logout/',
         LogoutView.as_view(template_name='personal/logout.html'),
         name='logout'),
]
