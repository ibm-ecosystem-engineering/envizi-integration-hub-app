#!/bin/bash

echo "app Started ...."

export WRITE_INTERIM_FILES=TRUE
export LOGLEVEL=DEBUG
export ENVIZI_CONFIG_FILE="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/config/envizi-config.json"
export DATA_FOLDER="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/app/data"
export OUTPUT_FOLDER="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub/output"

python app/main.py

echo "app completed ...."