import datetime
import uuid
import random
import string

from myapp.tables import T_Order, T_OrderDetails, T_Customer

# Bug bounty

class Order(object):
    def __init__(self, session):
        self.__session = session
        self.__uuid = None
        self.__error = ''

    def __json(self, row):
        retval = {}

        ad = row.as_dict()
        for k in ad:

            if type(ad[k]) is datetime.datetime:

                ad[k] = ad[k].isoformat() + 'Z'

            retval[k] = ad[k]

        return retval

    def __id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

    def get_error(self):
        return self.__error

    def get(self, ref_code=None):
        ret = []

        if ref_code is None:
            order_list = self.__session.query(T_Order).filter_by(active=True).all()
        else:
            order_list = self.__session.query(T_Order).filter_by(active=True, ref_code=ref_code).all()

        for order in order_list:
            ret.append(self.__json(order))

        return ret

    def create(self, args):
        customer_uuid = args['customer_uuid']

        customer = self.__session.query(T_Customer).filter_by(active=True, uuid=customer_uuid).first()
        if customer is None:
            ref_code = None
            self.__error = 'Invalid customer UUID'
        else:
            ref_code = self.__id_generator(12, '0123456789PyCon2017WritingRESTfulAPIsUsingFlask')
            order = T_Order(customer_id=customer.id,
                            ref_code=ref_code,
                            description=args['order_description'])

            self.__session.add(order)
            self.__session.commit()

        return ref_code

