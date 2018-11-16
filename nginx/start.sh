nginx -c /app/nginx.conf
timeout 10s $(cd /var/www/;)
nginx -c /etc/nginx/nginx.conf
nginx -g daemon off;
