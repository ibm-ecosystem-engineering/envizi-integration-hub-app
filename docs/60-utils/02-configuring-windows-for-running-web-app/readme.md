# How to configure Windows for running the web app

This document explains about how to install the following in Windows for to run Integration Hub web app.

- NVM
- Node
- Yarn
- Web App

### 1. Install Nvm

Install NVM in Windows, if you have not isntalled.

1. Download and Install the lastest nvm-setup.exe from the URL. https://github.com/coreybutler/nvm-windows/releases

The latest exe could be the following: 
https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe


2. Verify the installation by checking the version.

```
C:\Users\Administrator> nvm -version
1.1.12
```

### 2. Install Node

1. Run the following command to install Node.

```
nvm install node
```

2. Verify the installation by checking the version.

```
C:\Users\Administrator>node --version
v23.1.0
```

### 3. Install Yarn

1. Run the following command to install Yarn.

```
nvm install yarn
```

2. Verify the installation by checking the version.

```
C:\Users\Administrator>yarn --version
1.22.22
```


### 5. Clone the Web App

1. Download and install git from the url https://git-scm.com/downloads/win

2. Clone the Web App.

```
git clone https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app.git
```

### 6. Run the Web App

1. Goto the web directory

```
cd envizi-integration-hub-app/web
```

2. Run the below command to build the app.

```
yarn install
```

3. Run the below command to run the app.

```
yarn run dev
```

4. Access the app

```
http://localhost:3000
```
