#!/bin/sh -eu
if [ -z "${API_HOSTNAME:-}" ]; then
    API_HOSTNAME_JSON=http://localhost:8800
else
    API_HOSTNAME_JSON=$(jq -n --arg api_hostname '$API_HOSTNAME' '$api_hostname')

fi

if [ -z "${REDIRECT_URL:-}" ]; then
    API_REDIRECT_URL_JSON=""
else
    API_REDIRECT_URL_JSON=$(jq -n --arg redirect_url '$REDIRECT_URL' '$redirect_url')
fi

cat <<EOF
window.REACT_APP_API_HOSTNAME=$API_HOSTNAME_JSON;
window.REACT_APP_API_REDIRECT_URL=$API_REDIRECT_URL_JSON;
EOF
