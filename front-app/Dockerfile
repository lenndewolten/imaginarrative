FROM node:lts-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN yarn

COPY . .

ARG ENV_FILE
COPY ${ENV_FILE} .env


RUN yarn build


FROM nginx:alpine


COPY --from=build /app/dist /usr/share/nginx/html


EXPOSE 80


CMD ["nginx", "-g", "daemon off;"]