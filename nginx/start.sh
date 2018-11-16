#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 2
echo "connection started"
yes | netcat certbot 10000
echo "connection ended"
nginx -g "daemon off;"
