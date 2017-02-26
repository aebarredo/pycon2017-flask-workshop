import os
import logging

from logging.handlers import RotatingFileHandler

def setup_logger(app):

    if os.path.exists('log') is False:
        os.mkdir('log')

    if app.config['DEBUG'] is True:
        formatter = logging.Formatter("%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
        loglevel = logging.DEBUG
    else:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s ")
        loglevel = logging.INFO

    handler = RotatingFileHandler('/opt/python/log/myapp.log', backupCount=10, maxBytes=5000000)
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(loglevel)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    log.addHandler(handler)

    logger = app.logger

    return logger