from flask_restful import Resource, reqparse


class InfoHandler(Resource):
    def __init__(self):
        pass

    def post(self):
        retval = {}
        retval['status'] = 'SUCCESS'
        retval['method'] = 'POST'

        return retval, 200

    def get(self):
        retval = {}
        retval['status'] = 'SUCCESS'
        retval['method'] = 'GET'

        return retval, 200


class InfoHandlerV2(Resource):
    def __init__(self):
        pass

    def post(self):
        retval = {}
        retval['status'] = 'SUCCESS'

        return retval, 200

    def get(self):
        retval = {}
        retval['status'] = 'SUCCESS'

        return retval, 200
