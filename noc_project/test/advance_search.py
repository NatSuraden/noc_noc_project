import psycopg2
connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
cursor.execute('SELECT * FROM circuit')
circuit = cursor.fetchall()
cursor.execute('SELECT * FROM equipment')
equipment = cursor.fetchall()
cursor.execute('SELECT * FROM project')
project = cursor.fetchall()
cursor.execute('SELECT * FROM site')
site = cursor.fetchall()
inputdata = ['Makro','SO200162','','','','','ลาดกระบัง','LKB-S129',
'FGT60FTK20054815','Fortinet','FG-60F','SiS Distribution (Thailand) PCL.','','','Yes','V53802','10.99.178.18','10.11.220.8','TRUE',]
print(inputdata)