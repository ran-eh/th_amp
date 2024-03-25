import numpy as np
import os
import pandas as pd
from sqlalchemy import create_engine, DateTime
import time

import api_calls as api


host = os.environ["PG_HOST"]
db = os.environ["PG_DATABASE"]
user = os.environ["PG_USER"]
pw = os.environ["PG_PASSWORD"]
api_key = os.environ["API_KEY"]

locations = np.array([
    ('25.8600','-97.4200'),
    ('25.9000','-97.5200'),
    ('25.9000','-97.4800'),
    ('25.9000','-97.4400'),
    ('25.9000','-97.4000'),
    ('25.9200','-97.3800'),
    ('25.9400','-97.5400'),
    ('25.9400','-97.5200'),
    ('25.9400','-97.4800'),
    ('25.9400','-97.4400'),
])

locations_df = pd.DataFrame.from_records(locations, columns=["lat", "lon"])
locations_df.insert(0, 'id', range(len(locations_df)))
# For debugging, uncomment line below to avoid hitting tomorrow.io free tear rate limit
locations_df = locations_df.head(2)
print(locations_df)

connect = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
engine = create_engine(connect)
locations_df.to_sql(
    'locations', 
    con=engine, 
    index=False, 
    if_exists='replace'
)


for ix, row in locations_df.iterrows():
    lat = str(row["lat"])
    lon = str(row["lon"])
    if_exists = 'replace' if ix == 0 else 'append'

    df = api.get_realtime(api_key, lat, lon)
    
    df.to_sql(
        'realtime', 
        con=engine, 
        index=False, 
        if_exists=if_exists
    )
    df = api.get_timelines(api_key, lat, lon)

    df.to_sql(
        'timeline', 
        con=engine, 
        index=False, 
        if_exists=if_exists,
        dtype={"startTime": DateTime()}
    )
    print("to_sql() done (sqlalchemy)")

    os.environ['IS_HEALTHY'] = 'YES'
    print(os.environ)
    
time.sleep(100000)


# In[ ]:




