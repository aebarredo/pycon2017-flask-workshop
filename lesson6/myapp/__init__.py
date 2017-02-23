import json

from flask import Flask, request
from flask_restful import Api

from myapp.global_init import app, Session

from .controllers import InfoHandler

api = Api(app)

api.add_resource(InfoHandler, '/v3/info', endpoint='info1')
api.add_resource(InfoHandler, '/v3/info/<info_id>', endpoint='info2')


@app.after_request
def after_request_sequence(response):
    #logger.debug('After request, remove Session')
    Session.remove()

    return response
