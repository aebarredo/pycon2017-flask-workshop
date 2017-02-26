from .controllers import *


def order_routes(api):

    api.add_resource(OrderHandler, '/v2/orders', endpoint='orders_all')
    api.add_resource(OrderHandler, '/v2/orders/<ref_code>', endpoint='orders_single')

    return