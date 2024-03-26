import logging
import pandas as pd
import requests

url_base = "https://api.tomorrow.io/v4"
class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        # Alternate api key, in case the main one runs out
        # self.api_key = 'NPbBxunJXWpykpE2kISa3rSV00WFgJQu'
        self.log = logging.getLogger(__name__)


    def get_realtime(self, lat, lon):
        url = f"{url_base}/weather/realtime?location={lat}%2C%20{lon}&units=metric&apikey={self.api_key}"

        headers = {"accept": "application/json"}

        info = {'url': url, 'headers': headers}
        self.log.info(f"GET: {info}")
        response = requests.get(url, headers=headers)
        self.log.info(f"status_code: {response.status_code}")
        if not response.ok:
            self.log.error(f"response: {response.json()}")
            return None, response.json()
        df = pd.json_normalize(response.json()["data"])
        df.insert(0, 'lat', lat)
        df.insert(1, 'lon', lon)
        return df, None


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
        info = {'url': url, 'headers': headers, 'json': payload}
        self.log.info(f"POST: {info}")

        response = requests.post(url, json=payload, headers=headers)
        self.log.info(f"status_code: {response.status_code}")

        if not response.ok:
            self.log.error(f"response: {response.json()}")
            return None, response.json()

        response_json = response.json()
        timelines = response_json["data"]["timelines"]
        timeline = timelines[0]
        intervals = timeline["intervals"]
        df = pd.DataFrame(intervals)
        df = pd.json_normalize(intervals)
        df.insert(0, 'lat', lat)
        df.insert(1, 'lon', lon)
        return df, None