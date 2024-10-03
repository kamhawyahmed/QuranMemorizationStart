# TODO
# Add class for table even though never adding new records but to refer to them - maybe dont have to define all col's and maybe will crash if applying - found it
# Convert from 1 page site to multi page
#   Home page with surah list
#   subpages for surahs
# - 1 button to view all memorized surah (get) DONE
# - 1 BUTTON TO SHOW BUTTONS DONE
# - 114 buttons for 114 chapters, click button - mark memorize DONE and change colour (put)
    #html loop for 114 buttons DONE
    #integrate data from main.py DONE

from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import QuranDataManager
import sqlite3



backend = QuranDataManager.DataManager()


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quran_data.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model): 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context(): #open the app
    db.reflect()
    db.create_all()


# with app.test_request_context():
#     print(url_for('update', username='John-Doe'))



surah_shown_index = 1
memorized_surahs = []
surah_list = backend.make_mock_surah_list()



app_on = True
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form)
        if "app_on" in request.form:
            toggle_app()
    return render_template("test.html", app_on=app_on)

@app.route('/', methods=['GET', 'POST'])
def quran_memorization_page():
    if request.method == 'POST':
        print(request.form)

        if "show_memorized" in request.form:
            # result = db.session.execute(db.select(Book).order_by(Book.title))
            show_memorized_surah()
        else:
            for key in request.form.keys():
                if key.split("_")[1] == "surah":
                    toggle_memorized_surah()
                elif key.split("_")[1] == "ayah":
                    toggle_memorized_ayah()
                elif key.split("_")[0] == "select":
                    select_surah()
    for idx, surah in surah_list[surah_list["juz_no"] == 1].iterrows():
        print(surah["juz_no"])
        # print(type(surah_list[surah_list["juz_no"] == 1]))
    return update_page()

def toggle_app():
    global app_on
    app_on = not app_on
    return

def show_memorized_surah():
    print("hi")
    global memorized_surahs
    memorized_surahs = []

    for surah_name in backend.return_memorized_ayat()["surah_name_roman"]:
        memorized_surahs.append(surah_name)
    memorized_surahs = list(set(memorized_surahs))

def select_surah():
    global surah_shown_index
    for key in request.form.keys():
        surah_shown_index = [int(s) for s in key.split("_") if s.isdigit()][0]
    return

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
    return render_template("memorization.html", memorized_surahs = memorized_surahs, backend = backend, app_on = app_on, surah_shown_index = surah_shown_index, surah_list = surah_list)


if __name__ == "__main__":
    app.run(debug=True)
