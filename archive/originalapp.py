#Mark ayah as memorized
#Mark ayah as needing review
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#import data
data = pd.read_csv("quran_data.csv", index_col = False)
#initial data observ
# data.info()
# print(data.describe())
# print(data.columns)
#Access and change ayah memorized column binary with surah and ayah number input
input = [1,2] #fatiha aya 2
inputrange = [1, [3,4]] #fatiha ayah 1 to 5 - starts at 1 for first for both of them
ayah_range = inputrange[1]

# target_surah = data.query('surah_no == 1')
# target_ayah = data.query()

#select ayah memorized
condition = (data.surah_no == input[0]) & (data.ayah_no_surah == input[1])

# data.loc[(condition), "ayah_memorized"] = True

condition_range = (data.surah_no == input[0]) & (data.ayah_no_surah == input[1])
print(data.loc[(condition_range)])

#set all elements of column to something
data = data.assign(ayah_memorized='False')

for ayah_no in ayah_range:
    print(ayah_no)
    condition_range = ((data.surah_no == inputrange[0]) & (data.ayah_no_surah == ayah_no))
    data.loc[(condition_range), "ayah_memorized"] = True
print(data[data["surah_no"] == 1])

#change ayah memorized to true
data.to_csv("quran_data.csv", index = False)


