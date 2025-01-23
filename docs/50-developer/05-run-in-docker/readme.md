# Starting the App using Docker / Podman

This document provides instructions on how to start Envizi Integration Hub using Docker / Podman.

You will need to start two applications:

Backend API app (Python-based)
Frontend app (React.js-based)


## 1. Starting the Backend API app (Python-based)

Lets start the Backend API App in Linux VM.

1. The config file available in repo [here](../../../../api/config/envizi-config-sample.json)

2. Download and rename the file `envizi-config-sample.json` into `envizi-config.json`

3. Lets us assume this file is located in `/tmp/envizi-config.json`

4. Run the below command to start the app.

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


2. Starting Frontend app (React.js-based)

Lets start the Frontend App in Linux VM.

1. Replace the `##IP_ADDRESS_OF_VM##` with the actual IP address of the VM where API App is running.

```
podman run -d -p 3000:3000 --name my-e-int-hub2-ui --env NEXT_PUBLIC_API_URL="http://##IP_ADDRESS_OF_VM##:3001"  gandigit/e-int-hub2-ui-linux:latest
```

2. Run the above command to start the UI app.

#### Note

- To run the same in `Mac`, you need to change the image `e-int-hub2-ui-linux` into `e-int-hub2-ui-mac` in the above command.

- To run the same using `Podman` instead of `Docker`, you need to change the  `docker` into `podman` in the above command.

3. Open the url `http://##IP_ADDRESS_OF_VM##:3000/hello` in the browser to see if it is working.

4. The below home page should have been displayed.

<img src="images/img-15-home.png">

## 3. Stop the App (for info only)

Run the below commands one by one to stop the apps.

```
docker stop my-e-int2-hub
docker rm my-e-int2-hub

docker stop my-e-int2-hub-ui
docker rm my-e-int2-hub-ui
```

## 4. View App logs (for info only)

Run the below commmand to view the logs of the apps.

```
docker logs my-e-int2-hub

docker logs my-e-int2-hub-ui
```