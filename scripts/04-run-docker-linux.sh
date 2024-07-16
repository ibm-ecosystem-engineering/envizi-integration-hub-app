#!/usr/bin/env bash

docker run -d -p 3001:3001 --name my-e-int2-hub \
    --env LOGLEVEL=DEBUG \
     --env DATA_FOLDER=/app/data \
     --env DATA_STORE_FOLDER=/app/data \
     --env OUTPUT_FOLDER=/app/output \
    -v "/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/app/envizi-config.json:/app/envizi-config.json" \
    gandigit/e-int-hub-linux:latest


podman run -d -p 3001:3001 --name my-e-int2-hub \
    --env LOGLEVEL=DEBUG \
    --env DATA_FOLDER="/app/data" \
    --env DATA_STORE_FOLDER="/app/data" \
    --env OUTPUT_FOLDER="/app/output" \
    -v "/root/int-hub/envizi-config.json:/app/envizi-config.json" \
    gandigit/e-int-hub2-linux:latest


echo "build completed ...."