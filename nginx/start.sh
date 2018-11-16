#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
netcat certbot 10000
nginx -g "daemon off;"
