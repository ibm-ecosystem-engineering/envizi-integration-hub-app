# How to configure RedHat Enterprise Linux for running the web app

This document explains about how to install the following in Redhat RedHat Enterprise Linux 9.4 for to run a Carbon React Web application using yarn.
- Yarn
- NVM
- Node

### 1. Install Yarn

Install Yarn using Yum Package Manager

1. Run the below command to Configuring the official Yarn repository on your system

```
curl -sL https://dl.yarnpkg.com/rpm/yarn.repo -o /etc/yum.repos.d/yarn.repo 
```

2. Run the below command to install yarn.

```
sudo yum install yarn 
```

### 2. Install Nvm

 Install NVM on RHEL 9

1. Run the following script to download script from GitHub

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
```

2. Append the nvm and bash_completion source string lines to the ~/.bashrc file.

```
source ~/.bashrc

```

### 3. Install Node

1. Run the following script download script from GitHub

```
nvm install node
```

### 4. Check the versions 

Here are the versions installed.

```
[root@c62132v1 web]# npm -version
10.7.0
[root@c62132v1 web]# node --version
v22.2.0
[root@c62132v1 web]# yarn --version
1.22.19
```

#### Reference

1. How to Install Yarn on CentOS/RHEL & Fedora
https://tecadmin.net/install-yarn-centos/

2. How to Install Node.js 20 on Rocky Linux 9 or RHEL 9
https://jumpcloud.com/blog/how-to-install-node-js-20-rocky-linux-9-rhel-9

