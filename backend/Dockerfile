FROM python:3
LABEL org.opencontainers.image.source=https://github.com/litui/shrampybot
LABEL org.opencontainers.image.description="ShrampyBot Backend"
LABEL org.opencontainers.image.licenses=MIT
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /gsg/backend
COPY ./yennifer.crt /usr/local/share/ca-certificates
RUN update-ca-certificates
COPY requirements.txt /gsg/backend/
RUN pip install -r requirements.txt
RUN useradd -ms /bin/bash shrampybot
RUN addgroup shrampybot www-data
RUN chown -R www-data:www-data /gsg
USER shrampybot
COPY . /gsg/backend/
USER root
CMD ["gunicorn", "-c", "config/gunicorn/prod.py", "-b", "0.0.0.0:818"]
