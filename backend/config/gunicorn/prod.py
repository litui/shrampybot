"""Gunicorn *development* config file"""

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "shrampybot.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 4
# The socket to bind
bind = "0.0.0.0:818"
# Restart workers when code changes (development only!)
reload = False
# Write access and error info to /var/log
accesslog = errorlog = "../log/gunicorn-prod.log"
# Redirect stdout/stderr to log file
capture_output = False
# PID file so you can easily fetch process ID
pidfile = "/var/lib/gsg/gunicorn-prod.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = False

