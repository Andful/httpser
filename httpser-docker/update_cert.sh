#!/bin/sh
certbot certonly --non-interactive --agree-tos -m example@mail.com --webroot -w /var/www -d $1
exit 0
