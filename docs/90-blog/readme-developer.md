Integration Hub is a solution accelerator to facilitate the integration of ESG data from various sources into the IBM Envizi ESG Suite. The Hub provides configurable hooks to Integrate with any ESG data source, helps transform and integrate.

[Watch the quick overview video about the Integration Hub.]

[![Watch the video](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/F_khZj2DVJoZrLYi3yjYew/arch.png)](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/yUvGZTf_M5A_C_0f7mon_w/integation-hub-intro.mp4)

It leverage Envizi’s data flow automation capability and align with data templates. There are two pathways ingesting data into Envizi.
- On the top it shows ENVIZI SERVICES PATHWAY  via Expert Labs which is a paid services.
- On the bottom is the SELF SERVICES PATHWAY for clients or partners to take  complete ownership  DataTransformation and Integration. 

Integration Hub is a one of the solution for the SELF SERVICES PATHWAY. As part of this we provide you the Development toolkit to enable the Integration Specialists, Practioners, developers or managed services team to quickly build integration showcases.

![data-flow-automation.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/zbe8CHszxYbKvYs1IDZnEQ/data-flow-automation.png)


The following integrations are available in Integration Hub as of now.

1. Excel Integrations
2. WebHook Integrations (SAP, ERP Systems)
3. Invoice Processing
4. Utility Bill Processing
5. Turbonomic Integration

This Integration Hub can be extended to include integration with numerous other external systems that need to interface with the IBM Envizi ESG Suite. It connects to external systems, such as Turbonomic, Webhook API, Watson Discovery and etc, retrieves emissions data, converts this data into the Universal Account Setup and Data Loading format (UDC), and then dispatches it to an S3 bucket configured within the IBM Envizi ESG Suite.

The entire source code and detailed documentation of this application is available [here](https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app).

You can find more detailed information in section below on each of the integrations, how to deploy, run and extend the application further based on your need.

## Prerequisites

- Ensure you have access to an Envizi instance.

# 1. Integrations 

Lets us explore about the various integrations available.

## 1.1. Excel Integrations

Excel files can be integrated into Envizi using this Integration Hub.

[Watch the quick demo video about Excel Integration]

[![Watch the video](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/lEh9eGvGFsO7RId1s3TiIw/image-video-excel.png)](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/6VspZUjxEq1J5-DxhCOKXQ/Integration-Hub-Excel-Demo.mov)


### Excel Mappings list

Each excel file formats of the customer data could be mapped to POC / Account setup and Data Load PM&C templates.

Here is the list of excel mappings available.

![image11-excel-1.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/pDmK8Fve6mOEWoR5Onz90A/image11-excel-1.png)

The mapping `C-Corp Travel Data` in the above list is for the below excel file.

![image11-excel-5.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/nqlkiWyJmbzO1DTPKVdVWA/image11-excel-5.png)


Lets see the details of this mapping below.

### Excel Mapping Detail

Here is the mapping details page for the above excel file.

- **Organization :** This column is hard coded with the `IBM APAC` text.
- **Location :** This column is mapped to the `Places` column of the excel.
- **Account Number :** This column is mapped to the `Subject Name` column of the excel.
- **Total cost (incl. Tax) in local currency :** This column is mapped to the sum of `Cost A` + `Cost B` + `Cost C` columns of the excel.

![image11-excel-2.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/q7HZgv2IkL-_hUAFH2qqBA/image11-excel-2.png)
![image11-excel-3.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/4AgodS_T4GReXlsyugo85w/image11-excel-3.png)
![image11-excel-4.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/cFPh2i2kIzJRC3LOZ4G6FA/image11-excel-4.png)

### Upload Excel

You can upload the data file and click on the `Load Source Data`

![image11-excel-6.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/fW0tnpWX0zaSRVdjd7up2Q/image11-excel-6.png)
### Preview

You can preview the data conversion into Envizi format by click on the `Preview` 

![image11-excel-7.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/dv7jf_QDxC1h9jt0pQI55w/image11-excel-7.png)
It will show the converted data as below.

![image11-excel-8.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/9v7xN6f9xMYDYT_8X95CUw/image11-excel-8.png)

### Ingest to Envizi

You can push the data to Envizi.

![image11-excel-9.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/SJq4PjN65R8Ehtg0fQwZYQ/image11-excel-9.png)

### 1.2. Webhook Integrations

When any ERP systems or any other application can able to expose API, the Integration Hub can be connected to the API, pull the data, transform the data into Envizi format based on the given mapping and push the data into Envizi.


When any ERP systems or any other application can able to expose API, the Integration Hub can be connected to the API, pull the data, transform the data into Envizi format based on the given mapping and push the data into ABCD app.

[Watch the quick demo video about Webhook Integration]

[![Watch the video](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/APwG-J4_UyTlBOB6cB6zwA/image-video-webhook.png)](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/KZjZKdNwmVAaFzWcSfglEQ/Integration-Hub-Webhook-Demo.mov)


### Webhook Mappings list

Each Webhook response could be mapped to POC / Account setup and Data Load PM&C templates.

Here is the list of sample Webhook mappings available.

![image12-webhook-11.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/AzcJGZHJvFRHa0ji2L1bNA/image12-webhook-11.png)


The details of the `Elite ERP` mapping from the above list is given below.

### Webhook Mapping Detail

Let's see the mapping details.

![image12-webhook-12.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Qutkpofya2fD7TNqoHjSCw/image12-webhook-12.png)
![image12-webhook-13.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ToBNrsI732MUu5d2iKc_Hg/image12-webhook-13.png)
![image12-webhook-14.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/tKUQhIOm8rG18oc-nyNC7w/image12-webhook-14.png)
![image12-webhook-15.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/jkUPkykjyxe9fR-2AGfmww/image12-webhook-15.png)
![image12-webhook-16.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/B5cV6S_2bQib7pIF6Fukmw/image12-webhook-16.png)
![image12-webhook-17.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/OYLiTL8zuLSsvzhwYIZ_3g/image12-webhook-17.png)


### Preview

You can preview the data conversion into Envizi format by click on the `Preview` 

![image12-webhook-18.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/m_S61q99i8TYhbYYk_Un5w/image12-webhook-18.png)

It will show the converted data as below.

![image12-webhook-19.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/k0Wn2iyDDRZrA5hcRkqtdw/image12-webhook-19.png)

### Ingest to Envizi

You can push the data to Envizi.

![image12-webhook-20.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/6K9T0LDAgCcqNxbYx41xeQ/image12-webhook-20.png)

## 1.3. Invoice Integrations

The Integration Hub helps to read PDF Invoices using IBM Watson Discovery and create a Envizi Scope-3 Category-1 AI Assist Template files to push the Utility data into Envizi.

The Invoices are stored in IBM Watson Discovery as a collections.

Smart Document Understanding (SDU) trains IBM Watson Discovery to extract custom fields from the Invoices.

The Integration Hub can pull the data from the Watson Discovery and Convert the data into the Envizi format.

## Invoices in Watson Discovery

The Invoices are kept in the Watson Discovery.

![image13-invoice-1.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/eJpdnhWPlj2ARKxTSXwGIA/image13-invoice-1.png)

Smart Document Understanding helps to extract custom fields from the invoices.

![image13-invoice-2.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/pktEuqlsH7FwAXqSIy1EWA/image13-invoice-2.png)

The sample invoices are available here. 
- [Invoice1-94400.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/mks2WqNRdkLPqaPs3_7w3g/Invoice1-94400.pdf  "Invoice1-94400.pdf")
- [Invoice2.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/1JxjmPrlmE-B78dMoHBUxQ/Invoice2.pdf  "Invoice2.pdf")
- [Invoice3-UniverComputers.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/A8MimdeDFvIlmHWOPK36AQ/Invoice3-UniverComputers.pdf  "Invoice3-UniverComputers.pdf")
- [Invoice11-53100.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/V4-LiqfOjb0RsYf11KBb_Q/Invoice11-53100.pdf  "Invoice11-53100.pdf")
- [Invoice12-7080.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/dhaPmMrNkpTTbfdDXtAvHw/Invoice12-7080.pdf  "Invoice12-7080.pdf")
- [Invoice21.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/S0S8dGzmT5lMheUE7e_oBw/Invoice21.pdf  "Invoice21.pdf")


## Integration of Invoices into Envizi 

This section will communicate with the Watson Discovery to pull the data and convert into the Envizi format and Push to S3 bucket configured.

![image13-invoice-3.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ywcN4gTVAE6dBgyJCfBwxQ/image13-invoice-3.png)
![image13-invoice-4.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/yCHBtDZAQFE9CLwF3VNxrA/image13-invoice-4.png)


## 1.4. Utility Bill Integrations

The Integration Hub helps to read Utility bills of PDF format using IBM Watson Discovery and create a Envizi UDC template files to push the Utility bills data into Envizi.

The utility bills are stored in IBM Watson Discovery as a collections.

Smart Document Understanding (SDU) trains IBM Watson™ Discovery to extract custom fields from the utility bills.

The Integration Hub can pull the data from the Watson Discovery and Convert the data into the Envizi format.

### Utility Bills in Watson Discovery

The Utlity bills are kept in the Watson Discovery.

![image14-utility-1.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/NOgN8XkIDaJC2z-q5ZCc9g/image14-utility-1.png)

Smart Document Understanding helps to extract custom fields from the utility bills.

![image14-utility-2.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/XyjOJxkwoFfEjOEzBtview/image14-utility-2.png)

The sample utility bills are available here.  
- [utilitybills1-Ind.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/pX7FBKZ2YEcVxlt_708h_A/utilitybills1-Ind.pdf  "utilitybills1-Ind.pdf")

- [utilitybills3-WB.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/C9gM66UUJYuD4RWxUvDZ2w/utilitybills3-WB.pdf  "utilitybills3-WB.pdf")

- [utilitybills5-maxi.pdf](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/__P7J7JUl16FsPFqQuKA-Q/utilitybills5-maxi.pdf  "utilitybills5-maxi.pdf")


### Integration of Utility Bills into Envizi

This section will communicate with the Watson Discover to pull the data and covert into the Envizi format and Push to S3 bucket configured.

![image14-utility-3.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/mTOtkpqt3ZBOfPNQcxMHxQ/image14-utility-3.png)

### 1.5. Turbonomic Integrations

Integration Hub can able to integrate into IBM Turbonomic to be get the energy consumption of the Data centre.

Here are the various data from Turbonomic pulled into Envizi.

The below images shows the `Groups & Locations` data retrieved  from Turbonomic and converted in Envizi format.

![image15-turbo-11.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Dyk6EpPfUxcjW9dObAMaZg/image15-turbo-11.png)

The below image shows the `Accounts and Data` containing the `Energy Consumption` details.

![image15-turbo-12.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/nccwXAhkZjVHYU-_0FIfIw/image15-turbo-12.png)

The below image shows the `Accounts and Data` containing the `Active Hosts` details.

![image15-turbo-13.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/H6Yu1Bn5EHfBhuYikI29YQ/image15-turbo-13.png)

The below image shows the `Accounts and Data` containing the `Active VMs` details.

![image15-turbo-14.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/H_nNqDeJXQPobosted7xIg/image15-turbo-14.png)


The below image shows the `Accounts and Data` containing the `Energy Host Intensity` details.

![image15-turbo-15.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/889DupmQRR-PNZhNzuSUBQ/image15-turbo-15.png)


The below image shows the `Accounts and Data` containing the `VM Host Density` details.

![image15-turbo-16.png](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/x_f39r2tsCod-sIEeDNwKw/image15-turbo-16.png)


## 2. Run this Application

The source code of this application is available in https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app. 

1. Download this repo and keep it for further steps below.

### 2.1 Run in Local

This document explains about how to run the Envizi Integration Hub using Source code.

You need to start 2 apps (API app and UI app).

#### 2.1.1. Start the API App (Python)

1. Download this repo https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app.

2. Prepare Configuration file  `envizi-config.json` using the steps given in the above repo.

3. Keep the property file `envizi-config.json` in some folder. Lets us assume the file is located in `/Users/xyz/envizi-integration-hub-app/api/config/envizi-config.json`

4. Run the below command to create virtual environment (first time only).
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

#### 2.1.2 Start the Web App (Reactjs)

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


### 2.2 Run as Container

This section explains about how to start Envizi Integration Hub in Docker / Podman.

You need to run the 2 docker images (API app and UI app).

#### 2.2.1. Start the API App 

Lets start the API App in Linux VM.

1. Keep the configuration file `envizi-config.json` in some folder. Lets us assume the file is located in `/tmp/envizi-config.json`

2. Run the below command to start the app.

The abolve file name is mentioned in the `-v` parameter here and suffixed with `:/app/envizi-config.json`

```
docker run -d -p 3001:3001 --name my-e-int2-hub \
    --env LOGLEVEL=DEBUG \
    --env DATA_FOLDER="/app/data" \
    --env DATA_STORE_FOLDER="/app/data" \
    --env OUTPUT_FOLDER="/app/output" \
    -v "/tmp/envizi-config.json:/app/envizi-config.json" \
    gandigit/e-int-hub2-linux:latest

```

#### Note

- To run the same in `Mac`, you need to change the image `e-int-hub2-linux` into `e-int-hub2-mac` in the above command.

- To run the same using `Podman` instead of `Docker`, you need to change the  `docker` into `podman` in the above command.

3. Open the url `http://##IP_ADDRESS_OF_VM##:3001/hello` in the browser to see if it is working.


#### 2.2.2 Start the UI App 

Lets start the UI App in Linux VM.

1. Replace the `##IP_ADDRESS_OF_VM##` with the actual IP address of the VM where API App is running.

```
podman run -d -p 3000:3000 --name my-e-int-hub2-ui --env NEXT_PUBLIC_API_URL="http://##IP_ADDRESS_OF_VM##:3001"  gandigit/e-int-hub2-ui-linux:latest
```

2. Run the above command to start the UI app.

#### Note

- To run the same in `Mac`, you need to change the image `e-int-hub2-ui-linux` into `e-int-hub2-ui-mac` in the above command.

- To run the same using `Podman` instead of `Docker`, you need to change the  `docker` into `podman` in the above command.

3. Open the url `http://##IP_ADDRESS_OF_VM##:3000/hello` in the browser to see if it is working.

## 3. How to extend this application

This repo (https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app) is available as a open source. You are free to download, extend and use it.

## Summary

Using the Envizi Integration Hub we were able to successfully integrate various forms of data into the IBM Envizi ESG Suite.

## Next steps

The next step is to Get a closer look at IBM Envizi and how it can help accelerate your ESG strategy.

Start your 14-day IBM Envizi ESG Suite trial
https://www.ibm.com/account/reg/us-en/signup?formid=urx-51938

Request your personalized IBM Envizi demo
https://www.ibm.com/account/reg/us-en/signup?formid=DEMO-envizi