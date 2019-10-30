#!/bin/sh

export PATH=/usr/local/nginx/sbin:$PATH
case "$1" in
start)
echo "Start Kiwi Server"
uwsgi --ini uwsgi.ini
nginx -c /home/ec2-user/00Git/django_blog/nginx/nginx.conf
;;
stop)
echo "Stop Kiwi Server"
nginx -s stop
killall -9 uwsgi
esac
