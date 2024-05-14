
# Build step #2: build the API with the client as static files
FROM python:3.9-slim

WORKDIR /app

COPY ./src /app
COPY ./config/envizi-config-sample.json /app/envizi-config.json
COPY ./data /app/data
RUN pip install -r requirements.txt
ENV FLASK_ENV production

EXPOSE 3001

CMD ["python", "-u", "./app/main.py"]
