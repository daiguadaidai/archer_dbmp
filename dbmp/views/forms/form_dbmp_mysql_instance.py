#-*- coding: utf-8 -*-

from django import forms

class EditForm(forms.Form):
    # mysql_instance_id = forms.IntegerField(required=True, min_value=0)
    os_id = forms.IntegerField(required=True, min_value=0)
    # mysql_instance_info_id = forms.IntegerField()
    host = forms.GenericIPAddressField(required=True)
    port = forms.IntegerField(required=True, min_value=1025, max_value=65535)
    username = forms.CharField(required=True, min_length=1, max_length=200)
    password = forms.CharField(required=True, min_length=5, max_length=200)
    remark = forms.CharField(max_length=200)
    my_cnf_path = forms.CharField(required=True, min_length=5, max_length=200)
    base_dir = forms.CharField(required=True, min_length=5, max_length=200)
    start_cmd = forms.CharField(required=True, min_length=5, max_length=200)
