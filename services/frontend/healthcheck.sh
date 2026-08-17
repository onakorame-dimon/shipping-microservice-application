#!/bin/sh

status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)

if [ "$status" -eq 200 ]; then
    echo "Healthy"
else
    echo "Unhealthy: Failed with HTTP $status"
    exit 1
fi