import os
from datetime import date
import requests
from dotenv import load_dotenv
import pandas as pd
from config import get_connection

load_dotenv()
API_KEY = os.getenv("PORTLAND_MAPS_API_KEY")


portland_maps_permits_url = "https://www.portlandmaps.com/api/permit/"

new_construction_query = {
    "api_key": API_KEY,
    "search_type_Id": 8,
    "date_from": "02/06/2023",
    "date_to": date.today().strftime("%m-%d-%Y"),
    "download": 1,
}

alteration_query = {
    "api_key": API_KEY,
    "search_type_Id": 5,
    "date_from": "02/07/2023",
    "date_to": date.today().strftime("%m-%d-%Y"),
    "download": 1,
}


def add_permits_to_db(query, tbl_name, con):
    """
    Get permit data from portlandmaps.com and write results to database

    Parameters
    ----------
    query : dict
        Parameters to pass to the get request
    tbl_name : str
        Name of table in database to append results to
    con : sqlalchemy.engine.Engine
        Database connection object

    """
    response = requests.get(portland_maps_permits_url, params=query)
    df = pd.DataFrame(response.json()["results"])

    if len(df) > 0:
        # write permits to db
        df.to_sql(
            name=tbl_name,
            con=con,
            if_exists="append",
            index=False,
        )
        print(f"Permits succesfully added to {tbl_name} table")
    else:
        print(f"No new permits to add to {tbl_name} table")


def get_permits():
    """
    Add new permits for both new construction and alterations
    """
    # CONNECT TO DB
    engine = get_connection()

    # NEW CONSTRUCTION PERMITS
    add_permits_to_db(
        query=new_construction_query,
        tbl_name="portland_new_construction_permits",
        con=engine,
    )
    # ALTERATION PERMITS
    add_permits_to_db(
        query=alteration_query,
        tbl_name="portland_alteration_permits",
        con=engine,
    )


if __name__ == "__main__":
    get_permits()
