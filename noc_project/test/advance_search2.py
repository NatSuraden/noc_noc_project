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
'FGT60FTK20054815','Fortinet','FG-60F','SiS Distribution (Thailand) PCL.','','','Yes','V53802','10.99.178.18','222','TRUE']
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
        pass
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

print('input',inputdata[15:])

print('datatable by circuit')
for i in circuit_search:
    print(i)