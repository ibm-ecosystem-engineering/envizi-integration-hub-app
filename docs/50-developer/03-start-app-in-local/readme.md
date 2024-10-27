# Envizi Integration Hub - Starting the App using Source code

This document provides instructions on how to start Envizi Integration Hub from the source code.

You will  need to start two applications:
1. Backend API app (Python-based)
2. Frontend app (React.js-based)

## Prerequisites

You need to have the following softwares installed in your environment.

1. Python 3.x

2. Nvm, Node and Yarn. Refer the installation steps for [Linux/Mac](../../60-utils/01-configuring-redhat-enterprise-linux-for-running-web-app), [Windows](../../60-utils/02-configuring-windows-for-running-web-app)


## 1. Download this repo

1. Download this repo (https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app). 

2. Let's assume the repository has been downloaded, with its root folder located at `/Users/xyz/envizi-integration-hub-app`.


## 2. Starting Backend API app (Python-based)

1. Open a new command or terminal window.

2. Goto the repository root folder by running the below command.

```
cd /Users/xyz/envizi-integration-hub-app
```

3. Create `virtual environment` by running the below command.

```
python -m venv myvenv-hub
source myvenv-hub/bin/activate
```

4. Install the required python packages by running the below command.
```
python -m pip install -r requirements.txt
```

5. Run the below commands to set the environment properties

Note: Don't forget to replace the `/Users/xyz/envizi-integration-hub-app` with your folder structure.

```
export WRITE_INTERIM_FILES=FALSE
export LOGLEVEL=INFO
export ENVIZI_CONFIG_FILE="/Users/xyz/envizi-integration-hub-app/api/config/envizi-config.json"
export DATA_FOLDER="/Users/xyz/envizi-integration-hub-app/api/data"
export DATA_STORE_FOLDER="/Users/xyz/envizi-integration-hub-app/api/data-store"

export OUTPUT_FOLDER="/Users/xyz/envizi-integration-hub-app/output"
```

6. Run the below commands to start the app

Note: Don't forget to replace the `/Users/xyz/envizi-integration-hub-app` with your folder structure.

```
cd /Users/xyz/envizi-integration-hub-app/api
python src/main.py
```

7. Verify the app is working by opening the url in your browser http://localhost:3001/welcome .

It should display the text `Welcome to the Envizi Integration Hub`

**Note:** If you are running this in VM, then instead of `localhost` you need to give the `IP-Address` of your vm.

## 3. Starting Frontend app (React.js-based)

### Prerequisites

You need to have the `Nvm`, `Node` and `Yarn` installed in your system.

Refer the installation steps for [Linux/Mac](../../60-utils/01-configuring-redhat-enterprise-linux-for-running-web-app), [Windows](../../60-utils/02-configuring-windows-for-running-web-app)


### Steps 


#### Create .env file

We need to pass the URL of the Backend API App (Python based) to the Frontend Web App. 

1. Create `.env` file with the below content under the `web` folder.

```
NEXT_PUBLIC_API_URL=http://localhost:3001
```
**Note:** If you are running this in VM, then instead of `localhost` you need to give the `IP-Address` of your vm.

#### Install yarn dependencies

1. Goto the `web` folder by running the below commnad

```
cd /Users/xyz/envizi-integration-hub-app/web
```
Note: Don't forget to replace the `/Users/xyz/envizi-integration-hub-app` with your folder structure.


2. Run the below command to install year dependent files  (first time only).

```
 yarn install
```

3. Run the below command to start the app.

```
yarn run dev
```

4. Open the url in your browser http://localhost:3000/

**Note:** If you are running this in VM, then instead of `localhost` you need to give the `IP-Address` of your vm.

