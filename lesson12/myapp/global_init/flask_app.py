from flask import Flask


def create_flask_app():

    application = Flask(__name__)
    app = application
    app.config.from_object('config')

    app.config.update(CELERY_BROKER_URL='redis://localhost:6379',
                      CELERY_RESULT_BACKEND='redis://localhost:6379')
    return app