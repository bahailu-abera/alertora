#!/bin/sh
set -e

# Set domain and email from environment variables or use defaults
DOMAINS=${DOMAIN:-yourdomain.com}
EMAIL=${EMAIL:-your@email.com}

for domain in $DOMAINS; do
	CERT_PATH="/etc/letsencrypt/live/$domain/fullchain.pem"
	echo "Starting Certbot initialization for domain: $domain"

	# Check if certificate exists
	if [ -f "$CERT_PATH" ]; then
	  echo "Certificate exists, checking if it's a dummy...: $domain"
	  # Check if certificate is self-signed dummy cert by looking for CN in issuer
	  if openssl x509 -in "$CERT_PATH" -noout -issuer | grep -q "CN=$domain"; then
		echo "Found dummy certificate, removing old certificate files... : $domain"
		rm -rf "/etc/letsencrypt/live/$domain"
		rm -rf "/etc/letsencrypt/archive/$domain"
		rm -f "/etc/letsencrypt/renewal/$domain.conf"
		echo "No existing certificate found: $domain."
		# Obtain or renew real certificate
		echo "Attempting to obtain/renew real certificates with Certbot... : $domain"
		certbot certonly --webroot -w /var/www/certbot \
		--email "$EMAIL" --agree-tos --no-eff-email \
		-d "$domain" \
		--force-renewal
		echo "Certificate process completed! : $domain"
	  else
		echo "Found legitimate certificate, no action needed : $domain"
	  fi
	else
	  echo "No existing certificate found: $domain."
	  # Obtain or renew real certificate
	  echo "Attempting to obtain/renew real certificates with Certbot... : $domain"
	  certbot certonly --webroot -w /var/www/certbot \
	  --email "$EMAIL" --agree-tos --no-eff-email \
	  -d "$domain" \
	  --force-renewal
	  echo "Certificate process completed! : $domain"
	fi
done
echo "Please reload Nginx to apply new certificates:"
echo "docker-compose exec nginx nginx -s reload"

# Keep the container running (for demo or to prevent container exit)
echo "Sleeping to keep container alive..."
sleep 3600

