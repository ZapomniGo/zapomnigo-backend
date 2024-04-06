#!/bin/bash

if [ "$DOCK_ENV" = "LOCAL" ]; then
  curl -k -f https://localhost:8000/api/v1/health

elif [ "$DOCK_ENV" = "DEV" ]; then
  curl -f https://dev.zapomnigo.com:8000/api/v1/health

elif [ "$DOCK_ENV" = "PROD" ]; then
  curl -f https://zapomnigo.com:8000/api/v1/health

else
  echo "Unknown DOCK_ENV: $DOCK_ENV"
  exit 1
fi