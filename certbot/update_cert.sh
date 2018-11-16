#!/bin/sh
mkdir /var/www/httpServer
certbot certonly --non-interactive --agree-tos -m example@mail.com --webroot -w /var/www -d $1
