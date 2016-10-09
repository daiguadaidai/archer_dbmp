#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from dbmp.models.dbmp_inception_instance import DbmpInceptionInstance

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

def ajax_get_all(request):
    """ajax 获得所有的 Inception 实例"""

    if request.method == 'POST':
        try:
            # 查找所有的 Inception 实例
            dbmp_inception_instances = DbmpInceptionInstance.objects.values(
                                      'inception_instance_id',
                                      'alias').all()
            print dbmp_inception_instances
            respons_data = json.dumps(list(dbmp_inception_instances))
            return HttpResponse(respons_data, content_type='application/json')
        except Exception, e:
            logger.info(traceback.format_exc())
