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
from dbmp.views import v_dbmp_mysql_handler as dbmp_mysql_handler
from dbmp.views import v_dbmp_mysql_backup_instance as dbmp_mysql_backup_instance
from dbmp.views import v_dbmp_mysql_database as dbmp_mysql_database

urlpatterns = [
    # dbmp_mysql_instance
    url(r'^$', dbmp_mysql_instance.home, name='dbmp_mysql_instance_home'),
    url(r'^dbmp_mysql_instance/home/$', dbmp_mysql_instance.home, name='dbmp_mysql_instance_home'),
    url(r'^dbmp_mysql_instance/index/$', dbmp_mysql_instance.index, name='dbmp_mysql_instance_index'),
    url(r'^dbmp_mysql_instance/add/$', dbmp_mysql_instance.add, name='dbmp_mysql_instance_add'),
    url(r'^dbmp_mysql_instance/edit/$', dbmp_mysql_instance.edit, name='dbmp_mysql_instance_edit'),
    url(r'^dbmp_mysql_instance/view/$', dbmp_mysql_instance.view, name='dbmp_mysql_instance_view'),
    url(r'^dbmp_mysql_instance/delete/$', dbmp_mysql_instance.delete, name='dbmp_mysql_instance_delete'),
    url(r'^dbmp_mysql_instance/ajax_delete/$', dbmp_mysql_instance.ajax_delete, name='dbmp_mysql_instance_ajax_delete'),
    url(r'^dbmp_mysql_instance/iframe_os_list/$', dbmp_mysql_instance.iframe_os_list, name='dbmp_mysql_instance_iframe_os_list'),
    url(r'^dbmp_mysql_instance/start_instance_terminal/$', dbmp_mysql_instance.start_instance_terminal, name='dbmp_mysql_instance_start_instance_terminal'),
    url(r'^dbmp_mysql_instance/stop_instance_terminal/$', dbmp_mysql_instance.stop_instance_terminal, name='dbmp_mysql_instance_stop_instance_terminal'),
    url(r'^dbmp_mysql_instance/restart_instance_terminal/$', dbmp_mysql_instance.restart_instance_terminal, name='dbmp_mysql_instance_restart_instance_terminal'),
    url(r'^dbmp_mysql_instance/terminal_sql_console/$', dbmp_mysql_instance.terminal_sql_console, name='dbmp_mysql_instance_terminal_sql_console'),

    # dbmp_mysql_handler
    url(r'^dbmp_mysql_handler/ajax_mysql_is_alived/$', dbmp_mysql_handler.ajax_mysql_is_alived, name='dbmp_mysql_handler_ajax_mysql_is_alived'),
    url(r'^dbmp_mysql_handler/ajax_start_instance$', dbmp_mysql_handler.ajax_start_instance, name='dbmp_mysql_handler_ajax_start_instance'),
    url(r'^dbmp_mysql_handler/ajax_stop_instance$', dbmp_mysql_handler.ajax_stop_instance, name='dbmp_mysql_handler_ajax_stop_instance'),
    url(r'^dbmp_mysql_handler/ajax_mysql_instance_status$', dbmp_mysql_handler.ajax_mysql_instance_status, name='dbmp_mysql_handler_ajax_mysql_instance_status'),
    url(r'^dbmp_mysql_handler/ajax_execute_sql$', dbmp_mysql_handler.ajax_execute_sql, name='dbmp_mysql_handler_ajax_execute_sql'),

    # dbmp_mysql_backup_instance
    url(r'^dbmp_mysql_backup_instance/index/$', dbmp_mysql_backup_instance.index, name='dbmp_mysql_backup_instance_index'),
    url(r'^dbmp_mysql_backup_instance/add/$', dbmp_mysql_backup_instance.add, name='dbmp_mysql_backup_instance_add'),
    url(r'^dbmp_mysql_backup_instance/edit/$', dbmp_mysql_backup_instance.edit, name='dbmp_mysql_backup_instance_edit'),
    url(r'^dbmp_mysql_backup_instance/view/$', dbmp_mysql_backup_instance.view, name='dbmp_mysql_backup_instance_view'),
    url(r'^dbmp_mysql_backup_instance/ajax_delete/$', dbmp_mysql_backup_instance.ajax_delete, name='dbmp_mysql_backup_instance_ajax_delete'),

    # dbmp_mysql_database
    url(r'^dbmp_mysql_database/ajax_sync_database/$', dbmp_mysql_database.ajax_sync_database, name='dbmp_mysql_database_ajax_sync_database'),
    url(r'^dbmp_mysql_database/ajax_search_database/$', dbmp_mysql_database.ajax_search_database, name='dbmp_mysql_database_ajax_search_database'),
]
