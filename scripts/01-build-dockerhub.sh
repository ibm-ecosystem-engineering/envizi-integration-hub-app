#!/usr/bin/env bash

echo "build Started ...."

DOCKER_IMAGE=gandigit/e-int-hub

cd ..

### Linux
docker build --platform linux/amd64 -f Dockerfile -t $DOCKER_IMAGE-linux:latest .
docker push $DOCKER_IMAGE-linux:latest

### Mac
docker build -f Dockerfile -t$DOCKER_IMAGE-mac:latest .
docker push $DOCKER_IMAGE-mac:latest

echo "build completed ...."