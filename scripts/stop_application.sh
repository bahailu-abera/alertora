#!/bin/bash
set -e

cd /home/epic-user/realtime-backend/alertora || {
  echo "Directory not found!"
  exit 1
}

echo "Stopping and removing business logic containers..."

# List of business logic services to stop & remove
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

for service in "${SERVICES[@]}"; do
  echo "Stopping $service container..."
  docker stop "$service" 2>/dev/null || true

  echo "Removing $service container..."
  docker rm "$service" 2>/dev/null || true
done

echo "Done stopping and removing business logic containers."
