import psycopg2
# connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
# cursor = connection.cursor()
# display_list = []
# cursor.execute('SELECT * FROM circuit')
# circuit = cursor.fetchall()
# cursor.execute('SELECT * FROM equipment')
# equipment = cursor.fetchall()
# cursor.execute('SELECT * FROM site')
# site = cursor.fetchall()
# cursor.execute('SELECT * FROM project')
# project = cursor.fetchall()
# cursor.execute('SELECT * FROM interface')
# interface = cursor.fetchall()
# cursor.execute('SELECT * FROM contract')
# contract = cursor.fetchall()
def search(inputdata):
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM circuit')
    circuit = cursor.fetchall()
    cursor.execute('SELECT * FROM equipment')
    equipment = cursor.fetchall()
    data = []
    data_len = len(data)
    while data_len == 0:
        #search by circuit_id
        for i in circuit:
            data_in_process = []
            if str(i[0]).upper() == str(inputdata).upper():
                data_in_process.append(i[0]) #circuit_id  added
                for a in equipment:
                    if i[1] == a[0]:
                        data_in_process.append(a[1]) #project_name added
                        data_in_process.append(a[2]) #site_name added
                        data_in_process.append(a[0]) #serial_number added
                        break
                data_in_process.append(i[5])     #Equipment_Loopback  added
                data_in_process.append(i[3])   #IP_address_CE  added
                data.append(data_in_process)
                break
        #search by project_name
        data_len = len(data)
        for i in equipment:
            data_in_process = ["","","","","",""] 
            if str(i[1]).upper() == str(inputdata).upper():
                data_in_process[1] = i[1] #project_name added
                data_in_process[2] = i[2] #site_name added
                data_in_process[3] = i[0] #serial_number added 
                for a in circuit:
                    if a[1] == i[0]:
                        data_in_process[0] = a[0] #circuit_id  added
                        data_in_process[-2] = a[5] #Equipment_Loopback  added
                        data_in_process[-1] = a[3] #IP_address_CE added
                        break
                data.append(data_in_process)
        data_len = len(data)
        #search by site_name
        for a in equipment:
            data_in_process = ["","","","","",""] #site_name added
            if str(a[2]).upper() == str(inputdata).upper():
                data_in_process[2] = a[2]
                data_in_process[3] = a[0] #serial_number added 
                data_in_process[1] = a[1] #project_name added
                for x in circuit:
                    if x[1] == data_in_process[3]:
                        data_in_process[0] = x[0]   #circuit_id  added
                        data_in_process[-2] = x[5]  #Equipment_Loopback  added
                        data_in_process[-1] = x[3]  #IP_address_CE added
                        break
                data.append(data_in_process)
        data_len = len(data)
        #search by serial_number
        for i in equipment:
            data_in_process = ["","","","","",""] #serial_number added
            if str(i[0]).upper() == str(inputdata).upper():
                data_in_process[3] = i[0]
                data_in_process[2] = i[2] #site_name added
                data_in_process[1] = i[1] #project_name added
                for x in circuit:
                    if x[1] == data_in_process[3]:
                        data_in_process[0] = x[0]   #circuit_id  added
                        data_in_process[-2] = x[5]  #Equipment_Loopback  added
                        data_in_process[-1] = x[3]  #IP_address_CE added
                        break
                data.append(data_in_process)
        data_len = len(data)
        #search by IP
        for i in circuit:
            data_in_process = ["","","","",inputdata,""] #Equipment_Loopback  added
            if i[5] == data_in_process[4]:
                data_in_process[0] = i[0]   #circuit_id  added
                data_in_process[-1] = i[3]  #IP_address_CE added
                data_in_process[3] = i[1]   #serial_number added
                for x in equipment:
                    if x[0] == data_in_process[3]:
                        data_in_process[1] = x[1] #project_name added
                        data_in_process[2] = x[2] #site_name added
                        break
                data.append(data_in_process)
        data_len = len(data)
        for i in circuit:
            data_in_process = ["","","","","",inputdata] # IP_address_CE added
            if i[3] == data_in_process[-1]:
                data_in_process[0] = i[0]   #circuit_id  added
                data_in_process[-2] = i[5]  #IP_address_CE added
                data_in_process[3] = i[1]   #serial_number added
                for x in equipment:
                    if x[0] == data_in_process[3]:
                        data_in_process[1] = x[1] #project_name added
                        data_in_process[2] = x[2] #site_name added
                        break
                data.append(data_in_process)
        data_len = len(data)
        if data_len == 0:
            data = search2(inputdata)
            break
    return(data)          

def search2(inputdata):
    inputdata = str(inputdata).upper()
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM circuit')
    circuit = cursor.fetchall()
    cursor.execute('SELECT * FROM equipment')
    equipment = cursor.fetchall()
    data = []
    for i in circuit:
        data_in_process = []
        data_in_process.append(i[0])     #circuit_id  added
        for a in equipment:
            if i[1] == a[0]:
                data_in_process.append(a[1]) #project_name added
                data_in_process.append(a[2]) #site_name added
                data_in_process.append(a[0]) #serial_number added
                break
        data_in_process.append(i[5])     #Equipment_Loopback  added
        data_in_process.append(i[3])   #IP_address_CE  added
        data.append(data_in_process)
    data2 = []
    for i in data:
        #print(i)
        for a in i:
            if inputdata in a or inputdata.lower() in a:
                data2.append(i)
                break
    return(data2)

kgip = "Y"
while kgip == "Y":
    data_raw_input = input(str("search:> "))
    if data_raw_input == "":
        kgip = "N"
    else:
        data = search(data_raw_input)
        if len(data) == 0:
            print("Not Found")
        else:
            print("We Found")
            for i in data:
                print(i)