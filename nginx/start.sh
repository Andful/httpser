#!/bin/sh
nginx -c /app/nginx.conf
timeout 10s nginx -g daemon off
nginx -c /etc/nginx/nginx.conf
nginx -g daemon off
