# How to configure Windows for running the FrontEnd - Web app

This document explains the steps for installing the necessary components/tools on Windows to run the Integration Hub web app.

Here, you will be installing the following items.
- Nvm
- Node
- Yarn

### 1. Install Nvm

1. Download and Install the lastest nvm-setup.exe from the URL. https://github.com/coreybutler/nvm-windows/releases

(The latest exe could be the following: 
https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe)


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

### 4. Download the Web App

1. Download and install git from the url https://git-scm.com/downloads/win

2. Clone the Web App.

```
git clone https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app.git
```
