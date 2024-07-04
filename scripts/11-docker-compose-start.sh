#!/usr/bin/env bash

echo "build Started ...."

podman-compose up -d


podman-compose stop envizi-integration-hub_api_1
podman-compose stop envizi-integration-hub_client_1
podman-compose stop envizi-integration-hub_nginx_1



podman compose build flaskapp

podman compose up -d flaskapp

docker ps -a 

echo "build completed ...."