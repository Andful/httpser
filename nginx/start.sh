!/bin/sh
nginx -c /app/nginx.conf -g "daemon off;"&
TASK_PID=$!
nc certbot 10000
nginx -g "daemon off;"

sudo rm /var/www/certbot.running
