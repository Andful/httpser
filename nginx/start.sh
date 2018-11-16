#!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
echo $!
export TASK_PID=$!
echo $TASK_PID
sleep 1
ls -l /var/www/certbot.running
while [-f /var/www/certbot.running ]
do
  ls -l /var/www/certbot.running
  sleep 2
done
ls -l /var/www/certbot.running
echo "file should be removed"
kill $TASK_PID
nginx -g "daemon off;"
