import pandas as pd
import requests
from sqlalchemy import create_engine

param_dic = {
    "host"      : "db",
    "database"  : "weather",
    "user"      : "postgres",
    "password"  : "postgres"
}


connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
    param_dic['user'],
    param_dic['password'],
    param_dic['host'],
    param_dic['database']
)

engine = create_engine(connect)


url = "https://api.tomorrow.io/v4/timelines?apikey=MD8gOfRQx4yZ0lS8CfXv6OkVtBLCIdw8"

payload = {
    "location": "42.3478, -71.0466",
    "fields": ["temperature", "windSpeed", "windDirection"],
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
df.to_sql(
    'timeline', 
    con=engine, 
    index=False, 
    if_exists='replace'
)
print("to_sql() done (sqlalchemy)")

url = "https://api.tomorrow.io/v4/weather/realtime?location=42.3478%2C%20-71.0466&units=metric&apikey=MD8gOfRQx4yZ0lS8CfXv6OkVtBLCIdw8"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
values = [response.json()["data"]]

# df = pd.DataFrame(values)
df = pd.json_normalize(values)


df.to_sql(
    'realtime', 
    con=engine, 
    index=False, 
    if_exists='replace'
)
print("to_sql() done (sqlalchemy)")

# json_str = json.dumps(response_json["data"]["timelines"], indent=2)

# print(json_str)
# print(response.json())