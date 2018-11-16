#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 3
while [ -f /var/www/certbot.running ]
do
  echo "file still there"
  sleep 1
done
echo "file removed"
kill $TASK_PID
sleep 3
nginx -g "daemon off;"
