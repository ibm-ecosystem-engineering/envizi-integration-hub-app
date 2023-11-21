#!/bin/bash

echo "app Started ...."

export WRITE_INTERIM_FILES=TRUE
export LOGLEVEL=DEBUG
export ENVIZI_CONFIG_FILE="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/app/envizi-config.json"

python app/main.py

echo "app completed ...."