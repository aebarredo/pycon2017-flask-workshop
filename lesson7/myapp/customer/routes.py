from .controllers import *

# Designing RESTful api routes: http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
# Singular vs plural: http://stackoverflow.com/questions/6845772/rest-uri-convention-singular-or-plural-name-of-resource-while-creating-it


def customer_routes(api):

    api.add_resource(CustomerHandler, '/v1/customers', endpoint='customers_all')
    api.add_resource(CustomerHandler, '/v1/customers/<uuid>', endpoint='customer_single')

    return
