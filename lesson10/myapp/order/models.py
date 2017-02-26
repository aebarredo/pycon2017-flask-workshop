import datetime
import uuid
import random
import string

from myapp.global_init import logger
from myapp.tables import T_Order, T_OrderDetails, T_Customer

type_mapping = {'int': int, 'str': str, 'float': float}


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
            order_dict = self.__json(order)

            if ref_code is not None:
                orderdetail_dict = {}

                for detail in order.orderdetails:
                    detail_dict = self.__json(detail)
                    logger.debug(detail_dict)

                    fieldcode = detail_dict['fieldcode']
                    fieldvalue = detail_dict['fieldvalue']
                    fieldtype = detail_dict['fieldtype']

                    actual_value = type_mapping[fieldtype](fieldvalue)

                    orderdetail_dict[fieldcode] = actual_value

                order_dict['order_details'] = orderdetail_dict

            ret.append(order_dict)

            logger.debug(ret)

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

            for item, value in args['order_details'].items():
                detail = T_OrderDetails(order=order,
                                        fieldcode=item,
                                        fieldvalue=str(value),
                                        fieldtype=type(value).__name__)

            self.__session.add(order)
            self.__session.add(detail)
            self.__session.commit()

        return ref_code
