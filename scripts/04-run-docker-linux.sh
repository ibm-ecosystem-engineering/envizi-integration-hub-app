#!/usr/bin/env bash

docker run -d -p 3001:3001 --name my-e-int-hub \
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


podman run -d -p 3000:3000 --name my-e-int-hub2-ui --env NEXT_PUBLIC_API_URL="http://9.30.230.165:3001"  gandigit/e-int-hub2-ui-linux:latest


echo "build completed ...."