import os
from configparser import ConfigParser
from sqlalchemy.engine import URL, create_engine

absolute_path = os.path.dirname(__file__)
relative_path = "../../database.ini"
full_path = os.path.normpath(os.path.join(absolute_path, relative_path))


def config(filename=full_path, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


def get_connection():
    db = config()
    url_object = URL.create(
        drivername="postgresql+psycopg2",
        username=db["user"],
        password=db["password"],
        host=db["host"],
        database=db["database"],
    )
    return create_engine(url_object)
