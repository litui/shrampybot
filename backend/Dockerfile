FROM python:3
LABEL org.opencontainers.image.source=https://github.com/litui/shrampybot
LABEL org.opencontainers.image.description="ShrampyBot Backend"
LABEL org.opencontainers.image.licenses=MIT
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash shrampybot
RUN addgroup shrampybot www-data

WORKDIR /gsg/backend
RUN chown -R shrampybot:www-data /gsg
USER shrampybot
COPY requirements.txt /gsg/backend/

RUN pip install --user -r requirements.txt

COPY code/manage.py /gsg/backend/

VOLUME [ "/gsg/backend/code" ]

CMD ["./manage.py", "runserver", "0.0.0.0:8188"]

