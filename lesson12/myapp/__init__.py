import json

from flask import Flask, request, url_for
# from flask_restful import Api, Resource
from flask_restful import Resource
from flask_restful_swagger_2 import Api
from flask_cors import CORS, cross_origin

from myapp.global_init import app, Session, logger, celery
from myapp.customer.routes import customer_routes
from myapp.order.routes import order_routes


class ApiRoot(Resource):
    def __init__(self):
        pass

    def get(self):
        retval = {
            'version': 'Version 2',
            'description': 'myapp sample API',
            'endpoints': {
                'customers': url_for('customers'),
                'orders': url_for('orders_all')
            }
        }

        return retval


CORS(app)
api = Api(app,
          api_version='v2.0',
          api_spec_url='/specs',
          title='myapp API',
          description='Workshop: Writing RESTful APIs with Flask (PyconPH 2017)')


customer_routes(api)
order_routes(api)

api.add_resource(ApiRoot, '/', endpoint='api_root')

logger.debug('myapp is up (Lesson 12)')


@app.after_request
def after_request_sequence(response):
    Session.remove()

    return response
