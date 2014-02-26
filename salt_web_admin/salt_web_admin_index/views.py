#coding=UTF-8
#import datetime
import os
#import re
#import md5
import json,commands
from django.contrib.auth.decorators import login_required  
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.db import connection

from salt_web_admin_index.api import salt_api,common
from salt_web_admin_index.models import *
#from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
  context = {}
  context.update(csrf(request))
  services = Service.objects.all()
  context['services'] = services
  return render_to_response('index.html', context)
##################################################################################################################################
##远程命令执行
##################################################################################################################################
def execute(request):
    context = {'jid_auto':''}
    tgt = request.POST.get('tgt',"")
    fun = request.POST.get('fun',"cmd.run")
    arg = request.POST.get('arg',"")
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器执行该操作"})
            #comm="sh /srv/salt/state/cmd/scripts/cmd-hexin.sh"
            #comm="{comm_str} {tgt_str} {fun_str} {arg_str}".format(comm_str=comm,tgt_str=tgt,fun_str=fun,arg_str=arg)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_auto=commstatus
        elif tgt=='waiwei':
            if arg == '':
                comm="sh /srv/salt/state/cmd/scripts/cmd-waiwei.sh"
                comm="{comm_str} {tgt_str} {fun_str}".format(comm_str=comm,tgt_str=tgt,fun_str=fun)
                commyesorno,commstatus=commands.getstatusoutput(comm)
                jid_auto=commstatus
            else:
                comm="sh /srv/salt/state/cmd/scripts/cmd-waiwei.sh"
                comm="{comm_str} {tgt_str} {fun_str} \"{arg_str}\"".format(comm_str=comm,tgt_str=tgt,fun_str=fun,arg_str=arg)
                commyesorno,commstatus=commands.getstatusoutput(comm)
                jid_auto=commstatus
        else:
            if arg == '':
                comm="sh /srv/salt/state/cmd/scripts/cmd-else.sh"
                comm="{comm_str} {tgt_str} {fun_str}".format(comm_str=comm,tgt_str=tgt,fun_str=fun)
                commyesorno,commstatus=commands.getstatusoutput(comm)
                jid_auto=commstatus
            else:
                comm="sh /srv/salt/state/cmd/scripts/cmd-else.sh"
                comm="{comm_str} {tgt_str} {fun_str} \"{arg_str}\"".format(comm_str=comm,tgt_str=tgt,fun_str=fun,arg_str=arg)
                commyesorno,commstatus=commands.getstatusoutput(comm)
                jid_auto=commstatus
        context['jid_auto'] = jid_auto
        return render_to_response('auto_execute.html', context)
##################################################################################################################################
##结果收集
##################################################################################################################################
def getjobinfo(request):
    context = {}
    jid_auto = request.GET.get('jid_auto','')
    jid_reboot = request.GET.get('jid_reboot','')
    jid_fileupdate = request.GET.get('jid_fileupdate','')
    if jid_auto:
        where = int(request.GET.get('where','12376894567235'))
        if where == 12376894567235:
            result = '/getjobinfo?jid_auto=%s&where=%s' % (jid_auto,0)
            return HttpResponse(result)
        else:
            cursor = connection.cursor()
            host_result = cursor.execute("select id,success,`return` from salt.salt_returns \
                where jid='%s' limit %s,10000;" % (jid_auto,where) )
            hosts_result = cursor.fetchall()
            where = len(hosts_result) + where
            result = []
            for host_result in hosts_result:
                if host_result[2]:
                    result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br><pre>%s</pre><br>' % (host_result[0],host_result[1],host_result[2]))
                else :
                    if host_result[1]:
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行成功，但该命令无返回结果</pre><br/>' % (host_result[0],host_result[1]))
                    else :
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行失败！请联系管理员QQ：920862715  mail：zutb@funshion.com</pre><br/>' % (host_result[0],host_result[1]))
            context = {
                  "where":where,
                  "result":result
                }
        return HttpResponse(json.dumps(context))
    if jid_reboot:
        where = int(request.GET.get('where','12376894567235'))
        if where == 12376894567235:
            result = '/getjobinfo?jid_reboot=%s&where=%s' % (jid_reboot,0)
            return HttpResponse(result)
        else:
            cursor = connection.cursor()
            host_result = cursor.execute("select id,success,`return` from salt.salt_returns \
                where jid='%s' limit %s,10000;" % (jid_reboot,where) )
            hosts_result = cursor.fetchall()
            where = len(hosts_result) + where
            result = []
            for host_result in hosts_result:
                if host_result[2]:
                    result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br><pre>%s</pre><br>' % (host_result[0],host_result[1],host_result[2]))
                else :
                    if host_result[1]:
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行成功，但该命令无返回结果</pre><br/>' % (host_result[0],host_result[1]))
                    else :
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行失败！请联系管理员QQ：920862715  mail：zutb@funshion.com</pre><br/>' % (host_result[0],host_result[1]))
            context = {
                  "where":where,
                  "result":result
                }
        return HttpResponse(json.dumps(context))
    if jid_fileupdate:
        where = int(request.GET.get('where','12376894567235'))
        if where == 12376894567235:
            result = '/getjobinfo?jid_fileupdate=%s&where=%s' % (jid_fileupdate,0)
            return HttpResponse(result)
        else:
            cursor = connection.cursor()
            host_result = cursor.execute("select id,success,`return` from salt.salt_returns \
                where jid='%s' limit %s,10000;" % (jid_fileupdate,where) )
            hosts_result = cursor.fetchall()
            where = len(hosts_result) + where
            result = []
            for host_result in hosts_result:
                if host_result[2]:
                    result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br><pre>%s</pre><br>' % (host_result[0],host_result[1],host_result[2]))
                else :
                    if host_result[1]:
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行成功，但该命令无返回结果</pre><br/>' % (host_result[0],host_result[1]))
                    else :
                        result.append(u'host:%s&nbsp;&nbsp;&nbsp;state:%s<br/><pre>执行失败！请联系管理员QQ：920862715  mail：zutb@funshion.com</pre><br/>' % (host_result[0],host_result[1]))
            context = {
                  "where":where,
                  "result":result
                }
        return HttpResponse(json.dumps(context))
#################################################################################################################################
##返回结果检查
##################################################################################################################################
def result_check(request):
    context = {}
    jid_auto = request.GET.get('jid_auto','')
    jid_reboot = request.GET.get('jid_reboot','')
    jid_fileupdate = request.GET.get('jid_fileupdate','')
    if jid_auto:
        comm="sh /srv/salt/state/result_check/scripts/result_check.sh"
        comm="{comm_str} {jid_str}".format(comm_str=comm,jid_str=jid_auto)
        commyesorno,commstatus=commands.getstatusoutput(comm)
        message=commstatus
        return HttpResponse(message)
    if jid_reboot:
        comm="sh /srv/salt/state/result_check/scripts/result_check.sh"
        comm="{comm_str} {jid_str}".format(comm_str=comm,jid_str=jid_reboot)
        commyesorno,commstatus=commands.getstatusoutput(comm)
        message=commstatus
        return HttpResponse(message)
    if jid_fileupdate:
        comm="sh /srv/salt/state/result_check/scripts/result_check.sh"
        comm="{comm_str} {jid_str}".format(comm_str=comm,jid_str=jid_fileupdate)
        commyesorno,commstatus=commands.getstatusoutput(comm)
        message=commstatus
        return HttpResponse(message)
##################################################################################################################################
##服务管理--重启HA
##################################################################################################################################
def rebootha(request):
    context = {'jid_reboot':''}
    tgt = request.POST.get("id-reboot","")
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt=='hexin':
            return  render_to_response('error.html',{'error_message':"核心目前无HA!"})
            #comm="sh /srv/salt/state/service/scripts/rebootha/rebootha-hexin.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_reboot=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/service/scripts/rebootha/rebootha-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        else:
            comm="sh /srv/salt/state/service/scripts/rebootha/rebootha-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        context['jid_reboot'] = jid_reboot
        return render_to_response('reboot_execute.html', context)
##################################################################################################################################
##服务管理--重启nginx
##################################################################################################################################
def rebootnginx(request):
    context = {'jid_reboot':''}
    tgt = request.POST.get("id-reboot","")
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt=='hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心nginx重启!"})
            #comm="sh /srv/salt/state/service/scripts/rebootnginx/rebootnginx-hexin.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_reboot=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/service/scripts/rebootnginx/rebootnginx-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        else:
            comm="sh /srv/salt/state/service/scripts/rebootnginx/rebootnginx-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        context['jid_reboot'] = jid_reboot
        return render_to_response('reboot_execute.html', context)
##################################################################################################################################
##服务管理--重载nginx
##################################################################################################################################
def reloadnginx(request):
    context = {'jid_reboot':''}
    tgt = request.POST.get('id-reboot','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt=='hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心nginx重载!"})
            #comm="sh /srv/salt/state/service/scripts/rebootnginx/rebootnginx-hexin.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_reboot=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/service/scripts/reloadnginx/reloadnginx-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        else:
            comm="sh /srv/salt/state/service/scripts/reloadnginx/reloadnginx-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        context['jid_reboot'] = jid_reboot
        return render_to_response('reboot_execute.html', context)
##################################################################################################################################
##服务管理--test.ping
##################################################################################################################################
def testping(request):
    context = {'jid_reboot':''}
    tgt = request.POST.get('id-reboot','')
    fun = 'test.ping'
    arg=''
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/cmd/scripts/cmd-hexin.sh"
            #comm="{comm_str} {tgt_str} {fun_str} {arg_str}".format(comm_str=comm,tgt_str=tgt,fun_str=fun,arg_str=arg)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_reboot=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/cmd/scripts/cmd-waiwei.sh"
            comm="{comm_str} {tgt_str} {fun_str} {arg_str}".format(comm_str=comm,tgt_str=tgt,fun_str=fun,arg_str=arg)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        else:
            comm="sh /srv/salt/state/cmd/scripts/cmd-else.sh"
            comm="{comm_str} {tgt_str} {fun_str} {arg_str}".format(comm_str=comm,tgt_str=tgt,fun_str=fun,arg_str=arg)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_reboot=commstatus
        context['jid_reboot'] = jid_reboot
        return render_to_response('reboot_execute.html', context)
##################################################################################################################################
##配置文件管理--HA配置文件下发
##################################################################################################################################
def hafileupdate(request):
    context = {'jid_fileupdate':''}
    tgt = request.POST.get('id-fileupdate','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/haproxy/scripts/hafileupdate.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_fileupdate=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/haproxy/scripts/hafileupdate-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
        else:
            comm="sh /srv/salt/state/haproxy/scripts/hafileupdate-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
    context['jid_fileupdate'] = jid_fileupdate
    return render_to_response('fileupdate_execute.html', context)
##################################################################################################################################
##配置文件管理--NGINX配置文件下发
##################################################################################################################################
def nginxfileupdate(request):
    context = {'jid_fileupdate':''}
    tgt = request.POST.get('id-fileupdate','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/nginx_cache/scripts/nginxfileupdate.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_fileupdate=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/nginx_cache/scripts/nginxfileupdate-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
        else:
            comm="sh /srv/salt/state/nginx_cache/scripts/nginxfileupdate-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
    context['jid_fileupdate'] = jid_fileupdate
    return render_to_response('fileupdate_execute.html', context)
##################################################################################################################################
##配置文件管理--替换HA配置文件
##################################################################################################################################
def replacehaconf(request):
    context = {'jid_fileupdate':''}
    tgt = request.POST.get('id-fileupdate','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/replace-haproxy-configure-file/scripts/replacehaconf.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_fileupdate=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/replace-haproxy-configure-file/scripts/replacehaconf-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
        else:
            comm="sh /srv/salt/state/replace-haproxy-configure-file/scripts/replacehaconf-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
    context['jid_fileupdate'] = jid_fileupdate
    return render_to_response('fileupdate_execute.html', context)
##################################################################################################################################
##配置文件管理--替换NGINX配置文件
##################################################################################################################################
def replacenginxconf(request):
    context = {'jid_fileupdate':''}
    tgt = request.POST.get('id-fileupdate','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/replace-nginx-configure-file/scripts/replacenginxconf.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_fileupdate=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/replace-nginx-configure-file/scripts/replacenginxconf-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
        else:
            comm="sh /srv/salt/state/replace-nginx-configure-file/scripts/replacenginxconf-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
    context['jid_fileupdate'] = jid_fileupdate
    return render_to_response('fileupdate_execute.html', context)
##################################################################################################################################
##配置文件管理--换回HA配置文件
##################################################################################################################################
def resethaconf(request):
    context = {'jid_fileupdate':''}
    tgt = request.POST.get('id-fileupdate','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/replace-haproxy-configure-file/scripts/replacehaconf.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_fileupdate=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/reset-haproxy-configure-file/scripts/resethaconf-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
        else:
            comm="sh /srv/salt/state/reset-haproxy-configure-file/scripts/resethaconf-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
    context['jid_fileupdate'] = jid_fileupdate
    return render_to_response('fileupdate_execute.html', context)
##################################################################################################################################
##配置文件管理--换回NGINX配置文件
##################################################################################################################################
def replacenginxconf(request):
    context = {'jid_fileupdate':''}
    tgt = request.POST.get('id-fileupdate','')
    if tgt == '':
        return  render_to_response('error.html',{'error_message':"执行对象不能为空，请选择执行对象"})
    else:
        if tgt == 'hexin':
            return  render_to_response('error.html',{'error_message':"目前不支持对核心服务器进行该操作!"})
            #comm="sh /srv/salt/state/replace-nginx-configure-file/scripts/replacenginxconf.sh"
            #comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            #commyesorno,commstatus=commands.getstatusoutput(comm)
            #jid_fileupdate=commstatus
        elif tgt=='waiwei':
            comm="sh /srv/salt/state/reset-nginx-configure-file/scripts/resetnginxconf-waiwei.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
        else:
            comm="sh /srv/salt/state/reset-nginx-configure-file/scripts/resetnginxconf-else.sh"
            comm="{comm_str} {tgt_str}".format(comm_str=comm,tgt_str=tgt)
            commyesorno,commstatus=commands.getstatusoutput(comm)
            jid_fileupdate=commstatus
    context['jid_fileupdate'] = jid_fileupdate
    return render_to_response('fileupdate_execute.html', context)
