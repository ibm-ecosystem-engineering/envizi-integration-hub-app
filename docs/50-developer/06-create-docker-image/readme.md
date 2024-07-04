# Envizi Integration Hub - Creating Docker Image of the App

This document explains about how to create Docker images for this app.

## Steps

1. Download this repo.

2. Goto the `scripts` folder

```
cd scripts
```

### 1. Create API App image

1. Update the docker image name in `01-build-dockerhub.sh` as per your need.
```
DOCKER_IMAGE=gandigit/e-int-hub2
```

2. Run the below to create the docker image.

```
sh 01-build-dockerhub.sh
```

3. Run the below to push the image to the docker registry.

You may need to login into your docker registry before running this.

```
sh 02-push-dockerhub.sh
```

**Note** 
- Replace docker with `podman` if you want to do it via `podman`


### 2. Create UI App image

1. Update the docker image name in `21-build-dockerhub.sh` as per your need.
```
DOCKER_IMAGE=gandigit/e-int-hub2-ui
```

2. Run the below to create the docker image.

```
sh 21-build-dockerhub.sh
```

3. Run the below to push the image to the docker registry.

You may need to login into your docker registry before running this.

```
sh 22-push-dockerhub.sh
```

**Note** 
- Replace docker with `podman` if you want to do it via `podman`
