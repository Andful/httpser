#!/bin/sh
openssl x509 -enddate -noout -in $1
exit 0
