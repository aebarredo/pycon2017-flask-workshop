from flask import Flask


def create_flask_app():

    application = Flask(__name__)
    app = application
    app.config.from_object('config')

    return app