#!/usr/bin/env bash

echo "build Started ...."

DOCKER_IMAGE=gandigit/e-int-hub2-ui

cd ../web

### Linux
podman build --platform linux/amd64 -f Dockerfile -t $DOCKER_IMAGE-linux:latest .
# podman push $DOCKER_IMAGE-linux:latest

# ### Mac
# podman build -f Dockerfile -t$DOCKER_IMAGE-mac:latest .
# podman push $DOCKER_IMAGE-mac:latest

echo "build completed ...."