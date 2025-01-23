#!/bin/bash

echo "app Started ...."

export WRITE_INTERIM_FILES=TRUE
export LOGLEVEL=DEBUG
export ENVIZI_CONFIG_FILE="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub-app/api/config/envizi-config.json"
export DATA_FOLDER="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub-app/api/data"
export DATA_STORE_FOLDER="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub-app/api/data-store"

export OUTPUT_FOLDER="/Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub-app/output"


cd /Users/gandhi/GandhiMain/700-Apps/envizi-integration-hub-app


python -m venv myvenv-hub
source myvenv-hub/bin/activate


python api/src/main.py

echo "app completed ...."