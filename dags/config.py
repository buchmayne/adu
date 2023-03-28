from configparser import ConfigParser
from sqlalchemy.engine import URL, create_engine


# def config():
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read("database.ini")

#     db = {}
#     if parser.has_section("postgresql"):
#         params = parser.items("postgresql")
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception(
#             "Section {0} not found in the {1} file".format("postgresql", "database.ini")
#         )

#     return db


def get_connection():
    url_object = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="password",
        host="adu_db_1",
        database="postgres",
    )
    return create_engine(url_object)


# NEED TO FIX THIS ONCE THIS IS WORKING
PORTLAND_MAPS_API_KEY = "B923B3291E6B0DFE1BA426E8C40FA541"
