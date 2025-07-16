#!/bin/bash
set -e


cd /home/epic-user/realtime-backend/alertora || {
  echo "Directory not found!"
  exit 1
}

if [ -f ".env" ]; then
  export ENV=$(grep '^ENV=' .env | cut -d '=' -f2- | tr -d '"')
fi


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

# List of business logic services to pull
SERVICES=(
  notification-service
  user-preference-service
  email-worker
  sms-worker
  push-android-worker
  push-ios-worker
  retry-worker
  celery-beat
)

echo "Pulling updated images via docker compose..."
for SERVICE in "${SERVICES[@]}"; do
  echo "Pulling image for: $SERVICE"
  docker compose pull "$SERVICE"
done

echo "Starting Docker Compose services..."
docker compose up -d

echo "Reloading Nginx if running..."
NGINX_CONTAINER_ID=$(docker compose ps -q nginx)
if [ -n "$NGINX_CONTAINER_ID" ]; then
  docker exec "$NGINX_CONTAINER_ID" nginx -s reload || true
fi
