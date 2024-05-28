# Envizi Integration Hub - Starting the App using Python src code

This document explains about how to start Envizi Integration Hub using Python src code.

The Integration Hub App should be started with the configuration file.

## 1. Start the Python API App

1. Download this repo.

2. Prepare Configuration file by using the link [02-prepare-configuration-filed](../02-prepare-configuration-file)

3. Keep the property file `envizi-config.json` in some folder. Lets us assume the file is located in `/Users/xyz/envizi-integration-hub-app/api/config/envizi-config.json`

4. Run the below command to create virutal environment (first time only).
```
python -m venv myvenv
source myvenv/bin/activate

python -m pip install -r requirements.txt
```

5. Run the below command to start the app.

```
export WRITE_INTERIM_FILES=FALSE
export LOGLEVEL=INFO
export ENVIZI_CONFIG_FILE="/Users/xyz/envizi-integration-hub-app/api/config/envizi-config.json"
export DATA_FOLDER="/Users/xyz/envizi-integration-hub-app/api/data"
export DATA_STORE_FOLDER="/Users/xyz/envizi-integration-hub-app/api/data-store"

export OUTPUT_FOLDER="/Users/xyz/envizi-integration-hub-app/output"


python main.py

```

## 2. Start the Web App (Reactjs)

Note: You can refer the following documentation [here](../../60-utils/01-configuring-redhat-enterprise-linux-for-running-web-app)

1. Update the Python App URL in the file `envizi-integration-hub-app/web/src/components/common-constants.js`
```
export const API_URL = 'http://localhost:3001';
```

2. Run the below command build  (first time only).
```
 yarn build
```

3. Run the below command to start the app.

```
yarn run dev
```

4. Open the url in your browser http://localhost:3000/


