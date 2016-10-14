# -*- coding: utf-8 -*-

"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from machina.app import board
from demo_project import urls
# from demo_project.app import board

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Apps
    # url(r'^markdown/', include('django_markdown.urls')), in django 1.10 il modulo pattern è deprecato
    url(r'^forum/', include(board.urls)),
    url(r'^', include('demo_project.urls')),
]
