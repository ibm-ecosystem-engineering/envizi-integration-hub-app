#!/usr/bin/env bash

echo "build Started ...."

DOCKER_IMAGE=gandigit/e-int-hub2-ui-linux

cd ../web

podman run -d -p 3000:3000 --name my-e-int-hub2-ui $DOCKER_IMAGE:latest

echo "build completed ...."