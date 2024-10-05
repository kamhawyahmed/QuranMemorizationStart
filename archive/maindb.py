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

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List
import QuranDataManager



backend = QuranDataManager.DataManager()


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quran_data.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# with app.app_context(): #open the app
#     db.reflect()


class Surah(db.Model):
    __tablename__ = "surah"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    surah_no: Mapped[int] = mapped_column(Integer, unique=True)
    total_ayah_surah: Mapped[int] = mapped_column(Integer)
    juz_no: Mapped[int] = mapped_column(Integer)
    surah_name_roman: Mapped[str] = mapped_column(String)
    surah_name_en: Mapped[str] = mapped_column(String)
    surah_name_ar: Mapped[str] = mapped_column(String)
    place_of_revelation: Mapped[str] = mapped_column(String)



    ayat: Mapped[List["Ayah"]] = relationship(back_populates="surah")
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'< Surah {self.surah_no}, Ayat: {self.ayat} >'

class Ayah(db.Model): 
    __tablename__ = "ayah"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    surah_name_roman: Mapped[str] = mapped_column(String)
    surah_no: Mapped[int] = mapped_column(ForeignKey("surah.surah_no"))
    juz_no: Mapped[int] = mapped_column(Integer)
    ayah_no_surah: Mapped[int] = mapped_column(Integer)
    ayah_memorized: Mapped[int] = mapped_column(Integer)
    surah: Mapped["Surah"] = relationship(back_populates="ayat")

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Ayah {self.surah_no}:{self.ayah_no_surah}>'

with app.app_context(): #open the app
    db.create_all()


surah_shown_index = 1
memorized_surahs = []
surah_list = backend.make_mock_surah_list()
surah_selected = []
    

# with app.test_request_context():
#     print(surah)

app_on = True
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form)
        if "app_on" in request.form:
            toggle_app()
    return render_template("test.html", app_on=app_on)

@app.route('/', methods=['GET', 'POST'])
def quran_memorization_page(memorized_surahs=memorized_surahs):
    if request.method == 'POST':
        print(request.form)

        if "show_memorized" in request.form:
            memorized_surahs = show_memorized_surahs()

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
    return render_template("memorization.html", memorized_surahs = memorized_surahs, surah= surah_selected, backend = backend, app_on = app_on, surah_shown_index = surah_shown_index, surah_list = surah_list)



def toggle_app():
    global app_on
    app_on = not app_on
    return

def show_memorized_surahs():
    result = db.session.execute(db.select(Ayah).order_by(Ayah.id).where(Ayah.ayah_memorized == 1))
    memorized_surahs = set([ayah.surah_name_roman for ayah in result.scalars()])
    return memorized_surahs

def select_surah():
    global surah_shown_index
    global surah_selected
    for key in request.form.keys():
        surah_shown_index = [int(s) for s in key.split("_") if s.isdigit()][0]
        result = db.session.execute(db.select(Surah).where(Surah.surah_no == surah_shown_index))
        surah_selected = result.scalar()
    return redirect(url_for('quran_memorization_page'))


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)