FROM node:latest

WORKDIR /app

COPY package.json .

RUN yarn add sharp
RUN yarn

COPY . .

RUN yarn build

EXPOSE 3000
CMD ["yarn", "start"]
