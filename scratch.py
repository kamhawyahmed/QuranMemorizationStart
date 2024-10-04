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
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class Ayah(db.Model): 
    # __table__ = db.metadatas[None].tables['quran_data']
    __tablename__ = "quran_data"
    index: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    surah_no: Mapped[int] = mapped_column(Integer)
    ayah_no_surah: Mapped[int] = mapped_column(Integer)
    ayah_memorized: Mapped[int] = mapped_column(Integer)
    # title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # author: Mapped[str] = mapped_column(String(250), nullable=False)
    # rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    # def __repr__(self):
    #     return f'<Ayah {self.surah_no} | {self.ayah_no_surah}>'

with app.app_context(): #open the app
    db.create_all()



# with app.test_request_context():
#     print(url_for('update', username='John-Doe'))



surah_shown_index = 1
memorized_surahs = []
memorized_surahs_db = ["hi"]
surah_list = backend.make_mock_surah_list()

with app.test_request_context():
    result = db.session.execute(db.select(Ayah).where(Ayah.surah_no == 1))
    ayat = result.scalars()
    for ayah in ayat:
        print(f"Surah_No: {ayah.surah_no} Ayah_No: {ayah.ayah_no_surah} Memorized: {ayah.ayah_memorized}")
    # for ayah in ayat:
    #     print(ayah.surah_no)


#     ayat = (result.scalars())
#     ayat_list = list(ayat)
#     print(f"Ayat: {ayat_list}")
#     for ayah in result.scalars():
#         print(ayah)

@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form)
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
