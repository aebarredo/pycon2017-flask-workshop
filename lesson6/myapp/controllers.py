from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from myapp.global_init import Session
from .models import Info

info_fields = {
    'info_id': fields.Integer(attribute='id'),
    'info_text': fields.String(attribute='infotext')
}


class InfoHandler(Resource):
    """ Field marshalling http://flask-restful-cn.readthedocs.io/en/0.3.5/fields.html
    """
    def __init__(self):
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    # def __del__(self):
    #     pass
        
    def post(self):
        retval = {}
        retval['status'] = 'SUCCESS'

        self.__reqparse.add_argument('text', type=str, required=True)
        args = self.__reqparse.parse_args()

        info = Info(self.__session)
        info.save_info(args['text'])

        retval['message'] = 'Info saved'

        return retval, 200

    # @marshal_with(info_fields, envelope='data')
    def get(self, info_id=None):
        info = Info(self.__session)

        info_details = info.get_info(info_id)

        ret = {}
        ret['status'] = 'SUCCESS'
        ret['data'] = marshal(info_details, info_fields)

        # return info_details, 200
        return ret, 200
