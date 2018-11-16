#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 30
kill $TASK_PID
nginx -g "daemon off;"
