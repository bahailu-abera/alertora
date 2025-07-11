#!/bin/bash
set -e

cd /home/epic-user/realtime-backend/alertora || {
  echo "Directory not found!"
  exit 1
}

echo "Stopping running containers..."
docker compose down || true
