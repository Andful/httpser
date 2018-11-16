#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 2
echo "connection started"
while ! nc -z rabbitmq 10000; do sleep 3; done
echo "connection ended"
sleep 3
nginx -g "daemon off;"
