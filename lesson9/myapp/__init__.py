import json

from flask import Flask, request, url_for
# from flask_restful import Api, Resource
from flask_restful import Resource
from flask_restful_swagger_2 import Api

from myapp.global_init import app, Session, logger
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
                'customers': url_for('customers_all'),
                'orders': url_for('orders_all')
            }
        }

        return retval


# api = Api(app)

api = Api(app,
          api_version='v2.0',
          api_spec_url='/specs',
          title='myapp API',
          description='Workshop: Writing RESTful APIs with Flask (PyconPH 2017)')

# More tips on writing RESTful APIs: http://www.restapitutorial.com/lessons/httpmethods.html
customer_routes(api)
order_routes(api)

api.add_resource(ApiRoot, '/', endpoint='api_root')

logger.debug('myapp is up')


@app.after_request
def after_request_sequence(response):
    Session.remove()

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
