import pandas as pd
import requests

url_base = "https://api.tomorrow.io/v4"
class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_realtime(self, lat, lon):
        url = f"{url_base}/weather/realtime?location={lat}%2C%20{lon}&units=metric&apikey={self.api_key}"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        df = pd.json_normalize(response.json()["data"])
        df.insert(0, 'lat', lat)
        df.insert(1, 'lon', lon)
        return df


    def get_timelines(self, lat, lon):
        url = f"{url_base}/timelines?apikey={self.api_key}"

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
        return df