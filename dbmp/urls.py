"""hh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from dbmp.views import v_dbmp_mysql_instance as dbmp_mysql_instance

urlpatterns = [
    url(r'^$', dbmp_mysql_instance.index, name='dbmp_mysql_instance_index'),
    url(r'^dbmp_mysql_instance/index/$', dbmp_mysql_instance.index, name='dbmp_mysql_instance_index'),
    url(r'^dbmp_mysql_instance/list/$', dbmp_mysql_instance.list, name='dbmp_mysql_instance_list'),
    url(r'^dbmp_mysql_instance/test/$', dbmp_mysql_instance.test, name='dbmp_mysql_instance_test'),
]
