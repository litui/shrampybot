FROM python:3
LABEL org.opencontainers.image.source=https://github.com/litui/shrampybot
LABEL org.opencontainers.image.description="ShrampyBot Backend"
LABEL org.opencontainers.image.licenses=MIT
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

RUN useradd -ms /bin/bash shrampybot
RUN addgroup shrampybot www-data
# RUN addgroup shrampybot ssl-cert

COPY ca-certificates/* /usr/local/share/ca-certificates
RUN update-ca-certificates

WORKDIR /gsg/backend
RUN chown -R shrampybot:www-data /gsg
USER shrampybot
COPY requirements.txt /gsg/backend/

RUN pip install --user -r requirements.txt

WORKDIR /gsg/backend/code

# COPY manage.py /gsg/backend/

VOLUME [ "/gsg/backend/code" ]

CMD ["./manage.py", "runserver", "0.0.0.0:8188"]

