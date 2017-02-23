import datetime
import uuid

from myapp.tables import T_Customer

# Bug bounty

class Customer(object):
    def __init__(self, session):
        self.__session = session
        self.__uuid = None

    def __json(self, row):
        retval = {}

        ad = row.as_dict()
        for k in ad:

            if type(ad[k]) is datetime.datetime:

                ad[k] = ad[k].isoformat() + 'Z'

            retval[k] = ad[k]

        return retval

    def get(self, uuid=None):
        ret = []

        if uuid is None:
            customer_list = self.__session.query(T_Customer).filter_by(active=True).all()
        else:
            customer_list = self.__session.query(T_Customer).filter_by(active=True, uuid=uuid).all()

        for c in customer_list:
            ret.append(self.__json(c))

        return ret

    def add(self, args):
        customer_uuid = None
        customer = self.__session.query(T_Customer).filter_by(active=True,
                                                              firstname=args['firstname'],
                                                              lastname=args['lastname'],
                                                              middlename=args['middlename']).first()

        if customer is not None:
            customer_uuid = customer.uuid
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
