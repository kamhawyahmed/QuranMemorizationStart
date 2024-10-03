import sqlite3
con = sqlite3.connect("quran_data.db")

import pandas as pd
df = pd.read_csv("quran_data.csv")

print(df.columns)
df.to_sql(name="quran_data", con=con, chunksize=10000, if_exists="fail")
