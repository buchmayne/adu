from os.path import expanduser
import requests
import pandas as pd
import geopandas as gpd
from shapely import Point, set_srid

portland_maps_url = "https://www.portlandmaps.com/api/suggest/"
meters_in_mile = 1609.34
example_address = "3115 SE Franklin St"


df = pd.read_csv(expanduser("~/Downloads/clean_adu_listings_202304261535.csv"))
gdf = (
    gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"], crs=4269)
    )
    .loc[lambda df_: df_.groupby(["zpid"])["days_on_market"].idxmax()]
    .to_crs(3857)
)


def get_price_of_closest_adu(address, gdf):
    query = {
        "api_key": "B923B3291E6B0DFE1BA426E8C40FA541",
        "query": address,
    }

    response = requests.get(portland_maps_url, params=query)
    data = response.json()
    address_location = set_srid(
        Point(
            data["candidates"][0]["location"]["x"],
            data["candidates"][0]["location"]["y"],
        ),
        3857,
    )

    return (
        gdf.assign(
            distance=lambda df_: address_location.distance(df_["geometry"])
            / meters_in_mile
        )
        .loc[lambda df_: df_["distance"] == df_["distance"].min(), "price"]
        .squeeze()
    )


if __name__ == "__main__":
    print(get_price_of_closest_adu(example_address, gdf))
