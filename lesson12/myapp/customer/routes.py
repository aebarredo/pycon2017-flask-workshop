from .controllers import *


def customer_routes(api):

    api.add_resource(CustomerHandler, '/v2/customers', endpoint='customers')
    api.add_resource(CustomerUuidHandler, '/v2/customers/<uuid>', endpoint='customer_by_uuid')
    api.add_resource(CustomerOrderHandler, '/v2/customers/<uuid>/orders', endpoint='customer_orders')

    return
