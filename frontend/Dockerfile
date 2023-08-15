FROM node:18-alpine AS frontend

RUN mkdir -p /app

WORKDIR /app

COPY package*.json ./

RUN npm install -g @quasar/cli

RUN npm install

COPY . .

EXPOSE 9000
