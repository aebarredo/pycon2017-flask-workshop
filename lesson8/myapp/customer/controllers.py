from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from myapp.global_init import Session

from .models import Customer


customer_fields = {
    'uuid': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'middlename': fields.String,
    'active': fields.Boolean
}


class CustomerHandler(Resource):
    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    def get(self, uuid=None):

        customers = Customer(self.__session)
        customer_list = customers.get(uuid)

        ret = {}
        ret['status'] = 'SUCCESS'
        ret['customer'] = marshal(customer_list, customer_fields)

        return ret, 200

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

            ret = {'status': 'SUCCESS', 'uuid': uuid}

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
                ret = {'status': 'SUCCESS', 'message': 'Replaced'}

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
                ret = {'status': 'SUCCESS', 'message': 'Updated'}

        return ret, http_stat
