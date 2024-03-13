
# Build step #2: build the API with the client as static files
FROM python:3.9-slim

WORKDIR /app

COPY . /app
COPY ./app/data /app/data
RUN pip install -r requirements.txt
ENV FLASK_ENV production

EXPOSE 3001

CMD ["python", "-u", "./app/main.py"]
