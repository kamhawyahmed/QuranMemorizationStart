#Mark ayah as memorized
#Mark ayah as needing review
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class DataManager():
    def __init__(self):
        #self.data = pd.read_csv("quran_data.csv", index_col = False)
        ##when exporting to pythonanywhere add path file here
        self.data = pd.read_csv("quran_data.csv", index_col = False)

    def view_data(self):
        data_info = [self.data.info(), self.data.describe(), self.data.columns]
        return data_info
    def view_ayah(self, surah_num, ayah_nums):
        df = pd.DataFrame()
        for ayah_num in ayah_nums:
            condition = (self.data.surah_no == surah_num) & (self.data.ayah_no_surah == ayah_num)
            df = pd.concat([df,self.data.loc[(condition)][["surah_no", "juz_no", "surah_name_roman", "ayah_ar", "ayah_no_surah", "ayah_memorized"]]])
        return df
    def view_surah(self, surah_num):
        return self.data[self.data["surah_no"] == surah_num][["surah_no", "surah_name_roman", "ayah_no_surah", "ayah_memorized"]]
    def view_ayah_memorized(self, surah_num, ayah_nums):
        memorized = False
        if  self.view_ayah(surah_num, ayah_nums)["ayah_memorized"].all():
            memorized = True
        return memorized
    def view_surah_memorized(self, surah_num):
        memorized = False
        if  self.view_surah(surah_num)["ayah_memorized"].all():
            memorized = True
        return memorized
    def view_surah_juz_num(self, surah_num):
        return self.view_ayah(surah_num, [1])["juz_no"].item()
    def return_length_of_surah(self, surah_num):
        return len(self.view_surah(surah_num))
    def mark_ayah(self, surah_num, ayah_nums):
        for ayah_num in ayah_nums:
            condition = ((self.data.surah_no == surah_num) & (self.data.ayah_no_surah == ayah_num))
            self.data.loc[(condition), "ayah_memorized"] = not self.data.loc[(condition), "ayah_memorized"].item()
        self.save_data()
        return "Ayah memorization status updated."
    def reset_memorization_status(self):
        self.data = self.data.assign(ayah_memorized='False')
        self.save_data()
        return "All ayah memorization status reset to False."
    def return_memorized_ayat(self):
        return self.data[self.data["ayah_memorized"] == True][["surah_no", "surah_name_roman","ayah_no_surah", "ayah_memorized"]]
    def save_data(self):
        # change ayah memorized to true
        self.data.to_csv("quran_data.csv", index=False)
        return "Data saved."

if __name__ == "__main__": #checks if this is imported module
    app = DataManager()
    print(app.view_ayah(78,[1])["juz_no"].item())
    print(app.view_surah_juz_num(78))
    # print(app.view_ayah_memorized(1,[2,3,4]))
    # print(app.view_ayah(1,[2,3,4]))

    # print(app.return_length_of_surah(2))
    # print()
    # app.mark_ayah(1, list(range(1,8)))
    # print(app.view_ayat_of_surah(1))
    # # print(app.return_memorized_ayat())
    #
    #
