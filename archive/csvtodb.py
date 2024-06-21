import pandas as pd
import sqlite3

df = pd.read_csv("../quran_data.csv", index_col=False)

columns = ""
for i in df.columns:
    columns += f"{i}, "
columns = columns[:-2]

num_col = len(df.columns)



con = sqlite3.connect("quran_data.db") # creates implicitly if not found
cur = con.cursor()
#initialize col
cur.execute(f"CREATE TABLE memorization({columns})")

##add rows
placeholders = ""
for i in range(0, num_col):
    placeholders += "?, "
placeholders = placeholders[:-2]

list_of_tuples = []
list_of_tuples = list(df.itertuples(index=False, name=None))
cur.executemany(f"INSERT INTO memorization VALUES({placeholders})", list_of_tuples) #dont use f string for deployment - injection risk if someone has " in placeholder
con.commit()
con.close()