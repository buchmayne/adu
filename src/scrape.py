import requests
import json
import pandas as pd
from datetime import date
from config import get_connection

cookies = {
    "zguid": "24|%24d1ca2ccb-2f2f-4117-836a-69c85ce3ea50",
    "search": "6|1677820347791%7Crect%3D45.749318276578265%252C-122.45433810400391%252C45.360829953851024%252C-122.9370498959961%26rid%3D13373%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26att%3DADU%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26size%3D0-1000%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26excludeNullAvailabilityDates%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0913373%09%09%09%09%09%09",
    "G_ENABLED_IDPS": "google",
    "AWSALB": "IHQuiZXf2rtUwEu9xUZ2tzpAgWoevk7PsMrGOJd8RA6KH7tGa6TbUOCwYfIrvKqUaccw4XHm0y1N7La+/Srg5h88r1aG/PiY7RRqkOse+XA5dEGGcUITK5xFLlGz",
    "AWSALBCORS": "IHQuiZXf2rtUwEu9xUZ2tzpAgWoevk7PsMrGOJd8RA6KH7tGa6TbUOCwYfIrvKqUaccw4XHm0y1N7La+/Srg5h88r1aG/PiY7RRqkOse+XA5dEGGcUITK5xFLlGz",
    "JSESSIONID": "AA2ED08080A6844E1EAF80AF8B777D53",
    "zgsession": "1|1d53085e-4724-4c91-bd55-f49a9095e7bd",
    "g_state": '{"i_p":1675235332971,"i_l":1}',
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Connection": "keep-alive",
    # 'Cookie': 'zguid=24|%24d1ca2ccb-2f2f-4117-836a-69c85ce3ea50; search=6|1677820347791%7Crect%3D45.749318276578265%252C-122.45433810400391%252C45.360829953851024%252C-122.9370498959961%26rid%3D13373%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26att%3DADU%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26size%3D0-1000%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26excludeNullAvailabilityDates%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0913373%09%09%09%09%09%09; G_ENABLED_IDPS=google; AWSALB=IHQuiZXf2rtUwEu9xUZ2tzpAgWoevk7PsMrGOJd8RA6KH7tGa6TbUOCwYfIrvKqUaccw4XHm0y1N7La+/Srg5h88r1aG/PiY7RRqkOse+XA5dEGGcUITK5xFLlGz; AWSALBCORS=IHQuiZXf2rtUwEu9xUZ2tzpAgWoevk7PsMrGOJd8RA6KH7tGa6TbUOCwYfIrvKqUaccw4XHm0y1N7La+/Srg5h88r1aG/PiY7RRqkOse+XA5dEGGcUITK5xFLlGz; JSESSIONID=AA2ED08080A6844E1EAF80AF8B777D53; zgsession=1|1d53085e-4724-4c91-bd55-f49a9095e7bd; g_state={"i_p":1675235332971,"i_l":1}',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


def preprocess_listings_df(df):
    assert "hdpData" in df.columns
    assert "latLong" in df.columns
    assert "variableData" in df.columns
    assert "streetViewMetadataURL" in df.columns
    assert "streetViewURL" in df.columns
    return pd.concat([df, pd.json_normalize(df["latLong"])], axis=1).drop(
        [
            "latLong",
            "hdpData",
            "variableData",
            "streetViewMetadataURL",
            "streetViewURL",
        ],
        axis=1,
    )


if __name__ == "__main__":
    response = requests.get(
        "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.89138796972657%2C%22east%22%3A-122.50000003027344%2C%22south%22%3A45.360829953851024%2C%22north%22%3A45.749318276578265%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A13373%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22keywords%22%3A%7B%22value%22%3A%22ADU%22%7D%2C%22sqft%22%3A%7B%22max%22%3A1000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22]}&requestId=14",
        cookies=cookies,
        headers=headers,
    )

    list_results = response.json()["cat1"]["searchResults"]["listResults"]
    listings = pd.DataFrame(list_results)

    # add date to dataframe before writing to db
    listings["date_scraped"] = date.today()

    engine = get_connection()

    df = preprocess_listings_df(listings)

    # write listings to db
    df.to_sql(
        name="zillow_rental_listings", con=engine, if_exists="append", index=False
    )

    print("Listings succesfully added to database")
