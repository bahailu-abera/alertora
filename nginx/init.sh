#!/bin/sh
set -e

# Install openssl if not present
if ! command -v openssl > /dev/null; then
  apk update && apk add --no-cache openssl
fi

for domain in $DOMAIN; do
  CERT_PATH="/etc/letsencrypt/live/$domain/fullchain.pem"
  KEY_PATH="/etc/letsencrypt/live/$domain/privkey.pem"

  if [ ! -f "$CERT_PATH" ] || [ ! -f "$KEY_PATH" ]; then
    echo "Generating dummy certificate for $domain..."
    mkdir -p "/etc/letsencrypt/live/$domain"
    openssl req -x509 -nodes -newkey rsa:2048 \
      -days 1 \
      -keyout "$KEY_PATH" \
      -out "$CERT_PATH" \
      -subj "/CN=$domain"
  fi
done

exec nginx -g 'daemon off;'

