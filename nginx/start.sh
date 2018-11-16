#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 1
while [-f /var/www/certbot.running ]
do
  echo "file still there"
  sleep 2
done
echo "file removed"
kill $TASK_PID
nginx -g "daemon off;"
