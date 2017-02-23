import datetime

from sqlalchemy import Column, Integer, Sequence, String, DateTime, Boolean, Float, TEXT, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class T_Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)

    firstname = Column(String(100))
    lastname = Column(String(100))
    middlename = Column(String(100))

    uuid = Column(String(36))

    active = Column(Boolean, default=True)
    createdate = Column(DateTime, default=func.now())
    lastupdate = Column(DateTime, default=func.now(), onupdate=func.now())

    orders = relationship('T_Order', backref='customer')

    def as_dict(self):
        return ({c.name: getattr(self, c.name) for c in self.__table__.columns})


class T_Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)

    # Basic relationship patterns:
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-many
    customer_id = Column(Integer, ForeignKey(T_Customer.__tablename__+'.id'))

    ref_code = Column(String(12))
    description = Column(TEXT)

    active = Column(Boolean, default=True)
    createdate = Column(DateTime, default=func.now())
    lastupdate = Column(DateTime, default=func.now(), onupdate=func.now())

    # Notes on backref:
    # http://docs.sqlalchemy.org/en/latest/orm/backref.html
    orderdetails = relationship('T_OrderDetails', backref='order')

    def as_dict(self):
        return ({c.name: getattr(self, c.name) for c in self.__table__.columns})


class T_OrderDetails(Base):

    __tablename__ = 'orderdetails'
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)

    order_id = Column(Integer, ForeignKey(T_Order.__tablename__+'.id'))

    fieldcode = Column(String(20), nullable=False)
    fieldvalue = Column(String(255), nullable=True)
    fieldtype = Column(String(20), nullable=False, default='STRING')

    createdate = Column(DateTime, default=func.now())
    lastupdate = Column(DateTime, default=func.now(), onupdate=func.now())
    active = Column(Boolean, default=True)

    def as_dict(self):
        return ({c.name: getattr(self, c.name) for c in self.__table__.columns})
