from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from myapp.global_init import Session

from .models import Order


class OrderHandler(Resource):
    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    def get(self, ref_code=None):
        ret = {}

        orders = Order(self.__session)
        order_list = orders.get(ref_code)

        ret['status'] = 'SUCCESS'
        ret['order'] = order_list

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

            args = self.__reqparse.parse_args()

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

    