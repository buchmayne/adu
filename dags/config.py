from sqlalchemy.engine import URL, create_engine
from airflow.models import Variable

PORTLAND_MAPS_API_KEY = Variable.get("PORTLAND_MAPS_API_KEY")
db = Variable.get("postgres_vals", deserialize_json=True)


def get_connection():
    url_object = URL.create(
        drivername="postgresql+psycopg2",
        username=db["username"],
        password=db["password"],
        host=db["host"],
        database=db["database"],
    )
    return create_engine(url_object)
