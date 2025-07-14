#!/bin/bash
set -e

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

cd /home/epic-user/realtime-backend/alertora || {
  echo "Directory not found!"
  exit 1
}

# Determine environment and copy appropriate nginx config
if [[ "$ENV" == "staging" ]]; then
  echo "Detected staging environment. Using nginx.staging.conf"
  cp nginx/nginx.staging.conf nginx/nginx.conf
else
  echo "Detected production environment. Using nginx.production.conf"
  cp nginx/nginx.prod.conf nginx/nginx.conf
fi

echo "Logging into AWS ECR..."
sudo snap install aws-cli --classic || true
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 890742563855.dkr.ecr.eu-north-1.amazonaws.com

echo "Starting Docker Compose services..."
docker compose up -d

echo "Reloading Nginx if running..."
NGINX_CONTAINER_ID=$(docker compose ps -q nginx)
if [ -n "$NGINX_CONTAINER_ID" ]; then
  docker exec "$NGINX_CONTAINER_ID" nginx -s reload || true
fi
