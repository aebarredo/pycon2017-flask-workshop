import datetime

from .tables import T_InfoTable


class Info(object):
    def __init__(self, session):

        self.__session = session
        self.__info_details = None

    def __json(self, row):
        retval = {}

        ad = row.as_dict()
        for k in ad:

            if type(ad[k]) is datetime.datetime:

                ad[k] = ad[k].isoformat() + 'Z'

            retval[k] = ad[k]

        return retval

    def get_info(self, info_id=None):
        retval = []

        if info_id is None:
            info_details = self.__session.query(T_InfoTable).filter_by(active=True).all()
        else:
            info_details = self.__session.query(T_InfoTable).filter_by(id=info_id).all()

        if info_details is not None:
            for i in info_details:
                retval.append(self.__json(i))

        return retval

    def save_info(self, text):
        info = T_InfoTable(infotext=text)

        self.__session.add(info)
        self.__session.commit()

        return

    def del_info(self, info_id):
        pass

    def edit_info(self, info_id, info_text):
        pass
