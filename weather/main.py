import os
from sqlalchemy import DateTime
import time

from api_calls import WeatherAPI
from get_locations import get_locations
from db import DB


host = os.environ["PG_HOST"]
db = os.environ["PG_DATABASE"]
user = os.environ["PG_USER"]
pw = os.environ["PG_PASSWORD"]
api_key = os.environ["API_KEY"]

locations_df = get_locations()
print(locations_df)

db = DB(host, db, user, pw)
api = WeatherAPI(api_key)
for ix, row in locations_df.iterrows():
    lat = str(row["lat"])
    lon = str(row["lon"])
    if_exists = 'replace' if ix == 0 else 'append'

    df = api.get_realtime(lat, lon)    
    db.to_table(df, 'realtime', if_exists, dtype={"time": DateTime()})

    df = api.get_timelines(lat, lon)
    db.to_table(df, 'timeline', if_exists, dtype={"startTime": DateTime()})
time.sleep(100000)


# In[ ]:




