import json

from flask import Flask, request
from flask_restful import Api

from myapp.global_init import app, Session
from myapp.customer.routes import customer_routes
from myapp.order.routes import order_routes


api = Api(app)

customer_routes(api)
order_routes(api)


@app.after_request
def after_request_sequence(response):
    #logger.debug('After request, remove Session')
    Session.remove()

    return response
