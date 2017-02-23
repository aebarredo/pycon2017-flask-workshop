from flask_restful import Resource, reqparse
from myapp.global_init import Session
from .models import Info


class InfoHandler(Resource):
    def __init__(self):

        # Read: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        self.__session = Session()
        self.__reqparse = reqparse.RequestParser()

    def post(self):
        retval = {}
        retval['status'] = 'SUCCESS'

        self.__reqparse.add_argument('text', type=str, required=True)
        args = self.__reqparse.parse_args()

        info = Info(self.__session)
        info.save_info(args['text'])

        retval['message'] = 'Info saved'

        return retval, 200

    def get(self, info_id=None):
        info = Info(self.__session)

        info_details = info.get_info(info_id)

        retval = {}
        retval['status'] = 'SUCCESS'
        retval['info_details'] = info_details

        return retval, 200


