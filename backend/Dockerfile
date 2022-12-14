FROM python:3
LABEL org.opencontainers.image.source=https://github.com/litui/shrampybot
LABEL org.opencontainers.image.description="ShrampyBot Backend"
LABEL org.opencontainers.image.licenses=MIT
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# COPY ./yennifer.crt /usr/local/share/ca-certificates
# RUN update-ca-certificates
RUN useradd -ms /bin/bash shrampybot
RUN addgroup shrampybot www-data

WORKDIR /gsg/backend
RUN chown -R shrampybot:www-data /gsg
USER shrampybot
COPY requirements.txt /gsg/backend/

RUN pip install --user -r requirements.txt

COPY . /gsg/backend/

CMD ["gunicorn", "-c", "config/gunicorn/prod.py", "-b", "0.0.0.0:8188"]
