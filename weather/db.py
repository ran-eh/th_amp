from sqlalchemy import create_engine
import logging

class DB:    
    def __init__(self, host, db, user, pw):
        connect = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
        self.engine = create_engine(connect)
        self.log = logging.getLogger(__name__)


    def to_table(self, df, table, if_exists, dtype={}):
        self.log.info(f"Writing to table {table} with {if_exists}...")
        n = df.to_sql(
            table,
            con=self.engine,
            index=False,
            if_exists=if_exists,
            dtype=dtype
        )
        self.log.info(f"...{n} rows written")