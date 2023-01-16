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
'FGT60FTK20054815','Fortinet','FG-60F','SiS Distribution (Thailand) PCL.','','','Yes','V53802','10.99.178.18','10.11.220.8','TRUE']
#print(inputdata) 
project_search = []
site_search = []
equipment_search = []
circuit_search = []
#data = []
for i in range(19):
    if i == 0:
        for x in equipment:
            data_in_process = ["","","","","",""] 
            if str(x[1]).upper() == str(inputdata[0]).upper():
                data_in_process[1] = x[1] #project_name added
                data_in_process[2] = x[2] #site_name added
                data_in_process[3] = x[0] #serial_number added 
                for a in circuit:
                    if a[1] == x[0]:
                        data_in_process[0] = a[0] #circuit_id  added
                        data_in_process[-2] = a[5] #Equipment_Loopback  added
                        data_in_process[-1] = a[3] #IP_address_CE added
                        break
                project_search.append(data_in_process)
    elif i == 1:
        for x  in project:
            if str(x[1]).upper() == str(inputdata[1]).upper():
                for g in equipment:
                    data_in_process = ["",x[0],"","","",""] #project_name added
                    if g[1] == data_in_process[1]:
                        data_in_process[2] = g[2] #site_name added
                        data_in_process[3] = g[0] #serial_number added 
                        for a in circuit:
                            if a[1] == g[0]:
                                data_in_process[0] = a[0] #circuit_id  added
                                data_in_process[-2] = a[5] #Equipment_Loopback  added
                                data_in_process[-1] = a[3] #IP_address_CE added
                                break
                        if data_in_process in project_search:
                            pass
                        else:
                            project_search.append(data_in_process)
    elif i == 2:
        pass
    elif i == 3:
        pass
    elif i == 4:
        pass
    elif i == 5:
        pass
    elif i == 6:
       for a in equipment:
            data_in_process = ["","","","","",""] #site_name added
            if str(a[2]).upper() == str(inputdata[6]).upper():
                data_in_process[2] = a[2]
                data_in_process[3] = a[0] #serial_number added 
                data_in_process[1] = a[1] #project_name added
                for b in circuit:
                    if b[1] == data_in_process[3]:
                        data_in_process[0] = b[0]   #circuit_id  added
                        data_in_process[-2] = b[5]  #Equipment_Loopback  added
                        data_in_process[-1] = b[3]  #IP_address_CE added
                        break
                site_search.append(data_in_process)
    elif i == 7:
        for n in site:
            if str(n[4]).upper() == str(inputdata[7]).upper():
                for a in equipment:
                    data_in_process = ["","",n[2],"","",""] #site_name added
                    if a[2] == data_in_process[2]:
                        data_in_process[2] = a[2]
                        data_in_process[3] = a[0] #serial_number added 
                        data_in_process[1] = a[1] #project_name added
                        for b in circuit:
                            if b[1] == data_in_process[3]:
                                data_in_process[0] = b[0]   #circuit_id  added
                                data_in_process[-2] = b[5]  #Equipment_Loopback  added
                                data_in_process[-1] = b[3]  #IP_address_CE added
                                break
                        if data_in_process in site_search:
                            pass
                        else:
                            site_search.append(data_in_process)
    elif i == 8:
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
                        break
                if data_in_process in equipment_search:
                    pass
                else:
                    equipment_search.append(data_in_process)
                    break
    elif i == 9:
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
                        break
                if data_in_process in equipment_search:
                    pass
                else:
                    equipment_search.append(data_in_process)
    elif i == 10:
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
                        break
                if data_in_process in equipment_search:
                    pass
                else:
                    equipment_search.append(data_in_process)
    elif i == 11:
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
                        break
                if data_in_process in equipment_search:
                    pass
                else:
                    equipment_search.append(data_in_process)
    elif i == 12:
        pass
    elif i == 13:
        pass
    elif i == 14:
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
    elif i == 15:
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
                break
    elif i == 16:
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
                if data_in_process in circuit_search:
                    pass
                else:
                    circuit_search.append(data_in_process)
                    break 
    elif i == 17:
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
                if data_in_process in circuit_search:
                    pass
                else:
                    circuit_search.append(data_in_process)
                    break
    elif i == 18:
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
                if data_in_process in circuit_search:
                    pass
                else:
                    circuit_search.append(data_in_process)
print("xxxxxxxxxxxxxxxxxxx")
for i in project_search:
    print(i)
print("xxxxxxxxxxxxxxxxxxx")
for i in site_search:
    print(i)
print("xxxxxxxxxxxxxxxxxxx")
for i in circuit_search:
    print(i)
print("xxxxxxxxxxxxxxxxxxx")
for i in equipment_search:
    print(i)