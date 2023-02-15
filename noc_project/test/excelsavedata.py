import pandas as pd
import psycopg2
import numpy as np
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
contract = cursor.fetchall()
cursor.execute('SELECT * FROM site')
site = cursor.fetchall()

Project_Name = []
S_O = []
Customer_Start_of_contract = []
Customer_End_of_contract = []
Disty_Start_of_contract = []
Disty_End_of_contract = []
Vpn_Detail = []
Important_Detail = []
Addition_Detail = []
Remark = []
for i in project:
    Project_Name.append(i[0])
    S_O.append(i[1])
    Customer_Start_of_contract.append(i[2].strftime("%d/%m/%Y"))
    Customer_End_of_contract.append(i[3].strftime("%d/%m/%Y"))
    Disty_Start_of_contract.append(i[4].strftime("%d/%m/%Y"))
    Disty_End_of_contract.append(i[5].strftime("%d/%m/%Y"))
    Vpn_Detail.append(i[6])
    Important_Detail.append(i[7])
    Addition_Detail.append(i[8])
    Remark.append(i[9])

p_data = [Project_Name, S_O,Customer_Start_of_contract,Customer_End_of_contract,
   Disty_Start_of_contract,Disty_End_of_contract,Vpn_Detail,Important_Detail,
   Addition_Detail,Remark]
columns =["Project Name", "S/O","Customer_Start_of_contract","Customer_End_of_contract",
   "Disty_Start_of_contract","Disty_End_of_contract","Vpn Detail",
   "Important_Detail","Addition_Detail","Remark"]
df1 = pd.DataFrame(dict(zip(columns, p_data)))

Project_Name_contract = []
role = []
name = []
Tel = []
Addition_Detail_contract = []

for i in contract:
    #print(i)
    Project_Name_contract.append(i[1])
    role.append(i[2])
    name.append(i[3])
    Tel.append(i[4])
    Addition_Detail_contract.append(i[5])

con_data = [Project_Name_contract,role,name,Tel,Addition_Detail_contract]
columns = ["Project Name","Role","Name","Tel.","Additional Detail"]
df2 = pd.DataFrame(dict(zip(columns, con_data)))


with pd.ExcelWriter('noc_project/test/output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Project', index=False)
    df2.to_excel(writer, sheet_name='Contract', index=False)
# data = pd.read_excel("noc_project/test/output.xlsx",sheet_name='Project')
# #data = pd.read_excel("noc_project/upload/data_up_load.xlsx",sheet_name='Project')
# print(data)