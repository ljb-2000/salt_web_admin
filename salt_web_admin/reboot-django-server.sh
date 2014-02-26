#!/bin/bash
ServerPid=`ps -ef |grep manage|grep "$1"|grep usr|awk '{print $2}'`
kill -9 $ServerPid&&nohup python manage.py runserver $1 &
ps -ef|grep manage
