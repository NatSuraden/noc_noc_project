import pandas as pd
import psycopg2
import time
import datetime
from datetime import datetime

connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
cursor.execute('SELECT * FROM project')
project = cursor.fetchall()
# data = pd.read_excel("noc_project/upload/NOC Web parameter v3.xlsx",sheet_name='Project')
# data.fillna('', inplace=True)
# #print(data)
# #print(list(data))
# """ data = data.values.tolist()
# data2 = []
# for i in (data):
#     i[-2] = str(i[-2]).upper()
#     i[-3] = str(i[-3]).upper()
#     i[-4] = str(i[-4]).upper()
#     data2.append(i)
# for i in data2:
#     print(i) """
# """ col = []
# for i in data.columns:
#     col.append(i)
# print(col)
# #print(list(data)) """

# data = data.values.tolist()
# #print(data)
# for i in data:
#     print(i)
# print((data[0][2]).strftime("%d/%m/%y"))  

# test_str = "ABCDE\Gnadasdasdas"
# if "\n" in test_str:
#     print(True)
# from datetime import datetime

datetime_str1 = ['09/09/22','10/09/22','11/09/22','01/01/19']
datetime_str12 = []
for i in datetime_str1:
    datetime_object = datetime.strptime(i, '%d/%m/%y')
    datetime_str12.append(datetime_object)

a = datetime_str12[-1]
print(a)
# for i in datetime_str12:
#     if i < a:
#         print(i)

for i in project:
    #print(i[2])
    if i[2] > a:
        print(i[2],"True")
    



    