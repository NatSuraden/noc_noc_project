import pandas as pd
import psycopg2
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

ex_name_sheet = ['Project','Contract','Site','Equipment','Circuit','Interface']
for i in ex_name_sheet:
    data = pd.read_excel("noc_project/upload/data_up_load.xlsx",sheet_name=i)
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


#print(project_data[0])
#print(interface_data)



msg_project = ''
# project table check
for i in project_data:
    p_new = i[0]
    for x in project:
        p_old = x[0]
        if p_new == p_old:
            msg_project += p_new+' already in database\n'
print(msg_project[:-1])

msg_contract = ''
# project table check
for i in contract_data:
    con_new = ['','']
    con_new[0] = i[0]
    con_new[1] = i[1]
    for x in contract:
        con_old = ['','']
        con_old[0] = x[1]
        con_old[1] = x[2]
        if con_new == con_old:
            msg_contract += con_new[0]+","+con_new[1]+' already in database\n'
            break
print(msg_contract[:-1])

msg_site = ''
# project table check
for i in site_data:
    s_new = ['','']
    s_new[0] = i[0]
    s_new[1] = i[1]
    for x in site:
        s_old = ['','']
        s_old[0] = x[1]
        s_old[1] = x[2]
        if s_new == s_old:
            msg_site += s_new[0]+","+s_new[1]+' already in database\n'
            break
print(msg_site[:-1])




msg_equipment = ''
# equipment table check
for i in equipment_data:
    e_new = i[1]
    #print(e_new)
    for x in equipment:
        e_old = x[0]
        #print(e_old)
        if e_new == e_old:
            msg_equipment += e_new+' already in database\n'
            break
print(msg_equipment[:-1])


msg_circuit = ''
# equipment table check
for i in circuit_data:
    cir_new = i[1]
    #print(e_new)
    for x in circuit:
        cir_old = x[0]
        #print(e_old)
        if cir_new == cir_old:
            msg_circuit += cir_new+' already in database\n'
            break
print(msg_circuit[:-1])



msg_interface = ''
# project table check
for i in interface_data:
    inter_new = ['','']
    inter_new[0] = i[0]
    inter_new[1] = i[1]
    for x in interface:
        inter_old = ['','']
        inter_old[0] = x[1]
        inter_old[1] = x[2]
        if inter_new == inter_old:
            msg_interface += inter_new[0]+","+inter_new[1]+' already in database\n'
            break
print(msg_interface[:-1])
        