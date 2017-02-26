from flask_restful_swagger_2 import swagger

from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from myapp.global_init import Session, limiter, logger

from .models import Customer


customer_fields = {
    'uuid': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'middlename': fields.String,
    'uri': fields.Url('customer_single'),
    'orders': fields.Url('customer_orders'),
    'active': fields.Boolean
}

status_fields = {
    'status': fields.String,
    'uuid': fields.String,
    'message': fields.String,
    'uri': fields.Url('customer_single')
}


class CustomerHandler(Resource):
    decorators = [limiter.limit("360/minute;60/second", methods=['GET'])]

    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    def get(self, uuid=None):
        http_stat = 200

        args = None
        if uuid is None:
            self.__reqparse.add_argument('sort', type=str, default='lastname')
            args = self.__reqparse.parse_args()

            logger.debug(args)

        customers = Customer(self.__session, args)
        customer_list = customers.get(uuid)

        ret = {}
        if customer_list is not None:
            ret['status'] = 'SUCCESS'
            ret['customer'] = marshal(customer_list, customer_fields)
        else:
            ret['status'] = 'FAIL'
            ret['message'] = 'Invalid customer UUID'
            http_stat = 400

        return ret, http_stat

    def post(self, uuid=None):
        http_stat = 200

        if uuid is not None:
            http_stat = 400
            ret = {'status': 'FAIL', 'message': 'Bad request'}
        else:
            self.__reqparse.add_argument('firstname', type=str, required=True)
            self.__reqparse.add_argument('lastname', type=str, required=True)
            self.__reqparse.add_argument('middlename', type=str, default='')

            args = self.__reqparse.parse_args()

            customer = Customer(self.__session)
            uuid = customer.add(args)

            if uuid is not None:
                ret = marshal({'status': 'SUCCESS', 'uuid': uuid, 'message': 'Resource added'}, status_fields)
            else:
                ret = {'status': 'FAILED', 'message': 'Duplicate Resource'}
                http_stat = 409

        return ret, http_stat

    def put(self, uuid=None):
        http_stat = 200

        if uuid is None:
            http_stat = 400
            ret = {'status': 'FAIL', 'message': 'Specify customer UUID'}
        else:
            self.__reqparse.add_argument('firstname', type=str, required=True)
            self.__reqparse.add_argument('lastname', type=str, required=True)
            self.__reqparse.add_argument('middlename', type=str, default='')

            args = self.__reqparse.parse_args()

            customer = Customer(self.__session)
            if customer.replace(uuid, args) is False:
                ret = {'status': 'FAIL', 'message': 'Invalid UUID'}
                http_stat = 400
            else:
                ret = marshal({'status': 'SUCCESS', 'message': 'Replaced', 'uuid': uuid}, status_fields)

        return ret, http_stat

    def patch(self, uuid=None):
        http_stat = 200

        if uuid is None:
            http_stat = 400
            ret = {'status': 'FAIL', 'message': 'Specify customer UUID'}
        else:
            self.__reqparse.add_argument('firstname', type=str, default='')
            self.__reqparse.add_argument('lastname', type=str, default='')
            self.__reqparse.add_argument('middlename', type=str, default='')

            args = self.__reqparse.parse_args()

            customer = Customer(self.__session)
            if customer.edit(uuid, args) is False:
                ret = {'status': 'FAIL', 'message': 'Invalid UUID'}
                http_stat = 400
            else:
                ret = marshal({'status': 'SUCCESS', 'message': 'Updated', 'uuid': uuid}, status_fields)

        return ret, http_stat


order_fields = {
    'description': fields.String,
    'lastupdate': fields.String,
    'createdate': fields.String,
    'ref_code': fields.String,
    'uri': fields.Url('orders_single'),
    'active': fields.Boolean
}


class CustomerOrderHandler(Resource):
    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    def get(self, uuid):
        retval = {}
        http_stat = 200

        customer = Customer(self.__session)
        customer_json = customer.get(uuid)

        if customer_json is not None:
            order_list = customer.get_orders()

            retval['order'] = marshal(order_list, order_fields)
            retval['customer'] = marshal(customer_json, customer_fields)
            retval['status'] = 'SUCCESS'
        else:
            retval['status'] = 'SUCCESS'
            retval['message'] = 'Invalid customer UUID'
            http_stat = 400

        return retval, http_stat
