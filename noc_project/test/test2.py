import pandas as pd
import psycopg2
import time
import datetime
from datetime import datetime

# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# cursor.execute('SELECT * FROM project')
# project = cursor.fetchall()
# # data = pd.read_excel("noc_project/upload/NOC Web parameter v3.xlsx",sheet_name='Project')
# # data.fillna('', inplace=True)
# # #print(data)
# # #print(list(data))
# # """ data = data.values.tolist()
# # data2 = []
# # for i in (data):
# #     i[-2] = str(i[-2]).upper()
# #     i[-3] = str(i[-3]).upper()
# #     i[-4] = str(i[-4]).upper()
# #     data2.append(i)
# # for i in data2:
# #     print(i) """
# # """ col = []
# # for i in data.columns:
# #     col.append(i)
# # print(col)
# # #print(list(data)) """

# # data = data.values.tolist()
# # #print(data)
# # for i in data:
# #     print(i)
# # print((data[0][2]).strftime("%d/%m/%y"))  

# # test_str = "ABCDE\Gnadasdasdas"
# # if "\n" in test_str:
# #     print(True)
# # from datetime import datetime

# datetime_str1 = ['09/09/22','10/09/22','11/09/22','12/09/22']
# datetime_str12 = []
# for i in datetime_str1:
#     datetime_object = datetime.strptime(i, '%d/%m/%y')
#     datetime_str12.append(datetime_object)

# a = datetime_str12[-1]
# print(a)
# # for i in datetime_str12:
# #     if i < a:
# #         print(i)

# for i in project:
#     #print(i[2])
#     if i[2] > a:
#         print(i[2],"True")
    


# date_str = '2023-01-26'

# date_object = datetime.strptime(date_str, '%Y-%m-%d')
# print(type(date_object))
# print(date_object)  # printed in default format

# a = ["1","2"]
# b = ['A','B']
# c = [a,b]
# print(c)


from cryptography.fernet import Fernet

# we will be encrypting the below string.
message = "1234"
 
# generate a key for encryption and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key
 
key = Fernet.generate_key()
key = str(key)
key = bytes(key)
# Instance the Fernet class with the key
 
fernet = Fernet(key)
 
# then use the Fernet class instance
# to encrypt the string string must
# be encoded to byte string before encryption
encMessage = fernet.encrypt(message.encode())
 
print("original string: ", message)
print("encrypted string: ", encMessage)
 
# decrypt the encrypted string with the
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods
decMessage = fernet.decrypt(encMessage).decode()
 
print("decrypted string: ", decMessage)
    