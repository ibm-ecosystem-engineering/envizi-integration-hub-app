# Build step #2: build the API with the client as static files
FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./src /app
COPY ./config/envizi-sample-config.json /app/envizi-config.json
COPY ./data /app/data
COPY ./data-store /app/data

ENV ENVIZI_CONFIG_FILE ./envizi-config.json
ENV DATA_FOLDER /app/data
ENV DATA_STORE_FOLDER  /app/data
ENV OUTPUT_FOLDER  /app/output
ENV STOP_S3_PUSH  FALSE
ENV LOAD_ENVIZI_DATA  FALSE
ENV FLASK_ENV production

EXPOSE 3001

CMD ["python", "-u", "main.py"]
