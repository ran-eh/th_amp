import numpy as np
import pandas as pd


def get_locations():
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
    return locations_df