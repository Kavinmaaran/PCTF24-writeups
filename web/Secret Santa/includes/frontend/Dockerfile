FROM node:14-alpine as build
WORKDIR /app
COPY ./package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine
# RUN apt-get update && apt-get install -y nginx-mod-http-headers-mor

COPY --from=build /app/build /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
