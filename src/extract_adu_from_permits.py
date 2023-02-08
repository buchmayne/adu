from datetime import date
import pandas as pd
from config import get_connection


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
    )


if __name__ == "__main__":
    engine = get_connection()

    new_construction_permits = pd.read_sql(
        "select * from portland_new_construction_permits;", con=engine
    )
    alteration_permits = pd.read_sql(
        "select * from portland_alteration_permits;", con=engine
    )
    new_construction_adu_permits = extract_adu_from_permits(new_construction_permits)
    alteration_adu_permits = extract_adu_from_permits(alteration_permits)

    adu_permits = pd.concat(
        [new_construction_adu_permits, alteration_adu_permits], axis=0
    )

    adu_permits.to_sql(
        name="portland_adu_permits",
        con=engine,
        if_exists="append",
        index=False,
    )
