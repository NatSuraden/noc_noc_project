import pandas as pd
import psycopg2
connection = psycopg2.connect(user="postgres",password="pplus1234", host="127.0.0.1", port="5432", database="postgres")
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
cursor.execute('SELECT * FROM site')
site = cursor.fetchall()

ex_name_sheet = ['Project','Contract','Site','Equipment','Circuit','Interface']
for i in ex_name_sheet:
    data = pd.read_excel("noc_project/upload/NOC Web parameter v3.xlsx",sheet_name=i)
    data = data.values.tolist()
    if i == 'Project':
        project_data = data
    elif i == 'Contract':
        contract_data = data
    elif i == 'Site':
        site_data = data
    elif i == "Equipment":
        equipment_data = data
    elif i == 'Circuit':
        circuit_data = data
    elif i == 'Interface':
        interface_data = data


# project table check