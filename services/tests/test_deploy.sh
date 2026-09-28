#!/bin/bash

retries=3
init_wait_time=10


url="$1"

if [ -z "$url" ]; then
    echo "APP_URL was not provided or it is empty."
    exit 1
fi

for ((retry=1; retry<=retries; retry++)); do
    sleep "$init_wait_time"

    status=$(curl -sL -o /dev/null -w "%{http_code}" "$url")

    if [ "$status" -eq 200 ]; then
        echo "Deployment success"
        exit 0
    fi

    if [ "$retry" -eq "$retries" ]; then
        echo "Something went wrong. A response of $status was received."
        exit 1
    fi

    init_wait_time=$((init_wait_time - 4))
done
