from .controllers import *

# Designing RESTful api routes: http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
# Singular vs plural: http://stackoverflow.com/questions/6845772/rest-uri-convention-singular-or-plural-name-of-resource-while-creating-it
# Cheatsheet: https://github.com/RestCheatSheet/api-cheat-sheet#api-design-cheat-sheet
# http://mark-kirby.co.uk/2013/creating-a-true-rest-api/
# http://restfulapi.net/rest-architectural-constraints/
# https://www.mobomo.com/2010/04/rest-isnt-what-you-think-it-is/

def customer_routes(api):

    api.add_resource(CustomerHandler, '/v2/customers', endpoint='customers_all')
    api.add_resource(CustomerHandler, '/v2/customers/<uuid>', endpoint='customer_single')
    api.add_resource(CustomerOrderHandler, '/v2/customers/<uuid>/orders', endpoint='customer_orders')

    return
