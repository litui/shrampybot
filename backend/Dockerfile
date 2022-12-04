FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /gsg
COPY requirements.txt /gsg/
RUN pip install -r requirements.txt
COPY . /gsg/
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uwsgi", "--http", "0.0.0.0:5050", "--module", "shrampybot.wsgi"]