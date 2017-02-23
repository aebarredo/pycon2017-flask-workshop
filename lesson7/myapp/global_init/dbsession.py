import sys

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from myapp.tables import Base


def setup_db_session(app):

    # conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
    #     app.config['DB_USER'],
    #     app.config['DB_PASSWORD'],
    #     app.config['DB_SERVER'],
    #     app.config['DB_SCHEMA'])

    # engine = create_engine(conn_str, pool_recycle=3600, pool_size=50, max_overflow=30)

    engine = create_engine('sqlite:///db/database.db')

    # try:
    #     connection = engine.connect()
    # except TimeoutError:
    #     print("DB timeout error")
    #     sys.exit(1)
    # except OperationalError:
    #     print("DB OperationalError")
    #     sys.exit(1)

    Session = scoped_session(sessionmaker(bind=engine))

    Base.metadata.create_all(engine)

    # table_names = []
    # for subclass in Base.__subclasses__():
    #     table_names.append(subclass.__tablename__)

    # print('Tables ' + str(table_names))
    # missingtable = False

    # for table_name in table_names:
    #     if engine.dialect.has_table(connection, table_name) is False:
    #         missingtable = True
    #         break

    # if missingtable is True:
    #     print("Incomplete tables. Creating tables")
    #     Base.metadata.create_all(engine)
    #     print("Tables created")

    return Session
