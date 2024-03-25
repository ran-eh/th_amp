#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import os
import pandas as pd
# import psycopg
import requests
from sqlalchemy import create_engine, DateTime


# In[2]:


os.environ["PG_HOST"] = "db"
os.environ["PG_DATABASE"] = "weather"
os.environ["PG_USER"] = "postgres"
os.environ["PG_PASSWORD"] = "postgres"
os.environ["API_KEY"] = "MD8gOfRQx4yZ0lS8CfXv6OkVtBLCIdw8"



# In[3]:


host = os.environ["PG_HOST"]
db = os.environ["PG_DATABASE"]
user = os.environ["PG_USER"]
pw = os.environ["PG_PASSWORD"]
api_key = os.environ["API_KEY"]


# In[4]:


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
locations_df = locations_df.head(2)
display(locations_df)


# In[5]:


connect = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
engine = create_engine(connect)
locations_df.to_sql(
    'locations', 
    con=engine, 
    index=False, 
    if_exists='replace'
)


# In[15]:


for ix, row in locations_df.iterrows():
    lat = str(row["lat"])
    lon = str(row["lon"])
    if_exists = 'replace' if ix == 0 else 'append'

    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}%2C%20{lon}&units=metric&apikey={api_key}"
    
    headers = {"accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    df = pd.json_normalize(response.json()["data"])
    df.insert(0, 'lat', lat)
    df.insert(1, 'lon', lon)
    display(df)

    
    df.to_sql(
        'realtime', 
        con=engine, 
        index=False, 
        if_exists=if_exists
    )
    print("to_sql() done (sqlalchemy)")

    url = "https://api.tomorrow.io/v4/timelines?apikey=" + api_key
    
    payload = {
        "location": f"{lat},{lon}", 
        "fields": ["temperature", "windSpeed"],
        "units": "metric",
        "timesteps": ["1h"],
        "startTime": "nowMinus1d",
        "endTime": "nowPlus5d"
    }
    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip",
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    timelines = response_json["data"]["timelines"]
    timeline = timelines[0]
    intervals = timeline["intervals"]
    df = pd.DataFrame(intervals)
    print(df)
    df = pd.json_normalize(intervals)
    print(df)
    df.insert(0, 'lat', lat)
    df.insert(1, 'lon', lon)
    df

    df.to_sql(
        'timeline', 
        con=engine, 
        index=False, 
        if_exists=if_exists,
        dtype={"startTime": DateTime()}
    )
    print("to_sql() done (sqlalchemy)")
    
    # url = "https://api.tomorrow.io/v4/weather/realtime?location=42.3478%2C%20-71.0466&units=metric&apikey" + api_key
    
    # json_str = json.dumps(response_json["data"]["timelines"], indent=2)
    
    # print(json_str)
    # print(response.json())


# In[ ]:




