#!/bin/bash
    
mkdir -p integration_test_logs

# Check if compose file exists
if [ ! -f docker-compose.yaml ]; then
  echo "Error: docker-compose.yaml not found!"
  exit 1
fi

# Container status
docker compose -f docker-compose.yaml ps -a > integration_test_logs/compose-ps.txt 2>&1

# Logs for each service
for service in $(docker compose -f docker-compose.yaml config --services); do
docker compose -f docker-compose.yaml logs --no-color "$service" \
> "integration_test_logs/${service}-logs.txt"
done 

# Inspect each container
for container_id in $(docker compose -f docker-compose.yaml ps -aq); do

service_name=$(docker inspect \
--format '{{index .Config.Labels "com.docker.compose.service"}}' \
"$container_id")

docker inspect "$container_id" | jq \
> "integration_test_logs/${service_name}-inspect.json"
done