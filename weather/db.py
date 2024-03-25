from sqlalchemy import create_engine


class DB:    
    def __init__(self, host, db, user, pw):
        connect = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
        self.engine = create_engine(connect)


    def to_table(self, df, table, if_exists, dtype={}):
        df.to_sql(
            table,
            con=self.engine,
            index=False,
            if_exists=if_exists,
            dtype=dtype
        )