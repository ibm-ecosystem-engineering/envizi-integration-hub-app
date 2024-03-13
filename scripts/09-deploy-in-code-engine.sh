#!/usr/bin/env bash

echo "deploy in code engine Started ...."

ibmcloud login --sso

ibmcloud ce project select --name RetailDemo

ibmcloud ce secret create --name watsonx-secrets --from-env-file .env
ibmcloud ce app create --name watsonx-demo --image docker.io/aaaa/watsonx:latest --env-from-secret watsonx-secrets


docker run --rm -it --name watxtry1  \
--privileged \
-v /tmp:/tmp \
-p 3001:3001 \
--env-file .env \
gandhicloudlab/watxtry1:latest

echo "deploy in code engine completed ...."


