import pandas as pd


def clean_adu_listings(listings_data):
    """
    Return subset of listings that are most likely to be ADUs

    Parameters
    ----------
    listings_data : pd.DataFrame
        transformed_zillow_rental_listings table

    Returns
    -------
    pd.DataFrame
        Subset of listings most likely to be ADUs, based on assumptions
    """
    return (
        listings_data.drop_duplicates()
        .sort_values(["zpid", "date_scraped"])
        .assign(
            days_on_market=lambda df_: df_.groupby(["zpid"])["date_scraped"].rank(
                method="first"
            )
        )
        .loc[
            lambda df_: (
                (df_["sqft"] <= 900)
                & (df_["address_street"].str.contains("UNIT B|#B|SUITE B"))
            )
        ]
    )


def add_clean_adu_listings_to_db(**kwargs):
    """
    Query db for ADU listings, then preprocess listings data and write to db

    """
    con = kwargs["engine"]

    listings = pd.read_sql(
        """select * from transformed_zillow_rental_listings;""",
        con=con,
    )

    # write clean listings to db
    (
        listings.pipe(clean_adu_listings).to_sql(
            name="clean_adu_listings",
            con=con,
            if_exists="replace",
            index=False,
        )
    )
    print(f"Listings succesfully added to clean_adu_listings table")


if __name__ == "__main__":
    add_clean_adu_listings_to_db()
