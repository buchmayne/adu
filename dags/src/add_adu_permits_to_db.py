from datetime import date
import pandas as pd


def extract_adu_from_permits(df):
    """
    Return subset of permits that are most likely to be ADUs

    Parameters
    ----------
    df : pd.DataFrame
        Residential permits (both new construction and alteration)

    Returns
    -------
    pd.DataFrame
        Subset of permits most likely to be ADUs, based on assumptions
    """
    return (
        df.loc[~df["new_units"].isnull()]  # 1. Permit has to be for new unit
        .loc[
            lambda df_: df_["status"] == "Final"
        ]  # 2. Final permits (not tracking submissions)
        .loc[
            lambda df_: df_["description"].str.contains(
                " ADU | ACCESSORY DWELLING UNIT", na=False, case=False
            )
        ]  # 3. ADU or ACCESSORY DWELLING UNIT in the description
        .loc[
            lambda df_: df_["total_sqft"] <= 1_000
        ]  # 4. Has to be roughly ADU size, giving some flexibility as 800 sqft is max
        .assign(
            final_permit_date=lambda df_: pd.to_datetime(df_["final"]).dt.date
        )  # format final permit date as date
    )


def add_adu_permits_to_db(**kwargs):
    """
    Query db for new permits, then if new permits exist subset data on ADUs and add to database

    """
    con = kwargs["engine"]
    new_construction_permits = pd.read_sql(
        f"""select * from portland_new_construction_permits where final>='{date.today().strftime("%Y-%m-%d")}';""",
        con=con,
    )

    alteration_permits = pd.read_sql(
        f"""select * from portland_alteration_permits where final>='{date.today().strftime("%Y-%m-%d")}';""",
        con=con,
    )

    permits = pd.concat([new_construction_permits, alteration_permits], axis=0)

    if len(permits) > 0:
        # write permits to db
        (
            permits.pipe(extract_adu_from_permits).to_sql(
                name="portland_adu_permits",
                con=con,
                if_exists="append",
                index=False,
            )
        )
        print(f"Permits succesfully added to portland_adu_permits table")
    else:
        print(f"No new permits to add to portland_adu_permits table")


if __name__ == "__main__":
    add_adu_permits_to_db()
