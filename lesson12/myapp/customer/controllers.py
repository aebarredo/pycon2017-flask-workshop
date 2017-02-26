import time

from flask_restful_swagger_2 import swagger

from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from myapp.global_init import Session, limiter, logger, celery

from .models import Customer


customer_fields = {
    'uuid': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'middlename': fields.String,
    'uri': fields.Url('customer_by_uuid'),
    'orders': fields.Url('customer_orders'),
    'active': fields.Boolean
}

status_fields = {
    'status': fields.String,
    'uuid': fields.String,
    'message': fields.String,
    'uri': fields.Url('customer_by_uuid')
}


class CustomerUuidHandler(Resource):
    decorators = [limiter.limit("60/minute;1/second", methods=['GET'])]

    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    @swagger.doc({'description': 'Retrieve specific customer by UUID',
                  'summary': 'Get specific customer',
                  'tags': ['customer'],
                  'parameters': [
                  {
                      "type": "string",
                      "name": "Authorization",
                      "in": "header",
                      "required": False},
                  {
                      "type": "string",
                      "name": "uuid",
                      "in": "path",
                      "required": True},
                  {
                      "type": "string",
                      "name": "x-some-key",
                      "in": "header",
                      "required": False}],
                  'responses':
                  {
                      '200': {'description': 'Requested operation was successful'},
                      '401': {'description': 'Invalid credentials'}
                  }})
    def get(self, uuid):
        http_stat = 200

        customers = Customer(self.__session)
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

    @swagger.doc({'description': 'Overwrite existing customer details',
                  'summary': 'Overwrite customer',
                  'tags': ['customer'],
                  'parameters': [
                  {
                      "type": "string",
                      "name": "Authorization",
                      "in": "header",
                      "required": False},
                  {
                      "type": "string",
                      "name": "body",
                      "in": "body",
                      "schema": {},
                      "required": True},
                  {
                      "type": "string",
                      "name": "uuid",
                      "in": "path",
                      "required": True}],
                  'responses':
                  {
                      '200': {'description': 'Requested operation was successful'},
                      '401': {'description': 'Invalid credentials'}
                  }})
    def put(self, uuid):
        http_stat = 200

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

    @swagger.doc({'description': 'Update existing customer details',
                  'summary': 'Update customer',
                  'tags': ['customer'],
                  'parameters': [
                  {
                      "type": "string",
                      "name": "Authorization",
                      "in": "header",
                      "required": False},
                  {
                      "type": "string",
                      "name": "body",
                      "in": "body",
                      "schema": {},
                      "required": True},
                  {
                      "type": "string",
                      "name": "uuid",
                      "in": "path",
                      "required": True}],
                  'responses':
                  {
                      '200': {'description': 'Requested operation was successful'},
                      '401': {'description': 'Invalid credentials'}
                  }})
    def patch(self, uuid):
        http_stat = 200

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


class CustomerHandler(Resource):
    decorators = [limiter.limit("60/minute;1/second", methods=['GET'])]

    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    @swagger.doc({'description': 'Retrieve all customers',
                  'summary': 'Get all customers',
                  'tags': ['customer'],
                  'parameters': [
                  {
                      "type": "string",
                      "name": "Authorization",
                      "in": "header",
                      "required": False},
                  {
                      "type": "string",
                      "name": "sort",
                      "in": "query",
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
    def get(self):
        http_stat = 200

        self.__reqparse.add_argument('sort', type=str, default='lastname')
        args = self.__reqparse.parse_args()

        logger.debug(args)

        customers = Customer(self.__session, args)
        customer_list = customers.get()

        ret = {}
        if customer_list is not None:
            ret['status'] = 'SUCCESS'
            ret['customer'] = marshal(customer_list, customer_fields)
        else:
            ret['status'] = 'FAIL'
            ret['message'] = 'Invalid customer UUID'
            http_stat = 400

        return ret, http_stat

    @swagger.doc({'description': 'Create a new customer',
                  'summary': 'Create customer',
                  'tags': ['customer'],
                  'parameters': [
                  {
                      "type": "string",
                      "name": "body",
                      "in": "body",
                      "schema": {},
                      "required": True}],
                  'responses':
                  {
                      '200': {'description': 'Requested operation was successful'},
                      '401': {'description': 'Invalid credentials'}
                  }})
    def post(self):
        http_stat = 200

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

        logger.debug('Call some long running task')
        task_result = some_long_running_task.delay()
        # task_result.wait()

        return ret, http_stat

    def options(self):
        return 200, {}, {'Allow': 'GET,POST'}

order_fields = {
    'description': fields.String,
    'lastupdate': fields.String,
    'createdate': fields.String,
    'ref_code': fields.String,
    'uri': fields.Url('orders_single'),
    'active': fields.Boolean
}


@celery.task()
def some_long_running_task():
    logger.debug('Some long running task will executed')
    time.sleep(10)
    logger.debug('Long running done')
    return


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

