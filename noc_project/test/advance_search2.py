import psycopg2
from datetime import datetime
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
'FGT60FTK20054815','FortinetG','FG-60F','SiS Distribution (Thailand) PCL.','','2023-11-26','Yes','V53802','10.99.178.18','222','TRUE']
#print(inputdata) 
project_search = []
site_search = []
equipment_search = []
circuit_search = []

for i in range(4):
    if i == 0:
        pass
    elif i == 1:
        pass
    elif i == 2:
        serial = []
        if inputdata[-6] == "" and inputdata[-7] == "":
            if inputdata[8] != '':
                data_in_process_8 = []
            # print('do',i)
                for n in equipment:
                    data_in_process = ["","","","","",""] 
                    if str(n[0]).upper() == str(inputdata[8]).upper():
                        data_in_process[3] = n[0] #serial_number added
                        data_in_process[2] = n[2] #site_name added
                        data_in_process[1] = n[1] #project_name added
                        for x in circuit:
                            if x[1] == data_in_process[3]:
                                data_in_process[0] = x[0]   #circuit_id  added
                                data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                data_in_process[-1] = x[3]  #IP_address_CE added
                                data_in_process_8.append(data_in_process)
                                break
                        equipment_search.append(data_in_process)
                if len(data_in_process_8) == 0:
                    inputdata[8] = str(inputdata[8])+"(NOT FOUND)"
            if inputdata[9] != '':
                data_in_process_9 = []
                if inputdata[8] == '':
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[3]).upper() == str(inputdata[9]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    data_in_process_9.append(data_in_process)
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_9) == 0:
                        inputdata[9] = str(inputdata[9])+"(NOT FOUND)"
                else:
                    data_in_process_9 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[3]).upper() == str(inputdata[9]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    data_in_process_9.append(data_in_process)
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)  
                    if len(data_in_process_9) == 0:
                        inputdata[9] = str(inputdata[9])+"(NOT FOUND)"
            if inputdata[10] != '':
                #print('do',i)
                if inputdata[8] == '':
                    data_in_process_10 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[4]).upper() == str(inputdata[10]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    data_in_process_10.append(data_in_process)
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_10) == 0:
                        inputdata[10] = str(inputdata[10])+"(NOT FOUND)"
                else:
                    data_in_process_10 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[4]).upper() == str(inputdata[10]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    data_in_process_10.append(data_in_process)
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_10) == 0:
                        inputdata[10] = str(inputdata[10])+"(NOT FOUND)"
            if inputdata[11] != '':
                #print('do',i)
                if inputdata[8] == '':
                    data_in_process_11 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[5]).upper() == str(inputdata[11]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    data_in_process_11.append(data_in_process)
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_11) == 0:
                        inputdata[11] = str(inputdata[11])+"(NOT FOUND)"
                else:
                    data_in_process_11 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[5]).upper() == str(inputdata[11]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    data_in_process_11.append(data_in_process)
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_11) == 0:
                        inputdata[11] = str(inputdata[11])+"(NOT FOUND)"
            if inputdata[14] != '':
                #print('do',i)
                if inputdata[8] == '':
                    data_in_process_14 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[-2]).upper() == str(inputdata[14]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_14) == 0:
                        inputdata[14] = str(inputdata[14])+"(NOT FOUND)"
                else:
                    data_in_process_14 = []
                    for n in equipment:
                        data_in_process = ["","","","","",""] 
                        if str(n[-2]).upper() == str(inputdata[14]).upper() and str(n[0]).upper() == str(inputdata[8]).upper():
                            data_in_process[3] = n[0] #serial_number added
                            data_in_process[2] = n[2] #site_name added
                            data_in_process[1] = n[1] #project_name added
                            for x in circuit:
                                if x[1] == data_in_process[3]:
                                    data_in_process[0] = x[0]   #circuit_id  added
                                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                                    data_in_process[-1] = x[3]  #IP_address_CE added
                                    break
                            if data_in_process in equipment_search:
                                pass
                            else:
                                equipment_search.append(data_in_process)
                    if len(data_in_process_14) == 0:
                        inputdata[14] = str(inputdata[14])+"(NOT FOUND)"
        else:
            if inputdata[-6] != "":
                datetime_object = datetime.strptime(inputdata[-6], '%Y-%m-%d')
                for i in equipment:
                    if datetime_object >= i[-3]:
                        print(i)
    elif i == 3:
        if inputdata[15] != '':
            data_in_process_15 = []
            for n in circuit:
                data_in_process = []
                #print(n)
                if str(n[0]).upper() == str(inputdata[15]).upper():
                    data_in_process.append(n[0]) #circuit_id  added
                    for a in equipment:
                        if n[1] == a[0]:
                            data_in_process.append(a[1]) #project_name added
                            data_in_process.append(a[2]) #site_name added
                            data_in_process.append(a[0]) #serial_number added
                            break
                    data_in_process.append(n[5])     #Equipment_Loopback  added
                    data_in_process.append(n[3])   #IP_address_CE  added
                    circuit_search.append(data_in_process)
                    data_in_process_15.append(data_in_process)
                    break
            if len(data_in_process_15) == 0:
                #print(15) 
                inputdata[15] = str(inputdata[15])+"(NOT FOUND)"
        if inputdata[16] != '':
            if inputdata[15] == '':
                data_in_process_16 = []
                for n in circuit:
                    data_in_process = []
                    #print(n)
                    if str(n[3]).upper() == str(inputdata[16]).upper():
                        data_in_process.append(n[0]) #circuit_id  added
                        for a in equipment:
                            if n[1] == a[0]:
                                data_in_process.append(a[1]) #project_name added
                                data_in_process.append(a[2]) #site_name added
                                data_in_process.append(a[0]) #serial_number added
                                break
                        data_in_process.append(n[5])     #Equipment_Loopback  added
                        data_in_process.append(n[3])   #IP_address_CE  addedd
                        data_in_process_16.append(data_in_process)
                        if data_in_process in circuit_search:
                            pass
                        else:
                            circuit_search.append(data_in_process)
                            break
                if len(data_in_process_16) == 0:
                    inputdata[16] = str(inputdata[16])+"(NOT FOUND)"
            else:
                data_in_process_16 = []
                for n in circuit:
                    data_in_process = []
                    #print(n)
                    if str(n[3]).upper() == str(inputdata[16]).upper() and str(n[0]).upper() == str(inputdata[15]).upper():
                        data_in_process.append(n[0]) #circuit_id  added
                        for a in equipment:
                            if n[1] == a[0]:
                                data_in_process.append(a[1]) #project_name added
                                data_in_process.append(a[2]) #site_name added
                                data_in_process.append(a[0]) #serial_number added
                                break
                        data_in_process.append(n[5])     #Equipment_Loopback  added
                        data_in_process.append(n[3])   #IP_address_CE  addedd
                        data_in_process_16.append(data_in_process)
                        if data_in_process in circuit_search:
                            pass
                        else:
                            circuit_search.append(data_in_process)
                            break
                if len(data_in_process_16) == 0:
                    inputdata[16] = str(inputdata[16])+"(NOT FOUND)"
        if inputdata[17] != '':
            if inputdata[15] == '':
                data_in_process_17 = []
                for n in circuit:
                        data_in_process = []
                        #print(n)
                        if str(n[5]).upper() == str(inputdata[17]).upper():
                            data_in_process.append(n[0]) #circuit_id  added
                            for a in equipment:
                                if n[1] == a[0]:
                                    data_in_process.append(a[1]) #project_name added
                                    data_in_process.append(a[2]) #site_name added
                                    data_in_process.append(a[0]) #serial_number added
                                    break
                            data_in_process.append(n[5])     #Equipment_Loopback  added
                            data_in_process.append(n[3])   #IP_address_CE  addedd
                            data_in_process_17.append(data_in_process)
                            if data_in_process in circuit_search:
                                pass
                            else:
                                circuit_search.append(data_in_process)
                                break
                if len(data_in_process_17) == 0:
                    inputdata[17] = str(inputdata[17])+"(NOT FOUND)"
            else:
                data_in_process_17 = []
                for n in circuit:
                        data_in_process = []
                        #print(n)
                        if str(n[5]).upper() == str(inputdata[17]).upper() and str(n[0]).upper() == str(inputdata[15]).upper():
                            data_in_process.append(n[0]) #circuit_id  added
                            for a in equipment:
                                if n[1] == a[0]:
                                    data_in_process.append(a[1]) #project_name added
                                    data_in_process.append(a[2]) #site_name added
                                    data_in_process.append(a[0]) #serial_number added
                                    break
                            data_in_process.append(n[5])     #Equipment_Loopback  added
                            data_in_process.append(n[3])   #IP_address_CE  addedd
                            data_in_process_17.append(data_in_process)
                            if data_in_process in circuit_search:
                                pass
                            else:
                                circuit_search.append(data_in_process)
                                break
                if len(data_in_process) == 0:
                    inputdata[17] = str(inputdata[17])+"(NOT FOUND)"
            if inputdata[18] != '':
                if inputdata[15] == '':
                    data_in_process_18 = []
                    for n in circuit:
                        data_in_process = []
                        #print(n)
                        if str(n[-2]).upper() == str(inputdata[18]).upper():
                            data_in_process.append(n[0]) #circuit_id  added
                            for a in equipment:
                                if n[1] == a[0]:
                                    data_in_process.append(a[1]) #project_name added
                                    data_in_process.append(a[2]) #site_name added
                                    data_in_process.append(a[0]) #serial_number added
                                    break
                            data_in_process.append(n[5])     #Equipment_Loopback  added
                            data_in_process.append(n[3])   #IP_address_CE  addedd
                            data_in_process_18.append(data_in_process)
                            if data_in_process in circuit_search:
                                pass
                            else:
                                circuit_search.append(data_in_process)
                    if len(data_in_process_18) == 0:
                        inputdata[18] = str(inputdata[18])+"(NOT FOUND)"
                else:
                    data_in_process_18 = []
                    for n in circuit:
                        data_in_process = []
                        #print(n)
                        if str(n[-2]).upper() == str(inputdata[18]).upper() and str(n[0]).upper() == str(inputdata[15]).upper():
                            data_in_process.append(n[0]) #circuit_id  added
                            for a in equipment:
                                if n[1] == a[0]:
                                    data_in_process.append(a[1]) #project_name added
                                    data_in_process.append(a[2]) #site_name added
                                    data_in_process.append(a[0]) #serial_number added
                                    break
                            data_in_process.append(n[5])     #Equipment_Loopback  added
                            data_in_process.append(n[3])   #IP_address_CE  addedd
                            data_in_process_18.append(data_in_process)
                            if data_in_process in circuit_search:
                                pass
                            else:
                                circuit_search.append(data_in_process)
                    if len(data_in_process_18) == 0:
                        inputdata[18] = str(inputdata[18])+"(NOT FOUND)"

print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
print('input by equipment',inputdata[8:15])
print('datatable by equipment')
for i in equipment_search:
    print(i)


print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
print('input by circuit',inputdata[15:])

print('datatable by circuit')
for i in circuit_search:
    print(i)