# Envizi Integration Hub - Starting the App using Python src code

This document explains about how to start Envizi Integration Hub using Python src code.

The Integration Hub App should be started with the configuration file.

## Steps

1. Download this repo.

2. Prepare Configuration file by using the link [02-readme_prepare_config_file.md](./02-readme_prepare_config_file.md)

3. Keep the property file `envizi-config.json` in some folder. Lets us assume the file is located in `/tmp/envizi-config.json`

4. Run the below command to create virutal environment (first time only).
```
python -m venv myvenv
source myvenv/bin/activate

python -m pip install -r requirements.txt
```

5. Run the below command to start the app.

```
export WRITE_INTERIM_FILES=FALSE
export LOGLEVEL=INFO
export ENVIZI_CONFIG_FILE="/tmp/envizi-config.json"
export DATA_FOLDER="/tmp/app/data"
export OUTPUT_FOLDER="/tmp/output"

python app/main.py


```



