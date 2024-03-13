#!/usr/bin/env bash

echo "docker run Started ...."

docker run -d -p 3001:3001 --name my-e-int-hub \
    --env LOGLEVEL=DEBUG \
    -v "/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/app/envizi-config.json:/app/envizi-config.json" \
    gandigit/e-int-hub-1-mac:latest

echo "run completed ...."