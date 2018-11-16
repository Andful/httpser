#!/bin/sh
timeout 10s nginx -c /app/nginx.conf -g "daemon off"
nginx -g "daemon off";
