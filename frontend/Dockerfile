FROM node:lts
LABEL org.opencontainers.image.source=https://github.com/litui/shrampybot
LABEL org.opencontainers.image.description="ShrampyBot Frontend"
LABEL org.opencontainers.image.licenses=MIT

COPY ./package.json /gsg/frontend/
COPY ./package-lock.json /gsg/frontend/
WORKDIR /gsg/frontend
RUN npm install


COPY . /gsg/frontend

VOLUME [ "/gsg/frontend/src", "/gsg/frontend/dist" ]
CMD ["npm", "run", "dev"]
