# Prerequisite Installation for Frontend App on Linux (RedHat Enterprise Linux)

This document explains the steps for installing the necessary components/tools on RedHat Enterprise Linux 9.4 for to run a Carbon React Web application using yarn.

- NVM
- Node
- Yarn


### 1. Install Nvm

 Install NVM using the following script.

1. Run the following script to download script from GitHub

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
```

2. Append the nvm and bash_completion source string lines to the ~/.bashrc file.

```
source ~/.bashrc

```

3. Verify the installation by checking the version.

```
[root@c98199v1 ~]# nvm --version
0.40.1
```


### 2. Install Node

1. Run the below command to install the node.

```
nvm install node
```

2. Verify the installation by checking the version.

```
[root@c98199v1 ~]# node --version
v23.1.0
```

### 3. Install Yarn

Install Yarn using Yum Package Manager

1. Run the below command to Configuring the official Yarn repository on your system

```
curl -sL https://dl.yarnpkg.com/rpm/yarn.repo -o /etc/yum.repos.d/yarn.repo 
```

2. Run the below command to install yarn.

```
sudo yum install yarn 
```

3. Verify the installation by checking the version.

```
[root@c98199v1 ~]#  yarn --version
1.22.22
```


### 4. Download the Web App

1. Run the below command to install git

```
sudo yum install git
```

2. Clone the Web App.

```
git clone https://github.com/ibm-ecosystem-engineering/envizi-integration-hub-app.git
```

#### Reference

1. How to Install Yarn on CentOS/RHEL & Fedora
https://tecadmin.net/install-yarn-centos/

2. How to Install Node.js 20 on Rocky Linux 9 or RHEL 9
https://jumpcloud.com/blog/how-to-install-node-js-20-rocky-linux-9-rhel-9

