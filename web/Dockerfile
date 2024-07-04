FROM node:18-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY ./src ./src
COPY ./public ./public
COPY ./jsconfig.json ./jsconfig.json
RUN npm install

ENV NEXT_PUBLIC_API_URL http://localhost:3001

EXPOSE 3000
CMD ["npm", "run", "dev"]