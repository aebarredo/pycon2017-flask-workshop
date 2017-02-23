import datetime

from sqlalchemy import Column, Integer, Sequence, String, DateTime, Boolean, Float, TEXT, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class T_InfoTable(Base):
    __tablename__ = 'infotable'

    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)

    infotext = Column(String(100))

    active = Column(Boolean, default=True)
    createdate = Column(DateTime, default=func.now())
    lastupdate = Column(DateTime, default=func.now(), onupdate=func.now())

    def as_dict(self):
        return ({c.name: getattr(self, c.name) for c in self.__table__.columns})

