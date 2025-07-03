#!/bin/sh
set -e

DOMAIN=${DOMAIN:-example.com}
EMAIL=${EMAIL:-admin@example.com}

CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"

echo "[INFO] Running Certbot for $DOMAIN..."

# Delete dummy certs if found
if [ -f "$CERT_PATH" ]; then
  echo "Removing dummy certs..."
  rm -rf /etc/letsencrypt/live/$DOMAIN
  rm -rf /etc/letsencrypt/archive/$DOMAIN
  rm -f /etc/letsencrypt/renewal/$DOMAIN.conf
fi

# Issue real cert
certbot certonly --webroot -w /var/www/certbot \
  --email "$EMAIL" --agree-tos --no-eff-email \
  -d "$DOMAIN" \
  --force-renewal

# Reload Nginx to apply certs
echo "[INFO] Reloading nginx..."
docker exec nginx nginx -s reload

echo "[INFO] Certificate for $DOMAIN has been applied!"
