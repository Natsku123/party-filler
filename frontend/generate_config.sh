#!/bin/sh -eu
if [ -z "${API_HOSTNAME:-}" ]; then
    API_HOSTNAME_JSON=http://localhost:8800
else
    API_HOSTNAME_JSON=$(jq -n --arg api_url '$API_HOSTNAME' '$api_hostname')
fi

cat <<EOF
window.REACT_APP_API_HOSTNAME=$API_HOSTNAME_JSON;
EOF
