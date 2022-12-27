FROM nginx:latest

RUN apt update && apt install -y wait-for-it

COPY ./nginx.conf.template /tmp/nginx.conf.template
