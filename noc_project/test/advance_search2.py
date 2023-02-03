import psycopg2
from datetime import datetime
connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
#circuit = 'J12418' "SELECT * FROM circuit WHERE circuit_id ='J12418'"
inputdata = ['','','','','','','','',
'','','','','','2024-09-02 00:00:00','','','','','']
def W_chack(sql):
    sql_str = sql
    sql_list = sql.split(' ')
    if "Where" not in sql_list:
        sql_str = sql_str+" Where"
        return(sql_str)
    else:
        sql_str = sql_str+" and"
        return(sql_str)
table_main = []
sql = "SELECT * FROM project"
pj_count = 0
if inputdata[0] != '':
    pj_count += 1
    sql = W_chack(sql)
    sql = sql+" project_name = '{}' ".format(inputdata[0])
    table_main.append(inputdata[0])
if inputdata[1] != '':
    pj_count += 1
    sql = W_chack(sql)
    sql = sql+" s_o = '{}' ".format(inputdata[1])
if inputdata[2] != '':
    pj_count += 1
    sql = W_chack(sql)
    sql = sql+" customer_start_of_contract >= '{}' ".format(inputdata[2])
if inputdata[3] != '':
    pj_count += 1
    sql = W_chack(sql)
    sql = sql+" customer_end_of_contract <= '{}' ".format(inputdata[3])
if inputdata[4] != '':
    pj_count += 1
    sql = W_chack(sql)
    sql = sql+" disty_start_of_contract >= '{}' ".format(inputdata[4])
if inputdata[5] != '':
    pj_count += 1
    sql = W_chack(sql)
    sql = sql+" disty_end_of_contract <= '{}' ".format(inputdata[5])    

if pj_count == 0:
    project = []
else:
    cursor.execute(sql)
    project = cursor.fetchall()


sql = "SELECT * FROM site"
s_count = 0
if inputdata[6] != '':
    s_count += 1
    sql = W_chack(sql)
    sql = sql+" site_name = '{}' ".format(inputdata[6])
    table_main.append(inputdata[6])
if inputdata[7] != '':
    s_count += 1
    sql = W_chack(sql)
    sql = sql+" type = '{}' ".format(inputdata[7])
if s_count == 0:
    site = []
else:
    cursor.execute(sql)
    site = cursor.fetchall()


sql = "SELECT * FROM equipment"
cursor.execute(sql)
equipment_all = cursor.fetchall() 
e_count = 0
if inputdata[8] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" serial_number = '{}' ".format(inputdata[8])
    table_main.append(inputdata[8])
if inputdata[9] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" brand = '{}' ".format(inputdata[9])
if inputdata[10] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" model = '{}' ".format(inputdata[10])
if inputdata[11] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" disty_name = '{}' ".format(inputdata[11])
if inputdata[12] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" start_of_warranty >= '{}' ".format(inputdata[12])
if inputdata[13] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" end_of_warranty <= '{}' ".format(inputdata[13])
if inputdata[14] != '':
    e_count += 1
    sql = W_chack(sql)
    sql = sql+" ha_status = '{}' ".format(inputdata[14])
if e_count == 0:
    equipment = []
else:
    cursor.execute(sql)
    equipment = cursor.fetchall()


sql = "SELECT * FROM circuit"
cursor.execute(sql)
circuit_all = cursor.fetchall()
c_count = 0
if inputdata[-4] != '':
    c_count += 1
    sql = W_chack(sql)
    sql = sql+" circuit_id = '{}' ".format(inputdata[-4])
    table_main.append(inputdata[-4])
if inputdata[-3] != '':
    c_count += 1
    sql = W_chack(sql)
    sql = sql+" ip_address_ce = '{}' ".format(inputdata[-3])
if inputdata[-2] != '':
    c_count += 1
    sql = W_chack(sql)
    sql = sql+" Loopback = '{}' ".format(inputdata[-2])
if inputdata[-1] != '':
    c_count += 1
    sql = W_chack(sql)
    sql = sql+" owner_isp = '{}' ".format(inputdata[-1])
#print(sql)
cursor.execute(sql)
circuit = cursor.fetchall()
#print(circuit)
if c_count == 0:
    circuit = []
else:
    cursor.execute(sql)
    circuit = cursor.fetchall()


circuit_table = []
for n in circuit:
    for i in circuit_all:
        data_in_process = []
        if str(i[0]).upper() == str(n[0]).upper():
            data_in_process.append(i[0]) #circuit_id  added
            for a in equipment_all:
                if i[1] == a[0]:
                    data_in_process.append(a[1]) #project_name added
                    data_in_process.append(a[2]) #site_name added
                    data_in_process.append(a[0]) #serial_number added
                    break
            data_in_process.append(i[5])     #Equipment_Loopback  added
            data_in_process.append(i[3])   #IP_address_CE  added
            circuit_table.append(data_in_process)
            break

equipment_table = []
for i in equipment:
    data_in_process = ["","","","","",""] #serial_number added
    if str(i[0]).upper() == str(i[0]).upper():
        data_in_process[3] = i[0]
        data_in_process[2] = i[2] #site_name added
        data_in_process[1] = i[1] #project_name added
        for x in circuit_all:
            if x[1] == data_in_process[3]:
                data_in_process[0] = x[0]   #circuit_id  added
                data_in_process[-2] = x[5]  #Equipment_Loopback  added
                data_in_process[-1] = x[3]  #IP_address_CE added
                break
        equipment_table.append(data_in_process)
#print(equipment_table)
# for i in equipment_table:
#     print(i)

site_table = []
for n in site:
    #print(n[1])
    for i in equipment_all:
        data_in_process = ["","","","","",""] #serial_number added
        #print(i[1])
        if str(i[1]).upper() == str(n[1]).upper():
            data_in_process[3] = i[0]
            data_in_process[2] = i[2] #site_name added
            data_in_process[1] = i[1] #project_name added
            for x in circuit_all:
                if x[1] == data_in_process[3]:
                    data_in_process[0] = x[0]   #circuit_id  added
                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                    data_in_process[-1] = x[3]  #IP_address_CE added
                    break
            site_table.append(data_in_process)
#print(site_table)

project_table = []
for n in project:
    #print(n[1])
    for i in equipment_all:
        data_in_process = ["","","","","",""] #serial_number added
        #print(i[1])
        if str(i[1]).upper() == str(n[0]).upper():
            data_in_process[3] = i[0]
            data_in_process[2] = i[2] #site_name added
            data_in_process[1] = i[1] #project_name added
            for x in circuit_all:
                if x[1] == data_in_process[3]:
                    data_in_process[0] = x[0]   #circuit_id  added
                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                    data_in_process[-1] = x[3]  #IP_address_CE added
                    break
            project_table.append(data_in_process)

#print(project_table)


print(table_main)
table_main_data = []
if len(table_main) == 4:
    for i in equipment_all:
        data_in_process = ["","","","","",""] #serial_number added
        if table_main[0] in i and table_main[1] in i and table_main[2] in i:
            data_in_process[2] = i[2] #site_name added
            data_in_process[1] = i[1] #project_name added
            for x in circuit_all:
                if x[0] == table_main[-1] and x[1] == table_main[2]:
                    data_in_process[3] = x[1]
                    data_in_process[0] = x[0]   #circuit_id  added
                    data_in_process[-2] = x[5]  #Equipment_Loopback  added
                    data_in_process[-1] = x[3]  #IP_address_CE added
                    table_main_data.append(data_in_process)
                    break
            #table_main_data.append(data_in_process)
    print(table_main_data)
if len(table_main) == 3:
    table_main_data = []
    for i in circuit_all:
        data_in_process = []
        data_in_process.append(i[0])     #circuit_id  added
        for a in equipment_all:
            if i[1] == a[0]:
                data_in_process.append(a[1]) #project_name added
                data_in_process.append(a[2]) #site_name added
                data_in_process.append(a[0]) #serial_number added
                break
        data_in_process.append(i[5])     #Equipment_Loopback  added
        data_in_process.append(i[3])   #IP_address_CE  added
        if table_main[0] in data_in_process and table_main[1] in data_in_process and table_main[2] in data_in_process:
            table_main_data.append(data_in_process)
if len(table_main) == 2:
    table_main_data = []
    for i in circuit_all:
        data_in_process = []
        data_in_process.append(i[0])     #circuit_id  added
        for a in equipment_all:
            if i[1] == a[0]:
                data_in_process.append(a[1]) #project_name added
                data_in_process.append(a[2]) #site_name added
                data_in_process.append(a[0]) #serial_number added
                break
        data_in_process.append(i[5])     #Equipment_Loopback  added
        data_in_process.append(i[3])   #IP_address_CE  added
        if table_main[0] in data_in_process and table_main[1] in data_in_process:
            table_main_data.append(data_in_process)
if len(table_main) == 1:
    table_main_data = []
    for i in circuit_all:
        data_in_process = []
        data_in_process.append(i[0])     #circuit_id  added
        for a in equipment_all:
            if i[1] == a[0]:
                data_in_process.append(a[1]) #project_name added
                data_in_process.append(a[2]) #site_name added
                data_in_process.append(a[0]) #serial_number added
                break
        data_in_process.append(i[5])     #Equipment_Loopback  added
        data_in_process.append(i[3])   #IP_address_CE  added
        if table_main[0] in data_in_process:
            table_main_data.append(data_in_process)
if len(table_main) == 0:
    table_main_data = []
    try:
        for i in circuit_table:
            if i not in table_main_data:
                table_main_data.append(i)
    except:
        pass
    try:
        for i in equipment_table:
            if i not in table_main_data:
                table_main_data.append(i)
    except:
        pass
    try:
        for i in project_table:
            if i not in table_main_data:
                table_main_data.append(i)
    except:
        pass
    try:
        for i in site_table:
            if i not in table_main_data:
                table_main_data.append(i)
    except:
        pass


for i in table_main_data:
    print(i)
