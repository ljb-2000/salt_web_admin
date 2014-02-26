#coding=UTF-8
#import datetime
import os
#import re
#import md5
import json,commands



from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.db import connection

from salt_web_admin_index.api import salt_api,common
from salt_web_admin_index.models import *
#from django.views.decorators.csrf import csrf_exempt

##################################################################################################################################
##清缓存部分
##################################################################################################################################
def nginx_cache_url_withargs(req):
    if len(req.POST.get('nginx_cache_url_withargs')) == 0:
        return render_to_response('nginx_cache.html',{'title':"清除服务器缓存",'nginx_cache_count_withargs':"输入不能为空!请重新输入"})
    else:
        nginx_cache_url = req.POST.get('nginx_cache_url_withargs')
        nginx_cache_url = nginx_cache_url.split()
        result = []
        url='\\\\\\\"'
        fun = 'cmd.run'
        arg = "salt '*-CACHE-*' cmd.run "
        cmm = "python /usr/local/nginx/purge/purge_withargs.py "
        for textarea_url in nginx_cache_url:
            url=url+textarea_url+';'
        url=url[:-1]+'\\\\\\\"'
        sa='salt --timeout=1200 -N hexin cmd.run "python /usr/local/nginx/purge/purge_withargs.py '+url+"\""
        os.system(sa)
        te='salt --timeout=1200 -N \'waiwei\' cmd.run "salt --timeout=1200 \'*-CACHE-*\' cmd.run \\\"python /usr/local/nginx/purge/purge_withargs.py '+url+"\\\"\""
        te=te+" &"
        os.system(te)
        return render_to_response('nginx_cache_url.html',{'title':"运维清缓存－－－执行命令",'nginx_cache_count_withargs':"清空成功"})
