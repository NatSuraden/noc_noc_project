import psycopg2
from datetime import datetime
connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
#circuit = 'J12418' "SELECT * FROM circuit WHERE circuit_id ='J12418'"
inputdata = ['Makro','SO200162','','','','','ลาดกระบัง','LKB-S129',
'','FortinetG','FG-60F','SiS Distribution (Thailand) PCL.','2022-10-02','','Yes','V53802','10.99.178.18','10.11.220.8','TRUE']
def W_chack(sql):
    sql_str = sql
    sql_list = sql.split(' ')
    if "Where" not in sql_list:
        sql_str = sql_str+" Where"
        return(sql_str)
    else:
        sql_str = sql_str+" and"
        return(sql_str)


sql = "SELECT * FROM circuit"
if inputdata[-4] != '':
    sql = W_chack(sql)
    sql = sql+" circuit_id = '{}' ".format(inputdata[-4])
if inputdata[-3] != '':
    sql = W_chack(sql)
    sql = sql+" ip_address_ce = '{}' ".format(inputdata[-3])
if inputdata[-2] != '':
    sql = W_chack(sql)
    sql = sql+" Loopback = '{}' ".format(inputdata[-2])
if inputdata[-1] != '':
    sql = W_chack(sql)
    sql = sql+" owner_isp = '{}' ".format(inputdata[-1])
print(sql)
cursor.execute(sql)
equipment = cursor.fetchall()
print(equipment)




sql = "SELECT * FROM circuit"
if inputdata[-4] != '':
    sql = W_chack(sql)
    sql = sql+" circuit_id = '{}' ".format(inputdata[-4])
if inputdata[-3] != '':
    sql = W_chack(sql)
    sql = sql+" ip_address_ce = '{}' ".format(inputdata[-3])
if inputdata[-2] != '':
    sql = W_chack(sql)
    sql = sql+" Loopback = '{}' ".format(inputdata[-2])
if inputdata[-1] != '':
    sql = W_chack(sql)
    sql = sql+" owner_isp = '{}' ".format(inputdata[-1])
print(sql)
cursor.execute(sql)
circuit = cursor.fetchall()
print(circuit)
# cursor.execute('SELECT * FROM circuit')
# circuit = cursor.fetchall()
# cursor.execute('SELECT * FROM equipment')
# equipment = cursor.fetchall()
# cursor.execute('SELECT * FROM project')
# project = cursor.fetchall()
# cursor.execute('SELECT * FROM site')
# site = cursor.fetchall()
# inputdata = ['Makro','SO200162','','','','','ลาดกระบัง','LKB-S129',
# '','FortinetG','FG-60F','SiS Distribution (Thailand) PCL.','2022-10-02','','Yes','V53802','10.99.178.18','222','TRUE']
# #print(inputdata) 
# project_search = []
# site_search = []
# equipment_search = []
# circuit_search = []

# for i in range(4):
#     if i == 0:
#         pass
#     elif i == 1:
#         pass
#     elif i == 2:
#         if inputdata[8] != '':
#                 data_in_process_8 = []
#             # print('do',i)
#                 for n in equipment:
#                     data_in_process = ["","","","","",""] 
#                     if str(n[0]).upper() == str(inputdata[8]).upper():
#                         data_in_process[3] = n[0] #serial_number added
#                         data_in_process[2] = n[2] #site_name added
#                         data_in_process[1] = n[1] #project_name added
#                         for x in circuit:
#                             if x[1] == data_in_process[3]:
#                                 data_in_process[0] = x[0]   #circuit_id  added
#                                 data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                 data_in_process[-1] = x[3]  #IP_address_CE added
#                                 data_in_process_8.append(data_in_process)
#                                 break
#                         equipment_search.append(data_in_process)
#                 if len(data_in_process_8) == 0:
#                     inputdata[8] = str(inputdata[8])+"(NOT FOUND)"
#         if inputdata[9] != '':
#                 data_in_process_9 = []
#                 if inputdata[8] == '':
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[3]).upper() == str(inputdata[9]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_9.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_9) == 0:
#                         inputdata[9] = str(inputdata[9])+"(NOT FOUND)"
#                 else:
#                     data_in_process_9 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[3]).upper() == str(inputdata[9]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_9.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)  
#                     if len(data_in_process_9) == 0:
#                         inputdata[9] = str(inputdata[9])+"(NOT FOUND)"
#         if inputdata[10] != '':
#                 #print('do',i)
#                 if inputdata[8] == '':
#                     data_in_process_10 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[4]).upper() == str(inputdata[10]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_10.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_10) == 0:
#                         inputdata[10] = str(inputdata[10])+"(NOT FOUND)"
#                 else:
#                     data_in_process_10 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[4]).upper() == str(inputdata[10]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_10.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_10) == 0:
#                         inputdata[10] = str(inputdata[10])+"(NOT FOUND)"
#         if inputdata[11] != '':
#                 #print('do',i)
#                 if inputdata[8] == '':
#                     data_in_process_11 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[5]).upper() == str(inputdata[11]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_11.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_11) == 0:
#                         inputdata[11] = str(inputdata[11])+"(NOT FOUND)"
#                 else:
#                     data_in_process_11 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[5]).upper() == str(inputdata[11]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_11.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_11) == 0:
#                         inputdata[11] = str(inputdata[11])+"(NOT FOUND)"
#         if inputdata[8] == '':
#             if inputdata[-7] != "" and inputdata[-6] != "":
#                     data_in_process_15 = []
#                     datetime_object_start = datetime.strptime(inputdata[-7], '%Y-%m-%d')
#                     datetime_object_end = datetime.strptime(inputdata[-6], '%Y-%m-%d')
#                     for i in equipment:
#                         data_in_process = ["","","","","",""]
#                         if datetime_object_start <= i[-4] and datetime_object_end >= i[-3]:
#                             #print(i[0])
#                             data_in_process[3] = i[0] #serial_number added
#                             data_in_process[2] = i[2] #site_name added
#                             data_in_process[1] = i[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_15.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#             elif inputdata[-7] != "":
#                     data_in_process_15 = [] 
#                     datetime_object = datetime.strptime(inputdata[-7], '%Y-%m-%d')
#                     for i in equipment:
#                         data_in_process = ["","","","","",""]
#                         if datetime_object <= i[-4]:
#                             #print(i[0],i[-3])
#                             data_in_process[3] = i[0] #serial_number added
#                             data_in_process[2] = i[2] #site_name added
#                             data_in_process[1] = i[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_15.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_15) == 0:
#                         inputdata[-7] = str(inputdata[-7])+"(NOT FOUND)"            
#             elif inputdata[-6] != "":
#                     data_in_process_15 = []
#                     datetime_object = datetime.strptime(inputdata[-6], '%Y-%m-%d')
#                     for i in equipment:
#                         data_in_process = ["","","","","",""]
#                         if datetime_object >= i[-3]:
#                             #print(i[0],i[-3])
#                             data_in_process[3] = i[0] #serial_number added
#                             data_in_process[2] = i[2] #site_name added
#                             data_in_process[1] = i[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_15.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_15) == 0:
#                         inputdata[-6] = str(inputdata[-6])+"(NOT FOUND)"
#         else:
#             if inputdata[-7] != "" and inputdata[-6] != "":
#                     datetime_object_start = datetime.strptime(inputdata[-7], '%Y-%m-%d')
#                     datetime_object_end = datetime.strptime(inputdata[-6], '%Y-%m-%d')
#                     data_in_process_15 = []
#                     for i in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if datetime_object_start <= i[-4] and datetime_object_end >= i[-3] and str(i[0]).upper() == str(inputdata[8]).upper():
#                             #print(i[0])
#                             data_in_process[3] = i[0] #serial_number added
#                             data_in_process[2] = i[2] #site_name added
#                             data_in_process[1] = i[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_15.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_15) == 0:
#                         inputdata[-7] = str(inputdata[-7])+"(NOT FOUND)"
#                         inputdata[-6] = str(inputdata[-6])+"(NOT FOUND)"
#             elif inputdata[-7] != "":
#                     datetime_object = datetime.strptime(inputdata[-7], '%Y-%m-%d')
#                     data_in_process_15 = []
#                     for i in equipment:
#                         data_in_process = ["","","","","",""]
#                         if datetime_object <= i[-4] and str(i[0]).upper() == str(inputdata[8]).upper():
#                             #print(i[0],i[-3])
#                             data_in_process[3] = i[0] #serial_number added
#                             data_in_process[2] = i[2] #site_name added
#                             data_in_process[1] = i[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_15.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_15) == 0:
#                         inputdata[-7] = str(inputdata[-7])+"(NOT FOUND)"
#             elif inputdata[-6] != "":
#                     datetime_object = datetime.strptime(inputdata[-6], '%Y-%m-%d')
#                     for i in equipment:
#                         if datetime_object >= i[-3] and str(i[0]).upper() == str(inputdata[8]).upper():
#                             #print(i[0],i[-3])
#                             data_in_process[3] = i[0] #serial_number added
#                             data_in_process[2] = i[2] #site_name added
#                             data_in_process[1] = i[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_15.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_15) == 0:
#                         inputdata[-6] = str(inputdata[-6])+"(NOT FOUND)"
#         if inputdata[14] != '':
#                 #print('do',i)
#                 if inputdata[8] == '':
#                     data_in_process_14 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[-2]).upper() == str(inputdata[14]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_14.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)
#                     if len(data_in_process_14) == 0:
#                         inputdata[14] = str(inputdata[14])+"(NOT FOUND)"
#                     equipment_with_ha = []
#                     for i in equipment_search:
#                         #print(i[3])
#                         for n in equipment:
#                             #print(n[0])
#                             if i[3] == n[0] and str(n[-2]).upper() == str(inputdata[14]).upper():
#                                 print(n[0],n[-2])
#                                 equipment_with_ha.append(i)
#                                 break
#                     equipment_search = equipment_with_ha
#                 else:
#                     data_in_process_14 = []
#                     for n in equipment:
#                         data_in_process = ["","","","","",""] 
#                         if str(n[-2]).upper() == str(inputdata[14]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
#                             data_in_process[3] = n[0] #serial_number added
#                             data_in_process[2] = n[2] #site_name added
#                             data_in_process[1] = n[1] #project_name added
#                             for x in circuit:
#                                 if x[1] == data_in_process[3]:
#                                     data_in_process[0] = x[0]   #circuit_id  added
#                                     data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                                     data_in_process[-1] = x[3]  #IP_address_CE added
#                                     data_in_process_14.append(data_in_process)
#                                     break
#                             if data_in_process in equipment_search:
#                                 pass
#                             else:
#                                 equipment_search.append(data_in_process)

#     elif i == 3:
#         if inputdata[15] != '':
#             data_in_process_15 = []
#             for n in circuit:
#                 data_in_process = []
#                 #print(n)
#                 if str(n[0]).upper() == str(inputdata[15]).upper():
#                     data_in_process.append(n[0]) #circuit_id  added
#                     for a in equipment:
#                         if n[1] == a[0]:
#                             data_in_process.append(a[1]) #project_name added
#                             data_in_process.append(a[2]) #site_name added
#                             data_in_process.append(a[0]) #serial_number added
#                             break
#                     data_in_process.append(n[5])     #Equipment_Loopback  added
#                     data_in_process.append(n[3])   #IP_address_CE  added
#                     circuit_search.append(data_in_process)
#                     data_in_process_15.append(data_in_process)
#                     break
#             if len(data_in_process_15) == 0:
#                 #print(15) 
#                 inputdata[15] = str(inputdata[15])+"(NOT FOUND)"
#         if inputdata[16] != '':
#             if inputdata[15] == '':
#                 data_in_process_16 = []
#                 for n in circuit:
#                     data_in_process = []
#                     #print(n)
#                     if str(n[3]).upper() == str(inputdata[16]).upper():
#                         data_in_process.append(n[0]) #circuit_id  added
#                         for a in equipment:
#                             if n[1] == a[0]:
#                                 data_in_process.append(a[1]) #project_name added
#                                 data_in_process.append(a[2]) #site_name added
#                                 data_in_process.append(a[0]) #serial_number added
#                                 break
#                         data_in_process.append(n[5])     #Equipment_Loopback  added
#                         data_in_process.append(n[3])   #IP_address_CE  addedd
#                         data_in_process_16.append(data_in_process)
#                         if data_in_process in circuit_search:
#                             pass
#                         else:
#                             circuit_search.append(data_in_process)
#                             break
#                 if len(data_in_process_16) == 0:
#                     inputdata[16] = str(inputdata[16])+"(NOT FOUND)"
#             else:
#                 data_in_process_16 = []
#                 for n in circuit:
#                     data_in_process = []
#                     #print(n)
#                     if str(n[3]).upper() == str(inputdata[16]).upper() and str(n[0]).upper() == str(inputdata[15]).upper():
#                         data_in_process.append(n[0]) #circuit_id  added
#                         for a in equipment:
#                             if n[1] == a[0]:
#                                 data_in_process.append(a[1]) #project_name added
#                                 data_in_process.append(a[2]) #site_name added
#                                 data_in_process.append(a[0]) #serial_number added
#                                 break
#                         data_in_process.append(n[5])     #Equipment_Loopback  added
#                         data_in_process.append(n[3])   #IP_address_CE  addedd
#                         data_in_process_16.append(data_in_process)
#                         if data_in_process in circuit_search:
#                             pass
#                         else:
#                             circuit_search.append(data_in_process)
#                             break
#                 if len(data_in_process_16) == 0:
#                     inputdata[16] = str(inputdata[16])+"(NOT FOUND)"
#         if inputdata[17] != '':
#             if inputdata[15] == '':
#                 data_in_process_17 = []
#                 for n in circuit:
#                         data_in_process = []
#                         #print(n)
#                         if str(n[5]).upper() == str(inputdata[17]).upper():
#                             data_in_process.append(n[0]) #circuit_id  added
#                             for a in equipment:
#                                 if n[1] == a[0]:
#                                     data_in_process.append(a[1]) #project_name added
#                                     data_in_process.append(a[2]) #site_name added
#                                     data_in_process.append(a[0]) #serial_number added
#                                     break
#                             data_in_process.append(n[5])     #Equipment_Loopback  added
#                             data_in_process.append(n[3])   #IP_address_CE  addedd
#                             data_in_process_17.append(data_in_process)
#                             if data_in_process in circuit_search:
#                                 pass
#                             else:
#                                 circuit_search.append(data_in_process)
#                                 break
#                 if len(data_in_process_17) == 0:
#                     inputdata[17] = str(inputdata[17])+"(NOT FOUND)"
#             else:
#                 data_in_process_17 = []
#                 for n in circuit:
#                         data_in_process = []
#                         #print(n)
#                         if str(n[5]).upper() == str(inputdata[17]).upper() and str(n[0]).upper() == str(inputdata[15]).upper():
#                             data_in_process.append(n[0]) #circuit_id  added
#                             for a in equipment:
#                                 if n[1] == a[0]:
#                                     data_in_process.append(a[1]) #project_name added
#                                     data_in_process.append(a[2]) #site_name added
#                                     data_in_process.append(a[0]) #serial_number added
#                                     break
#                             data_in_process.append(n[5])     #Equipment_Loopback  added
#                             data_in_process.append(n[3])   #IP_address_CE  addedd
#                             data_in_process_17.append(data_in_process)
#                             if data_in_process in circuit_search:
#                                 pass
#                             else:
#                                 circuit_search.append(data_in_process)
#                                 break
#                 if len(data_in_process) == 0:
#                     inputdata[17] = str(inputdata[17])+"(NOT FOUND)"
#             if inputdata[18] != '':
#                 if inputdata[15] == '':
#                     data_in_process_18 = []
#                     for n in circuit:
#                         data_in_process = []
#                         #print(n)
#                         if str(n[-2]).upper() == str(inputdata[18]).upper():
#                             data_in_process.append(n[0]) #circuit_id  added
#                             for a in equipment:
#                                 if n[1] == a[0]:
#                                     data_in_process.append(a[1]) #project_name added
#                                     data_in_process.append(a[2]) #site_name added
#                                     data_in_process.append(a[0]) #serial_number added
#                                     break
#                             data_in_process.append(n[5])     #Equipment_Loopback  added
#                             data_in_process.append(n[3])   #IP_address_CE  addedd
#                             data_in_process_18.append(data_in_process)
#                             if data_in_process in circuit_search:
#                                 pass
#                             else:
#                                 circuit_search.append(data_in_process)
#                     if len(data_in_process_18) == 0:
#                         inputdata[18] = str(inputdata[18])+"(NOT FOUND)"
#                 else:
#                     data_in_process_18 = []
#                     for n in circuit:
#                         data_in_process = []
#                         #print(n)
#                         if str(n[-2]).upper() == str(inputdata[18]).upper() and str(n[0]).upper() == str(inputdata[15]).upper():
#                             data_in_process.append(n[0]) #circuit_id  added
#                             for a in equipment:
#                                 if n[1] == a[0]:
#                                     data_in_process.append(a[1]) #project_name added
#                                     data_in_process.append(a[2]) #site_name added
#                                     data_in_process.append(a[0]) #serial_number added
#                                     break
#                             data_in_process.append(n[5])     #Equipment_Loopback  added
#                             data_in_process.append(n[3])   #IP_address_CE  addedd
#                             data_in_process_18.append(data_in_process)
#                             if data_in_process in circuit_search:
#                                 pass
#                             else:
#                                 circuit_search.append(data_in_process)
#                     if len(data_in_process_18) == 0:
#                         inputdata[18] = str(inputdata[18])+"(NOT FOUND)"

# print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
# print('input by equipment',inputdata[8:15])
# print('datatable by equipment')
# for i in equipment_search:
#     print(i)


# print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
# print('input by circuit',inputdata[15:])

# print('datatable by circuit')
# for i in circuit_search:
#     print(i)