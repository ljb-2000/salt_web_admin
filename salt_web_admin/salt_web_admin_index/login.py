#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])  
        if user is not None:
            return render_to_response('index.html',{'username':user})
        else:
            return render_to_response('login.html', {'message':"密码错误请重新输入"})
    else:
        return render_to_response('login.html', RequestContext(request))

