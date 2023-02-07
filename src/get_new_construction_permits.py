import os
from datetime import date
import requests
from dotenv import load_dotenv
import pandas as pd
from config import get_connection

load_dotenv()
API_KEY = os.getenv("PORTLAND_MAPS_API_KEY")


portland_maps_permits_url = "https://www.portlandmaps.com/api/permit/"

query = {
    "api_key": API_KEY,
    "search_type_Id": 8,
    "date_from": "02/06/2023",
    "date_to": date.today().strftime("%m-%d-%Y"),
    "download": 1,
}


if __name__ == "__main__":
    response = requests.get(portland_maps_permits_url, params=query)
    df = pd.DataFrame(response.json()["results"])

    engine = get_connection()

    # write permits to db
    df.to_sql(
        name="portland_new_construction_permits",
        con=engine,
        if_exists="append",
        index=False,
    )

    print("Permits succesfully added to database")
