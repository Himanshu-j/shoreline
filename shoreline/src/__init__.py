import os
import time
import logging
from flask import Flask
from logging.handlers import RotatingFileHandler

from src.api import api

# Create and Initialise flask server
app = Flask(__name__)
api.init_app(app)


# This section handles Logging part of the server
if not os.path.exists('service_logs'):
    os.mkdir('service_logs')
file_handler = RotatingFileHandler(
    filename='service_logs/debug.log',
    maxBytes=1024 * 1024,
    backupCount=10)
log_format = r"[%(asctime)s] %(levelname)s [%(name)s." \
             r"%(funcName)s:%(lineno)d] %(message)s"
log_formatter = logging.Formatter(log_format)
log_formatter.converter = time.localtime
file_handler.setFormatter(log_formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
