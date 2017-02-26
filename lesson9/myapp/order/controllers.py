from flask_restful_swagger_2 import swagger

from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from myapp.global_init import Session, logger

from .models import Order

order_detail_fields = {
    'size': fields.String,
    'weight': fields.Raw,
    'amount': fields.Raw
}

order_fields = {
    'description': fields.String,
    'lastupdate': fields.String,
    'createdate': fields.String,
    'ref_code': fields.String,
    'active': fields.Boolean,
    'uri': fields.Url('orders_single'),
    'order_details': fields.Nested(order_detail_fields)
}


class OrderHandler(Resource):
    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    @swagger.doc({'description': 'Retrieve list of orders or a specific order given a reference number',
                      'summary': 'Get orders',
                      'tags': ['orders'],
                      'parameters': [
                      {
                          "type": "string",
                          "name": "Authorization",
                          "in": "header",
                          "required": False},
                      {
                          "type": "string",
                          "name": "ref_code",
                          "in": "path",
                          "required": False},
                      {
                          "type": "string",
                          "name": "some-header",
                          "in": "header",
                          "required": False}],
                      'responses':
                      {
                          '200': {'description': 'Requested operation was successful'},
                          '401': {'description': 'Invalid credentials'}
                      }})

    def get(self, ref_code=None):
        ret = {}

        orders = Order(self.__session)
        order_list = orders.get(ref_code)

        ret['status'] = 'SUCCESS'
        ret['order'] = marshal(order_list, order_fields)

        return ret, 200



    def post(self, ref_code=None):

        ret = {}
        http_stat = 200

        if ref_code is not None:
            ret['status'] = 'FAIL'
            ret['message'] = 'Invalid request'
            http_stat = 400
        else:
            # parse request
            self.__reqparse.add_argument('customer_uuid', type=str, required=True)
            self.__reqparse.add_argument('order_description', type=str, required=True)
            self.__reqparse.add_argument('order_details', type=dict, location='json', default=[])

            args = self.__reqparse.parse_args()

            logger.debug(args)

            order = Order(self.__session)
            new_ref_code = order.create(args)

            if new_ref_code is None:
                ret['status'] = 'FAIL'
                ret['message'] = order.get_error()
                http_stat = 400
            else:
                ret['status'] = 'SUCCESS'
                ret['ref_no'] = new_ref_code

        return ret, http_stat
