#!/usr/bin/env bash

echo "build Started ...."

DOCKER_IMAGE=gandigit/e-int-hub2

cd ../api

### Linux
podman push $DOCKER_IMAGE-linux:latest

# ### Mac
# podman push $DOCKER_IMAGE-mac:latest

echo "build completed ...."