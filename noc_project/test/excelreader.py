import pandas as pd
import psycopg2

# Table circuit                DONE
# data = pd.read_excel("upload/NOC Web parameter v3.xlsx",sheet_name='Circuit')
# #print(data)
# #print(list(data))
# data = data.values.tolist()
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# for i in data:
#     i[-3] = str(i[-3]).upper()
#     i[-2] = str(i[-2]).upper()
#     cursor = connection.cursor()
#     #cursor.execute('SELECT * FROM circuit WHERE equipment_ref = %s AND owner_isp = %s', (a, b,))
#     cursor.execute('SELECT * FROM circuit WHERE circuit_id = %s AND equipment_ref = %s AND ip_address_pe = %s',(i[1],i[0],i[2],))
#     data_in_base = cursor.fetchall()
#     if data_in_base:
#         print("ERROR")
#     else:
#         postgres_insert_query = """ INSERT INTO circuit (circuit_id, equipment_ref, ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
#         link_number,original_isp,owner_isp,isp_contact_tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#         cursor.execute(postgres_insert_query,(i[1],i[0],i[2],i[3],i[4],i[5],i[6],
#         i[7],i[8],i[9],i[10]))
#         connection.commit()
#         print("successfully in PostgreSOL ")
# cursor.close()
# connection.close()

##Table equipment       DONE
connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
data = pd.read_excel("upload/NOC Web parameter v3.xlsx",sheet_name='Equipment')
#print(list(data))
#print(data)
data.fillna('', inplace=True)
data = data.values.tolist()
for i in data:
    cursor.execute('SELECT * FROM equipment WHERE serial_number = %s AND site_name = %s AND project_name = %s',(i[1],i[0],i[-1],))
    data_in_base = cursor.fetchall()
    if data_in_base:
        print("ERROR")
    else:
        postgres_insert_query = """ INSERT INTO equipment (serial_number, project_name,site_name, brand,model,disty_name,disty_contact,
        open_case_contact,start_of_warranty,end_of_warranty,ha_status,ha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(i[1],i[-1],i[0],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
        connection.commit()
        print("successfully in PostgreSOL ")

# # Table project      DONE 0.5 
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# data = pd.read_excel("upload/NOC Web parameter v3.xlsx",sheet_name='Project')
# data.fillna('', inplace=True)

# data = data.values.tolist()

# data = data[:-1]
# for i in data:
#     #print(type(i[2]))
#     cursor.execute('SELECT * FROM project WHERE project_name = %s AND s_o = %s AND customer_start_of_contract = %s',(i[0],i[1],i[2].strftime("%d/%m/%y"),))
#     #cursor.execute('SELECT * FROM project WHERE project_name = %s AND s_o = %s AND customer_start_of_contract = %s',(i[0],i[1],i[2],))
#     data_in_base = cursor.fetchall()
#     if data_in_base:
#         print("ERROR")
#     else:
#         postgres_insert_query = """ INSERT INTO project (project_name,s_o,customer_start_of_contract,customer_end_of_contract,
#         disty_start_of_contract,disty_end_of_contract,vpn_detail,Important_Detail,
#         Addition_Detail,Remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#         cursor.execute(postgres_insert_query,(i[0],i[1],i[2].strftime("%d/%m/%y"),i[3].strftime("%d/%m/%y"),i[4].strftime("%d/%m/%y"),i[5].strftime("%d/%m/%y"),i[6],i[7],i[8],i[9]))
#         connection.commit()
#         print("successfully in PostgreSOL ")
 
#TABLE site DONE
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# data = pd.read_excel("upload/NOC Web parameter v3.xlsx",sheet_name='Site')
# data.fillna('', inplace=True)
# data = data.values.tolist()
# for i in data:
#     cursor.execute('SELECT * FROM site WHERE project_name = %s AND site_name = %s AND location = %s',(i[0],i[1],i[2],))
#     data_in_base = cursor.fetchall()
#     if data_in_base:
#         print("ERROR")
#     else:
#         postgres_insert_query = """ INSERT INTO site (project_name,site_name,location,site_short_name,
#         contact_owner_site,contact,type) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
#         cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
#         connection.commit()
#         print("successfully in PostgreSOL ")


#TABLE contract DONE
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# data = pd.read_excel("upload/NOC Web parameter v3.xlsx",sheet_name='Contract')
# data.fillna('', inplace=True)
# data = data.values.tolist()
# for i in data:
#     cursor.execute('SELECT * FROM contract WHERE project_name = %s AND role = %s AND name = %s',(i[0],i[1],i[2],))
#     data_in_base = cursor.fetchall()
#     if data_in_base:
#         print("ERROR")
#     else:
#         postgres_insert_query = """ INSERT INTO contract (project_name,role,name,tel,
#         additional_detail) VALUES (%s,%s,%s,%s,%s)"""
#         cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4]))
#         connection.commit()
#         print("successfully in PostgreSOL ")

#TABLE interface 
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# data = pd.read_excel("upload/NOC Web parameter v3.xlsx",sheet_name='Interface')
# data.fillna('', inplace=True)
# data = data.values.tolist()
# for i in data:
#     cursor.execute('SELECT * FROM interface WHERE circuit_id = %s AND equipment_serial = %s AND equipment_brand = %s',(i[0],i[1],i[2],))
#     data_in_base = cursor.fetchall()
#     if data_in_base:
#         print("ERROR")
#     else:
#         postgres_insert_query = """ INSERT INTO interface (circuit_id,equipment_serial,equipment_brand,
#         equipment_model,physical_interface,vlan_id,tunnel_interface_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
#         cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
#         connection.commit()
#         print("successfully in PostgreSOL ")

# cursor.close()
# connection.close()
