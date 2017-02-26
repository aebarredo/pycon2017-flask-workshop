import datetime
import uuid

from sqlalchemy import or_, and_, func, desc, asc

from myapp.global_init import logger
from myapp.tables import T_Customer


class Customer(object):
    def __init__(self, session, args=None):
        self.__session = session
        self.__uuid = None
        self.__this_customer = None
        self.__args = args

    def __json(self, row):
        retval = {}

        ad = row.as_dict()
        for k in ad:

            if type(ad[k]) is datetime.datetime:

                ad[k] = ad[k].isoformat() + 'Z'

            retval[k] = ad[k]

        return retval

    def __build_sort_param(self):
        sort_param = []

        # comma delimited sort keys
        sort_keys = self.__args.get('sort', None)

        sort_list = []
        if sort_keys is not None:
            sort_list = sort_keys.split(',')

        for key in sort_list:
            if '-' in key:
                key = key.replace('-', '')
                sort = desc(getattr(T_Customer, key.strip()))
            else:
                sort = asc(getattr(T_Customer, key.strip()))

            sort_param.append(sort)

        return sort_param

    def get(self, uuid=None):
        ret = []

        if uuid is None:
            sort_param = self.__build_sort_param()
            customer_list = self.__session.query(T_Customer).order_by(*sort_param).filter_by(active=True).all()

        else:
            customer_list = self.__session.query(T_Customer).filter_by(active=True, uuid=uuid).all()

            if len(customer_list) == 0:
                customer_list = None
            else:
                self.__this_customer = customer_list[0]

        if customer_list is not None:
            for c in customer_list:
                ret.append(self.__json(c))
        else:
            ret = None

        return ret

    def add(self, args):
        customer_uuid = None
        customer = self.__session.query(T_Customer).filter_by(active=True,
                                                              firstname=args['firstname'],
                                                              lastname=args['lastname'],
                                                              middlename=args['middlename']).first()

        if customer is not None:
            customer_uuid = None

        else:

            customer_uuid = str(uuid.uuid4())
            new_customer = T_Customer(uuid=customer_uuid,
                                      firstname=args['firstname'],
                                      lastname=args['lastname'],
                                      middlename=args['middlename'])

            self.__session.add(new_customer)
            self.__session.commit()

        return customer_uuid

    def replace(self, customer_uuid, args):
        retval = False

        customer = self.__session.query(T_Customer)\
                                 .filter_by(active=True, uuid=customer_uuid)\
                                 .with_for_update(nowait=True, of=T_Customer)\
                                 .first()

        if customer is not None:
            customer.firstname = args['firstname']
            customer.lastname = args['lastname']
            customer.middlename = args['middlename']

            self.__session.commit()

            retval = True

        return retval

    def edit(self, customer_uuid, args):
        retval = False

        customer = self.__session.query(T_Customer)\
                                 .filter_by(active=True, uuid=customer_uuid)\
                                 .with_for_update(nowait=True, of=T_Customer)\
                                 .first()

        if customer is not None:

            for key, value in args.items():
                if value == '':
                    continue

                setattr(customer, key, value)

            self.__session.commit()

            retval = True

        return retval

    def get_orders(self):
        retval = []

        if self.__this_customer is not None:
            for order in self.__this_customer.orders:
                retval.append(self.__json(order))   

        return retval
