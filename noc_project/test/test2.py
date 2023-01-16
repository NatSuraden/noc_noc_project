import pandas as pd
import psycopg2
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
a = ['J12418', 'Makro', 'ลาดกระบัง', 'J108EN5920004706', '10.11.220.10', '171.103.210.226']
b = "a"

for i in a:
    if b in i:
        print(i)


    