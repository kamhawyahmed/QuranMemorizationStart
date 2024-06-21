# GOAL - COMPLETE
# - 1 button to view all memorized surah (get) DONE
# - 1 BUTTON TO SHOW BUTTONS DONE
# - 114 buttons for 114 chapters, click button - mark memorize DONE and change colour (put)
    #html loop for 114 buttons DONE
    #integrate data from main.py DONE
from flask import Flask
from flask import render_template
from flask import request
import QuranDataManager
import sqlite3

NUM_SURAH = 114
backend = QuranDataManager.DataManager()


app = Flask(__name__)

test = "test"

memorized_surahs = []

app_on = True

##db
from flask import g #global use item for between function storage within 1 call

DATABASE = 'quran_data.db'

def get_db(): #returns con object
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE) #open db and create if not existing
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close() #close db and save
def query_db(query):
    con = get_db()
    cur = con.cursor()
    res = cur.execute(query)
    result = res.fetchall()
    return result
def query_ayah_memorized(surah_no, ayah_no):
    return query_db(f"SELECT ayah_memorized FROM memorization WHERE surah_no = {surah_no} AND ayah_no_surah = {ayah_no}")[0][0]
##





@app.route('/', methods=['GET', 'POST'])
def quran_memorization_page():
    global test
    test = query_db("SELECT ayah_memorized FROM memorization WHERE surah_no = 1 AND ayah_no_surah = 1")

    if request.method == 'POST':
        print(request.form)
        if "app_on" in request.form:
            global app_on
            app_on = not app_on
        elif "show_memorized" in request.form:
            global memorized_surahs
            memorized_surahs = list(set(query_db("SELECT surah_name_roman FROM memorization WHERE ayah_memorized = True")))
            # global memorized_surahs
            # memorized_surahs = []
            # for surah_name in backend.return_memorized_ayat()["surah_name_roman"]:
            #     memorized_surahs.append(surah_name)
            # memorized_surahs = list(set(memorized_surahs))
        else:
            for key in request.form.keys():
                if key.split("_")[1] == "surah":
                    toggle_memorized_surah()
                elif key.split("_")[1] == "ayah":
                    toggle_memorized_ayah()
    return update_page()


def toggle_memorized_surah():
    for key in request.form.keys():
        surah_toggle_num = [int(s) for s in key.split("_") if s.isdigit()][0]
    ayat_to_toggle = list(range(1,backend.return_length_of_surah(surah_toggle_num)+1))
    backend.mark_ayah(surah_toggle_num, ayat_to_toggle)
    return

def toggle_memorized_ayah():
    for key in request.form.keys():
        surah_toggle_num, ayah_toggle_num = [int(s) for s in key.split("_") if s.isdigit()][0:2]
    backend.mark_ayah(surah_toggle_num, [ayah_toggle_num])
    return

def update_page():
    return render_template("requestdb.html", num_surah = NUM_SURAH, memorized_surahs = memorized_surahs, backend = backend, app_on = app_on, test_output = test, query_ayah_memorized = query_ayah_memorized)


if __name__ == "__main__":
    app.run(debug=True)
