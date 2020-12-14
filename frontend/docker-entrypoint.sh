#!/bin/sh -eu
./generate_config.sh >/usr/share/nginx/html/config.js
nginx -g "daemon off;"