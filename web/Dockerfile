# This Dockerfile builds the React front end for nginx.
# It also proxies /api requests to api:5000

FROM node:18-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY ./src ./src
COPY ./public ./public
RUN npm install

EXPOSE 3000
CMD ["npm", "run", "dev"]

# # Build step #2: build an nginx container
# FROM nginx:stable-alpine
# COPY --from=build-step /app/build /usr/share/nginx/html
# COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf


# FROM node:10.16.0-alpine

# WORKDIR /usr/src/app
# ENV PATH /usr/src/app/node_modules/.bin:$PATH

# # install and cache app dependencies
# COPY package.json /usr/src/app/package.json

# RUN npm install

# EXPOSE 3000
# CMD ["npm", "run", "dev"]