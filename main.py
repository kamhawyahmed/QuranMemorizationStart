#PYTHONANYWHERE SETUP INSTRUCTIONS -
# del folder
# git clone github
# pip3.10 install --user -r requirements.txt
# error codes ignore

# TODO list
# TODO MAKE PRETTY HOME PAGE
# TODO MAKE PRETTY SURAH PAGE
# TODO MERGE THSI WITH REST OF PYANYWHERE SITE
# Add class for table even though never adding new records but to refer to them -
#   maybe dont have to define all col's and maybe will crash if applying - found it DONE
# Convert from 1 page site to multi page - DONE
#   Home page with surah list DONE
#   subpages for surahs DONE
# - 1 button to view all memorized surah (get) DONE
# - 1 BUTTON TO SHOW BUTTONS DONE
# - 114 buttons for 114 chapters, click button - mark memorize DONE and change colour (put)
#    #html loop for 114 buttons DONE
#    #integrate data from main.py DONE

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from typing import List

#


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quran_data.db"
# app.config["SQLALCHEMY_ECHO"] = True

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
    surah_memorized: Mapped[int] = mapped_column(Integer)



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
    ayah_ar: Mapped[str] = mapped_column(String)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Ayah {self.surah_no}:{self.ayah_no_surah}>'

with app.app_context(): #open the app
    db.create_all()

app_on = True
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form)
    return render_template("test.html")

@app.route('/', methods=['GET'])
def home():
    result = db.session.execute(db.select(Surah))
    surahs = result.scalars().all()
    return render_template("memorization_home.html", surahs = surahs)

@app.route('/surah/<surah_no>', methods=['GET', 'POST'])
def surah(surah_no):
    result = db.session.execute(db.select(Surah).where(Surah.surah_no == surah_no))
    surah_selected = result.scalar()
    if request.method == 'POST':
        key = list(request.form.keys())[0]
        if "surah" in key:
            surah_selected.surah_memorized = 1 - surah_selected.surah_memorized
            ayat_selected = surah_selected.ayat
            for ayah in ayat_selected:
                ayah.ayah_memorized = surah_selected.surah_memorized
            db.session.commit()
        elif "ayah" in key:
            ayah_no = [int(s) for s in key.split("_") if s.isdigit()][0]
            ayah_selected = surah_selected.ayat[ayah_no - 1]
            ayah_selected.ayah_memorized = 1 - ayah_selected.ayah_memorized
            surah_selected.surah_memorized = calculate_surah_memorized(surah_selected)
            db.session.commit()
    return render_template("memorization_surah.html", surah_selected = surah_selected)


def calculate_surah_memorized(surah):
    surah_memorized = 1
    for ayah in surah.ayat:
        if ayah.ayah_memorized == 0:
            surah_memorized = 0
    return surah_memorized

def update_all_surah_memorized_manually():
    with app.test_request_context():
        result = db.session.execute(db.select(Surah))
        surah_list = result.scalars().all()
        for surah in surah_list:
            surah_memorized = 1
            for ayah in surah.ayat:
                if ayah.ayah_memorized == 0:
                    surah_memorized = 0
                    print(surah.surah_no, ayah.ayah_no_surah, ayah.ayah_memorized, surah_memorized)
            surah.surah_memorized = surah_memorized
        db.session.commit()
    return

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)