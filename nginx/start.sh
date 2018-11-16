#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
sleep 1
while [-f /var/www/certbot.running ]
do
  sleep 2
done
ls -l /var/www/certbot.running
echo "file should be removed"
kill TASK_PID
nginx -g "daemon off;"
