import psycopg2
import pandas as pd
import json
import ast
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# #cursor.execute('SELECT * FROM accounts')
# cursor.execute('SELECT * FROM project')
# data = cursor.fetchall()

# # name = []
# # Role = []
# # password = []
# # for i in account:
# #     i = list(i)
# #     name.append(i[1])
# #     password.append(i[2])
# #     Role.append(i[3])
 
# # dictionary of lists
# # dict = {'Username': name, 'Password': password, 'Role': Role}
     
# # df = pd.DataFrame(dict)
 
# #print(data)
# #print(len(data))
# for i in data[0]:
#     print(i)
#     print("______________________________________")

# a = data[0][2]

# print((data[0][2]).strftime("%d/%m/%y"))
connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
cursor.execute('SELECT * FROM circuit')
circuit = cursor.fetchall()
cursor.execute('SELECT * FROM equipment')
equipment = cursor.fetchall()
cursor.execute('SELECT * FROM interface')
interface = cursor.fetchall()
cursor.execute('SELECT * FROM project')
project = cursor.fetchall()
cursor.execute('SELECT * FROM contract')
contrat = cursor.fetchall()
# a = "(['V53802', 'Makro', 'ลาดกระบัง', 'FGT60FTK20054815', '10.11.220.8', '10.99.178.18'], 'V53802')"
a = "(['V53802', 'Makro', 'ลาดกระบัง', 'FGT60FTK20054815', '10.11.220.8', '10.99.178.18'], 'Makro')"
res = ast.literal_eval(a)
print(res)
print(res[1])
index = res[0].index(res[1])
print(index)
if index == 1:
    zone1 = [res[1],res[0][0],res[0][3]] #Project Name , circuit_Id ,Serial_numbe 
    zone2 = [] #project detials
    zone3 = [] #contrat
    for i in project:
        if i[0] == res[1]:
            zone2 = i
            break
    #print(zone2)
    for i in contrat:
        if i[1] == res[1]:
            zone3 = i
            break
    print(zone3)
# if index == 0: #circuit_ID
#     zone1 = [res[0][1]] #Project Name
#     zone2 = [] #Detial circuit ทั้งหมด
#     zone3 = ["","",""] #Equipment Model ,Equipment Brand ,Serial_numbe
#     zone4 = [] #Physical Interface , VLAN_ID , Tunnel Interface Name
#     for i in circuit:
#         if i[0] == res[1]:
#             zone2 = i
#             zone3[-1] = i[1]
#             break
#     for i in equipment:
#         if i[0] == zone3[-1]:
#             zone3[0] = i[4]
#             zone3[1] = i[3]
#             break
#     for i in interface:
#         if i[1] == res[1]:
#             zone4.append(i[-3])
#             zone4.append(i[-2])
#             zone4.append(i[-1])
#     print(zone1)
#     print(zone2)
#     print(zone3)
#     print(zone4)

#     print(zone4[-1])
#     zone4[-1] = str(zone4[-1]).replace("\n"," <br /> ")
#     print(zone4)
    