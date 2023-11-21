# Envizi Integration Hub - Prepare Configuration file

This document explains about how to prepare Configuration file to use in Envizi Integration Hub.

## 1. Download the Config file

1. Download the [envizi-config-sample.json](../config/envizi-config-sample.json)
2. Rename it to `envizi-config.json`

## 2. Update Envizi s3 bucket details

Update the below envizi s3 bucket details from the data we noted while creating Data service in envizi.

```
  "envizi": {
    "access": {
      "bucket_name": "envizi-client-dataservice-us-prod",
      "folder_name": "client_9608cd600af647",
      "access_key": "xxxx",
      "secret_key": "xxxxx"
    },
  }
```

## 3. Update Envizi OrgName

Update `org_name` in `envizi` section.

The Org Name is your organization name in the org hierarchy.
```
  "envizi": {
    "parameters": {
      "org_name": "Demo Corp D4",
    }
  },
```
<img src="images/img-14-orgname.png">

## 4. Update Envizi Prefix (Optional)

Update `prefix` in `envizi` section.

This helps to create all the groups, locations and accounts created by this integration hub prefixed to avoid duplicates if any.
```
  "envizi": {
    "parameters": {
      "prefix": "G2"
    }
  },
```

## 5. Update Turbonomic access

Update the below Turbonomic access details.

The user should have `Observer` role.

```
  "turbo": {
    "access": {
      "url": "https://xxxxx.turbonomic.com",
      "user": "",
      "password": ""
    },
  }
```
## 6. Update Turbonomic parameters (Optional)

Here are the Turbonomic parameters. You may need to modify `account_style_xxxxx` properties as per your environment. Otherwise no updates are required in the parameters. You can see the below explanations about the parameters.

```
  "turbo": {
    "parameters": {
      "group": "Sustainable-IT",
      "sub_group": "Turbonomic",
      "account_style_energy_consumption": "S2 - Electricity - kWh",
      "account_style_active_hosts": "Building Attributes - Headcount",
      "account_style_active_vms": "Building Attributes - Headcount",
      "account_style_energy_host_intensity": "Building Attributes - Headcount",
      "account_style_vm_host_density": "Building Attributes - Headcount",
      "start_date": "2023-10-30",
      "end_date": "2023-11-04"
    }
  }
```

1. The `group` and `sub_group` are created as `Groups` in Organization Hierarchy.
2. Each datacenter from Turbonomic is created as a `Location` under the `sub_group`.
3. The below  `Accounts` and `Account Styles` should be created for each Datacenter from Turbonomic.
  ```
  Account                         Account Style
  -----------------------         ------------------------
  Energy Consumption      ---     Energy Consumption - kWh
  Active Hosts            ---     Active Hosts [Number]     
  Active VMs              ---     Active Virtual Machines [Number]
  Energy Host Intensity   ---     Energy Host Intensity - kWh/host
  VM Host Density         ---     Virtual Machine to Host Density - VM/Host
  ```
4. If you have these `Account Styles` in your environment you can update the `account_style_xxxxx` properties with the your values. Otherwise just leave it for default as they are available in UDC. 