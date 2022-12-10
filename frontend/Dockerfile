FROM node:14

WORKDIR /gsg/frontend

COPY . /gsg/frontend

EXPOSE 828

RUN npm install http-server -g

RUN npm install --omit=optional && npm run build

CMD http-server -r -U -p 828
