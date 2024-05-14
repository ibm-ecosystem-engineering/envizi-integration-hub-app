# Envizi Integration Hub - Copying UI (ReactJs) files to Python App

This document explains about how to Copy UI (ReactJs) files to Python App.

## Steps

1. Download this repo.

2. Goto the `web` folder

```
cd web
```

3. Update the `API_FOLDER_STATIC` in `10-copy-ui-files-to-app.sh` as per your need.

This should point to the `/app/static` subfolder of this repo.

```
API_FOLDER_STATIC=/Users/tttt/envizi-integration-hub/app/static
```

4. Run the below to copy the ReactJs files to Python app.
```
sh 10-copy-ui-files-to-app.sh
```



