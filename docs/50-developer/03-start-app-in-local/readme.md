# Envizi Integration Hub - Starting the App using Source code

This document explains about how to start Envizi Integration Hub using Source code.

You need to start 2 apps (API app and UI app).

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

5. Replace `/Users/xyz/envizi-integration-hub-app` with your folder structure in the below commands.

6. Run the below command to start the app.

```
export WRITE_INTERIM_FILES=FALSE
export LOGLEVEL=INFO
export ENVIZI_CONFIG_FILE="/Users/xyz/envizi-integration-hub-app/api/config/envizi-config.json"
export DATA_FOLDER="/Users/xyz/envizi-integration-hub-app/api/data"
export DATA_STORE_FOLDER="/Users/xyz/envizi-integration-hub-app/api/data-store"

export OUTPUT_FOLDER="/Users/xyz/envizi-integration-hub-app/output"

cd /Users/xyz/envizi-integration-hub-app/api

python src/main.py

```

7. Open the url in your browser http://localhost:3001/hello to check if it is working.

**Note:** If you are running this in VM, then instead of `localhost` you need to give the `IP-Address` of your vm.

## 2. Start the Web App (Reactjs)

We need to pass the URL of the Python API App to the Web App. 

1. Create `.env` file with the below content under the `web` folder.
```
NEXT_PUBLIC_API_URL=http://localhost:3001
```

**Note:** If you are running this in VM, then instead of `localhost` you need to give the `IP-Address` of your vm.

2. Run the below command build  (first time only).
```
 yarn build
```

3. Run the below command to start the app.

```
yarn run dev
```

4. Open the url in your browser http://localhost:3000/

**Note:** If you are running this in VM, then instead of `localhost` you need to give the `IP-Address` of your vm.