import logging
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
period_seconds =  os.environ.get("WAIT_SEONDS", 60 * 2)

def run():
    log.info("Starting run")
    locations_df = get_locations()

    conn = DB(host, db, user, pw)
    api = WeatherAPI(api_key)
    for ix, row in locations_df.iterrows():
        lat = str(row["lat"])
        lon = str(row["lon"])
        log.info(f"Starting for {lat},{lon}")

        # If first location, rewrite table from scratch
        if_exists = 'replace' if ix == 0 else 'append'

        df, err = api.get_realtime(lat, lon)
        if err:
            return err
        
        conn.to_table(df, 'realtime', if_exists, dtype={"time": DateTime()})

        df, err  = api.get_timelines(lat, lon)
        if err:
            return err
        conn.to_table(df, 'timeline', if_exists, dtype={"startTime": DateTime()})
    log.info("Run ended")
    return None

if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
    log = logging.getLogger(__name__)
    log.info("Starting Weather Service")
    while True:
        try:
            err = run()
            if err:
                log.error(err)
        except Exception as e:
            log.exception(e)
        finally:
            log.info(f"Sleep for {period_seconds} seconds")
            time.sleep(period_seconds) # 1 hour
