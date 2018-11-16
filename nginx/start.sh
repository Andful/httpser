#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 2
netcat certbot 10000
nginx -g "daemon off;"
