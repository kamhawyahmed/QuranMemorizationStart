import sqlite3
con = sqlite3.connect("quran_data.db") # creates implicitly if not found
cur = con.cursor()
res = cur.execute("SELECT surah_name_roman FROM memorization WHERE ayah_memorized = True")
result = res.fetchall()
print(cur.description, result)

def query_db():
    cur = con.cursor()
    res = cur.execute("SELECT surah_name_roman FROM memorization WHERE ayah_memorized = True")
    result = res.fetchall()
    con.close()