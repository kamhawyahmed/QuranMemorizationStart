import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#import data
data = pd.read_csv("original_quran_data.csv")
#initial data observ
print(data.info())
print(type(data)) #DATAFRAME

dict_data = data.to_dict()
#Set up csv with ayah memorized column binary

# create list of length of df
list = []
for i in range(0,6236):
    # assign false to all elements of list
    list.append("false")
print(len(list))
# assign header as ayah_memorized
data["ayah_memorized"] = list
data.info()
# save data as csv
data.to_csv("quran_data_edited.csv", index= False)