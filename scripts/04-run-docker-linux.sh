#!/usr/bin/env bash

docker run -d -p 3001:3001 --name my-e-int-hub \
    --env LOGLEVEL=DEBUG \
    -v "/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/app/envizi-config.json:/app/envizi-config.json" \
    gandigit/e-int-hub-linux:latest
