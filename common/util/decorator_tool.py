#-*- coding: utf-8 -*-

import simplejson as json

class DecoratorTool(object):

    def __init__(self):
        pass

    @classmethod
    def get_request_alert_message(self, func):
        """获得请求的alter信息"""
        def warpper(request):
            request.session['alert_message_now'] = {}

            request.session['alert_message_now'] = {
                'default_code': request.session.get('default_code', 'warning'),
                'default_msg':  request.session.get('default_msg', []),
                'primary_code': request.session.get('primary_code', 'info'),
                'primary_msg': request.session.get('primary_msg', []),
                'warning_code': request.session.get('warning_code', 'warning'),
                'warning_msg':  request.session.get('warning_msg', []),
                'info_code': request.session.get('info_code', 'info'),
                'info_msg': request.session.get('info_msg', []),
                'danger_code': request.session.get('danger_code', 'danger'),
                'danger_msg': request.session.get('danger_msg', []),
                'success_code': request.session.get('success_code', 'success'),
                'success_msg': request.session.get('success_msg', []),
            }
            request.session['default_code'] = 'default'
            request.session['default_msg'] = []
            request.session['primary_code'] = 'primary'
            request.session['primary_msg'] = []
            request.session['warning_code'] = 'warning'
            request.session['warning_msg'] = []
            request.session['info_code'] = 'info'
            request.session['info_msg'] = []
            request.session['danger_code'] = 'danger'
            request.session['danger_msg'] = []
            request.session['success_code'] = 'success'
            request.session['success_msg'] = [] 

            # form danger信息
            if request.session.has_key('form_danger_message'):
                messages = request.session.get('form_danger_message', {})
                for label, msgs in messages.items():
                    for msg in msgs:
                        request.session['alert_message_now']['danger_msg'].append(msg)
                request.session.pop('form_danger_message')

            return func(request)

        return warpper
