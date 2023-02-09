from flask import Flask, render_template, request, redirect, url_for, session,Markup,jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import random
from datetime import date
import datetime
from sqlalchemy import Column,Integer,String,Date 
import re
import json
import ast
import os
import http.client
import mimetypes
import pandas as pd

app = Flask(__name__)
app.secret_key = 'how_to_be_got_A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pplus1234@127.0.0.1:5432/python2565'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = "noc_project/upload/"
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['xlsx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    user_id = 0
    role = ""
    newpass =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = psycopg2.connect(user="postgres",
                                    password="pplus1234",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="python2565")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchall()
        for row in account:
            user_id += row[0]
            role += row[3]
        if account:
            session['loggedin'] = True
            session['user_id'] = user_id
            for i in password:
                i = '*'
                newpass += i
            session['password'] = newpass
            session['username'] = username
            session['role'] = role
            cursor.execute('SELECT * FROM circuit')
            circuit = cursor.fetchall()
            session['circuit'] = circuit
            cursor.execute('SELECT * FROM equipment')
            equipment = cursor.fetchall()
            session['equipment'] = equipment
            cursor.execute('SELECT * FROM interface')
            interface = cursor.fetchall()
            session['interface'] = interface
            cursor.execute('SELECT * FROM project')
            project = cursor.fetchall()
            session['project'] = project
            cursor.execute('SELECT * FROM contract')
            contrat = cursor.fetchall()
            session['contrat'] = contrat
            cursor.execute('SELECT * FROM site')
            site = cursor.fetchall()
            session['site'] = site
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/check_test',methods=["POST","GET"])
def check_test():
    if request.method == 'POST':
        msg_data = request.form
        print(msg_data)
    return render_template('upload.html')

@app.route('/check_cell',methods=["POST","GET"])
def check_cell():
    msg = 'test'
    if request.method == 'POST':
        msg = check_data()
    return jsonify({'htmlcheck_cell': render_template('check_cell.html',msg = msg)})



def check_data():
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

    msg_new = ["","","","","",""]
    msg_old = ["","","","","",""]
    msg_project_old = ''
    msg_project_update = ''
    # project table check
    for i in project_data:
        p_new = i[0]
        count = 0
        for x in project:
            p_old = x[0]
            if p_new == p_old:
                count += 1
                if i[0] == x[0] and i[1] == x[1] and i[2] == x[2] and i[3] == x[3] and i[4] == x[4] and i[5] == x[5] and i[6] == x[6] and i[7] == x[7] and i[8] == x[8] and i[9] == x[9]:
                    msg_project_old += p_new+' already in database\n'
                else:
                    msg_project_update += p_new+' will update\n'
                break
        if count == 0:
            msg_project_update += p_new+' new data\n'

    if len(msg_project_update) != 0:
        msg_project_update = msg_project_update[:-1]
    if len(msg_project_old) != 0:
        msg_project_old = msg_project_old[:-1]
    msg_project_old = str(msg_project_old).replace("\n"," <br/> ")
    msg_project_update = str(msg_project_update).replace("\n"," <br/> ")
    msg_project_old = Markup(msg_project_old)
    msg_project_update = Markup(msg_project_update)
    msg_new[0] = msg_project_update
    msg_old[0] = msg_project_old

    msg_contract_old = ''
    msg_contract_update = ''
    # project table check
    for i in contract_data:
        #print(i)
        con_new = ['','']
        con_new[0] = i[0]
        con_new[1] = i[1]
        count = 0
        for x in contract:
            con_old = ['','']
            con_old[0] = x[1]
            con_old[1] = x[2]
            if con_new[0] == con_old[0] and con_new[1] == con_old[1]:
                count += 1
                if i[0] == x[1] and i[1] == x[2] and i[2] == x[3] and i[3] == x[4] and i[4] == x[5]:
                    msg_contract_old += con_new[0]+","+con_new[1]+' already in database\n'
                else:
                    msg_contract_update += con_new[0]+","+con_new[1]+' will update\n'
                break
        if count == 0:
            msg_contract_update += con_new[0]+","+con_new[1]+' new data\n'
            
    if len(msg_contract_update) != 0:
        msg_contract_update = msg_contract_update[:-1]
    if len(msg_contract_old) != 0:
        msg_contract_old = msg_contract_old[:-1]
    msg_contract_old = str(msg_contract_old).replace("\n"," <br/> ")
    msg_contract_update = str(msg_contract_update).replace("\n"," <br/> ")
    msg_contract_old = Markup(msg_contract_old)
    msg_contract_update = Markup(msg_contract_update)
    msg_new[1] = msg_contract_update
    msg_old[1] = msg_contract_old


    msg_site_old = ''
    msg_site_update = ''
    # project table check
    for i in site_data:
        s_new = ['','']
        s_new[0] = i[0]
        s_new[1] = i[1]
        count = 0
        for x in site:
            s_old = ['','']
            s_old[0] = x[1]
            s_old[1] = x[2]
            if s_new[0] == s_old[0] and s_new[1] == s_old[1]:
                if i[0] == x[1] and i[1] == x[2] and i[2] == x[3] and i[3] == x[4] and i[4] == x[5] and i[5] == x[6] and i[6] == x[7]:
                    msg_site_old += s_new[0]+","+s_new[1]+' already in database\n'
                else:
                    msg_site_update += s_new[0]+","+s_new[1]+' will update\n'
                break
        if count == 0:
            msg_site_update += s_new[0]+","+s_new[1]+' new data\n'
    
    if len(msg_site_update) != 0:
        msg_site_update = msg_site_update[:-1]
    if len(msg_site_old) != 0:
        msg_site_old = msg_site_old[:-1]
    msg_site_old = str(msg_site_old).replace("\n"," <br/> ")
    msg_site_update = str(msg_site_update).replace("\n"," <br/> ")
    msg_site_old = Markup(msg_site_old)
    msg_site_update = Markup(msg_site_update)
    msg_new[2] = msg_site_update
    msg_old[2] = msg_site_old


    msg_equipment_old = ''
    msg_equipment_update = ''
    # equipment table check
    for i in equipment_data:
        e_new = i[1]
        #print(e_new)
        count = 0
        for x in equipment:
            e_old = x[0]
            if e_old == e_new:
                count += 1
                print(i[0],x[2])
                print(i[1],x[0])
                print(i[2],x[3])
                print(i[3],x[4])
                print(i[4],x[5])
                print(i[5],x[6])
                print(i[6],x[7])
                print(i[7],x[8])
                print(i[8],x[9])
                print(i[9],x[11])
                print(i[10],x[-2])
                print(i[11],x[1])
                print("***")
                if i[0] == x[2] and i[1] == x[0] and i[2] == x[3] and i[3] == x[4] and i[4] == x[5] and i[5] == x[6] and i[6] == x[7] and i[7] == x[8] and i[8] == x[9] and i[9] == x[11] and i[10] == x[-2] and i[11] == x[1]:
                    msg_equipment_old += e_new+' already in database\n'
                    break
                else:
                    msg_equipment_update += e_new+' will update\n'
        if count == 0:
            msg_equipment_update += e_new+' new data\n'
    if len(msg_equipment_update) != 0:
        msg_equipment_update = msg_equipment_update[:-1]
    if len(msg_equipment_old) != 0:
        msg_equipment_old = msg_equipment_old[:-1]
    msg_equipment_old = str(msg_equipment_old).replace("\n"," <br/> ")
    msg_equipment_update = str(msg_equipment_update).replace("\n"," <br/> ")
    msg_equipment_old = Markup(msg_equipment_old)
    msg_equipment_update = Markup(msg_equipment_update)
    msg_new[3] = msg_equipment_update
    msg_old[3] = msg_equipment_old


    msg_circuit_old = ''
    msg_circuit_update = ''
    # equipment table check
    for i in circuit_data:
        cir_new = i[1]
        count = 0
        for x in circuit:
            cir_old = x[0]
            if cir_new == cir_old:
                count += 1
                # print(i)
                # print(x)
                if i[0] == x[1] and i[1] == x[0] and i[2] == x[2] and i[3] == x[3] and i[4] == x[4] and i[5] == x[5] and i[6] == x[6] and i[7] == x[7] and i[8] == x[8] and i[9] == x[9] and i[10] == x[10] and i[11] == x[11]: 
                    msg_circuit_old += cir_new+' already in database\n'
                else:
                    msg_circuit_update += cir_new+' will update\n'
                break
        if count == 0:
            msg_circuit_update += cir_new+' new data\n'
    if len(msg_circuit_update) != 0:
        msg_circuit_update = msg_circuit_update[:-1]
    if len(msg_circuit_old) != 0:
        msg_circuit_old = msg_circuit_old[:-1]
    msg_circuit_old = str(msg_circuit_old).replace("\n"," <br/> ")
    msg_circuit_update = str(msg_circuit_update).replace("\n"," <br/> ")
    msg_circuit_old = Markup(msg_circuit_old)
    msg_circuit_update = Markup(msg_circuit_update)
    msg_new[4] = msg_circuit_update
    msg_old[4] = msg_circuit_old



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
    #print(msg_interface[:-1])
    msg_list = [msg_new,msg_old]
    return msg_list

@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        #circuit_data = request.get_json()
        circuit_data = request.form['circuit_data']
        #print(circuit_data)
        circuit = session['circuit']
        equipment = session['equipment']
        interface = session['interface']
        site = session['site']
        project = session['project']
        contrat = session['contrat']
        res = ast.literal_eval(circuit_data)
        # printing final result and its type
        # print(res)
        if len(res[0]) == 1:
            zone1 = [res[0][0]] #Project Name
            zone2 = [] #Detial circuit ทั้งหมด
            zone3 = ["null","null","null"] #Equipment Model ,Equipment Brand ,Serial_number
            zone4 = ["null","null"] #Physical Interface , VLAN_ID , Tunnel Interface Name
            for i in circuit:
                if i[0] == res[1]:
                    zone2 = i
                    zone3[-1] = i[1]
                    break
            for i in equipment:
                if i[0] == zone3[-1]:
                    zone3[0] = i[4]
                    zone3[1] = i[3]
                    break
            for i in interface:
                if i[1] == res[1]:
                    zone4[0] = i[-3]
                    zone4[1] = i[-2]
                    zone4.append(i[-1])
                            # if '\n' in zone4[-1]:
                            #     zone4[-1] = str(zone4[-1]).replace("\n"," <br /> ")
                            # else:
                            #     pass
                    break
            if len(zone4) == 0:
                zone5 = ['null']
            elif '\n' in zone4[-1]:
                zone4[-1] = zone4[-1].split("\n")
                zone5 = zone4[-1]
            elif '\n' not in zone4[-1]:
                zone5 = []
                zone5.append(zone4[-1])
            else:
                zone5 = ['null']
            zone5_num = len(zone5)
            return jsonify({'htmlcircuit_detial': render_template('circuit_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5,zone5_num = zone5_num)})
        else:
            data = []
            data.append(res[0])
            index = res[0].index(res[1])
            if index == 0: #circuit_ID
                zone1 = [res[0][1]] #Project Name
                zone2 = [] #Detial circuit ทั้งหมด
                zone3 = ["null","null","null"] #Equipment Model ,Equipment Brand ,Serial_number
                zone4 = ["null","null"] #Physical Interface , VLAN_ID , Tunnel Interface Name
                for i in circuit:
                    if i[0] == res[1]:
                        zone2 = i
                        zone3[-1] = i[1]
                        break
                for i in equipment:
                    if i[0] == zone3[-1]:
                        zone3[0] = i[4]
                        zone3[1] = i[3]
                        break
                for i in interface:
                    if i[1] == res[1]:
                        zone4[0] = i[-3]
                        zone4[1] = i[-2]
                        zone4.append(i[-1])
                        break
                if len(zone4) == 0:
                    zone5 = ['null']
                elif '\n' in zone4[-1]:
                    zone4[-1] = zone4[-1].split("\n")
                    zone5 = zone4[-1]
                elif '\n' not in zone4[-1]:
                    zone5 = []
                    zone5.append(zone4[-1])
                else:
                    zone5 = ['null']
                zone5_num = len(zone5)
                return jsonify({'htmlcircuit_detial': render_template('circuit_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5,zone5_num = zone5_num)})
            elif index == 1:
                    zone1 = [res[1],res[0][0],res[0][3]] #Project Name , circuit_Id ,Serial_number 
                    zone2 = [] #project detials
                    zone3 = [] #contrat
                    for i in project:
                        i = list(i)
                        if i[0] == res[1]:
                            i[2] = i[2].strftime("%d/%m/%y")
                            i[3] = i[3].strftime("%d/%m/%y")
                            i[4] = i[4].strftime("%d/%m/%y")
                            i[5] = i[5].strftime("%d/%m/%y")
                            for a in i:
                                a = str(a).replace("\n"," <br/> ")
                                a = Markup(a)
                                zone2.append(a)
                                #print(zone2)
                            break
                        #print(zone2)
                    for i in contrat:
                        if i[1] == res[1]:
                            conlist = []
                            for a in i:
                                a = str(a).replace("\n"," <br/> ")
                                a = Markup(a)   
                                conlist.append(a)
                            zone3.append(conlist)

                        #print(zone3)
                        #zone4 = zone3[-1]
                        # zone4 = str(zone3[0]).replace("\n"," <br/> ")
                        # zone4 = Markup(zone4)
                        
                    return jsonify({'htmlproject_detial': render_template('project_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3)})
            elif index == 2:
                    zone1 = [res[0][1],res[0][0],res[0][3]] #Project Name , circuit_Id ,Serial_number
                    zone2 = [] #site detials
                    for i in site:
                        if i[1] == zone1[0] and i[2] == res[1]:
                            for a in i:
                                a = str(a).replace("\n"," <br/> ")
                                a = Markup(a)
                                zone2.append(a) 
                            break
                    return jsonify({'htmlsite_detial': render_template('site_detial.html',zone1 = zone1,zone2 = zone2)})
            elif index == 3: #Serial_number
                    zone1 = [res[0][1]] #Project Name
                    zone2 = [] #Detial Equipment
                    zone3 = [] #Site_name
                    zone4 = [] #Circuit_ID  list
                    for i in equipment:
                        #print(i[0],res[1])
                        if i[0] == res[1]:
                            zone2 = i
                            zone2 = list(zone2)
                            try:
                                zone2[-3] = zone2[-3].strftime("%d/%m/%y")
                                zone2[-4] = zone2[-4].strftime("%d/%m/%y")
                            except: 
                                pass
                            break
                    for i in site:
                            #print(i)
                        if i[1] == zone2[1] and i[2] == zone2[2]:
                            zone3 = i
                            break
                    for i in circuit:
                        if i[1] == res[1]:
                            zone4.append(i[0])
                    zone4_num = len(zone4)
                    return jsonify({'htmlserial_number_detial': render_template('serial_number_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone4_num=zone4_num)})


@app.route('/noc_project/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


def search(inputdata):
    circuit = session['circuit']
    equipment = session['equipment']
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
            data_in_process = ["","","","","",""]
            if str(a[2]).upper() == str(inputdata).upper():
                data_in_process[2] = a[2] #site_name added
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
            data_in_process = ["","","","","",""]
            if str(i[0]).upper() == str(inputdata).upper():
                data_in_process[3] = i[0] #serial_number added
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
    circuit = session['circuit']
    equipment = session['equipment']
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
        for a in i:
            if inputdata in a or inputdata.lower() in a:
                data2.append(i)
                break
    return(data2)


@app.route('/noc_project/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        data = []
        if request.method == "POST" and 'data_search' in request.form:
            search_data = request.form['data_search']
            #data_time = request.form['data_time']
            # print(data_time)
            # print(type(data_time))
            data = search(search_data)
            if len(data) == 0:
                msg = "Not Found"
            else:
                msg = "We Found"
            return render_template('home.html', text=msg ,data = data)
        return render_template('home.html', text='Hello '+str(session['role']),data = data)
    return redirect(url_for('login'))

@app.route('/noc_project/advance_search', methods=['GET', 'POST'])
def advanced_search():
    main_table = []
    project = session['project']
    equipment = session['equipment']
    site = session['site']
    site2 = [[],[]]
    circuit = session['circuit']
    circuit2 = []
    equipment2 = [[],[],[],[]]
    circuit_table = []
    equipment_table = []
    project_table = []
    site_table = []
    for i in site:
        if i[2] not in site2[0] and i[2] != "-":
            site2[0].append(i[2])
        if i[-1] not in site2[-1] and i[-1] != "-":
            site2[-1].append(i[-1])
    for i in circuit:
        if i[-2] not in circuit2 and i[-2] != "-":
            circuit2.append(i[-2])
    for i in equipment:
        if i[3] not in equipment2[0] and i[3] != "-":
            equipment2[0].append(i[3])
        if i[4] not in equipment2[1] and i[4] != "-":
            equipment2[1].append(i[4])
        if i[5] not in equipment2[2] and i[5] != "-":
            equipment2[2].append(i[5])
        if i[-2] not in equipment2[3] and i[-2] != "-":
            equipment2[3].append(i[-2])
    if request.method == "POST":
        inputdata = [request.form['project_name'],request.form['s_o'],request.form['customer_start_contract'],
        request.form['customer_end_contract'],request.form['disty_Start_contract'],request.form['disty_End_contract'],

        request.form['site_name'],request.form['site_type'],

        request.form['serial_number'],request.form['equipment_brand'],request.form['equipment_model'],
        request.form['disty_name'],request.form['start_of_warranty'],request.form['end_of_warranty'],request.form['ha_status'],

        request.form['circuit_id'],request.form['ip_address_ce'],request.form['ip_loopback'],request.form['owner_isp']]
        table_data = adv_search(inputdata)
        main_table = table_data[0]
        circuit_table = table_data[1]
        equipment_table = table_data[2]
        project_table = table_data[3]
        site_table = table_data[4]

    return render_template('advanced_search.html', text='Hello '+str(session['role']),main_table = main_table,project=project,
    equipment = equipment,equipment2=equipment2,circuit=circuit,circuit2=circuit2,site2 = site2 ,project_table = project_table,
    site_table = site_table,equipment_table = equipment_table,circuit_table= circuit_table)

@app.route('/noc_project/serial_number_detial', methods=['GET', 'POST'])
def serial_number_detial():
    if request.method == "POST" and 'data' in request.form:
        connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM circuit')
        circuit = cursor.fetchall()
        cursor.execute('SELECT * FROM equipment')
        equipment = cursor.fetchall()
        cursor.execute('SELECT * FROM interface')
        interface = cursor.fetchall()
        a = request.form['data']
        res = ast.literal_eval(a)
        zone1 = [res[0][0]] #Project Name
        zone2 = [] #Detial circuit ทั้งหมด
        zone3 = ["null","null","null"] #Equipment Model ,Equipment Brand ,Serial_numbe
        zone4 = ["null","null"] #Physical Interface , VLAN_ID , Tunnel Interface Name
        for i in circuit:
            if i[0] == res[1]:
                zone2 = i
                zone3[-1] = i[1]
                break
        for i in equipment:
            if i[0] == zone3[-1]:
                zone3[0] = i[4]
                zone3[1] = i[3]
                break
        for i in interface:
            if i[1] == res[1]:
                zone4[0] = i[-3]
                zone4[1] = i[-2]
                zone4.append(i[-1])
                        # if '\n' in zone4[-1]:
                        #     zone4[-1] = str(zone4[-1]).replace("\n"," <br /> ")
                        # else:
                        #     pass
                break
        if len(zone4) == 0:
            zone5 = ['null']
        elif '\n' in zone4[-1]:
            zone4[-1] = zone4[-1].split("\n")
            zone5 = zone4[-1]
        elif '\n' not in zone4[-1]:
            zone5 = []
            zone5.append(zone4[-1])
        else:
            zone5 = ['null']
        return render_template('circuit_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5)
@app.route('/noc_project/register_user', methods=['GET', 'POST'])
def register_user():
    if 'admin' in session['role'] or 'super_user' in session['role']:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
            A_username = request.form['username']
            A_password = request.form['password']
            A_role = request.form['role']
            print(A_role)
            connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (A_username,))
            account = cursor.fetchone()
            if account:
                return render_template('home.html',text='User already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', A_username):
                return render_template('home.html',text='Invalid email address!')
            elif A_role == "none":
                return render_template('home.html',text='Please select Role')
            else:
                postgres_insert_query = """ INSERT INTO accounts (username, password, role) VALUES (%s,%s,%s)"""
                cursor.execute(postgres_insert_query,(A_username,A_password,A_role))
                connection.commit()
                connection.close()
                return render_template('home.html',text='register successfully')
        return render_template('register_user.html')
    return redirect(url_for('login'))

@app.route('/noc_project/user_table', methods=['GET', 'POST'])
def user_table():
     if 'admin' in session['role'] or 'super_user' in session['role']:
        columns = ['Username', 'password', 'Role']
        session['columns'] = columns
        return render_template('user_table.html', columns=columns)

@app.route('/_server_data')
def get_server_data():
    
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM accounts')
    account = cursor.fetchall()
    name = []
    Role = []
    password = []
    for i in account:
        i = list(i)
        name.append(i[1])
        password.append(i[2])
        Role.append(i[3])
    cursor.close()
    connection.close()
    collection = []
    columns = session['columns']
    for i in range(len(name)):
        collection.append(dict(zip(columns,[name[i],password[i],Role[i]])))

    results = BaseDataTables(request, columns, collection).output_result()
    
    return json.dumps(results)

class BaseDataTables:
    
    def __init__(self, request, columns, collection):
        
        self.columns = columns

        self.collection = collection
         
        self.request_values = request.values
         
 
        self.result_data = None
         
        self.cardinality_filtered = 0
 
        self.cadinality = 0
 
        self.run_queries()
    
    def output_result(self):
        
        output = {}

        aaData_rows = []
        
        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)):
                aaData_row.append(str(row[ self.columns[i] ]).replace('"','\\"'))
            aaData_rows.append(aaData_row)
            
        output['aaData'] = aaData_rows
        
        return output
    
    def run_queries(self):
        
         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)

#@app.route('/upload_file', methods = ['GET', 'POST']) 
#def upload_file():
    """ namefile = []
    dir_path = r'test/upload/'
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            #count += 1
            namefile.append(path) """
    #return render_template('index.html' ,namefile = namefile)

@app.route('/noc_project/page_upload', methods = ['GET', 'POST'])
def page_upload():
    return render_template('upload.html') 

@app.route('/python-flask-files-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	files = request.files.getlist('files[]')
	
	errors = {}
	success = False
	for file in files:
    
		if file and allowed_file(file.filename):
            
			filename = 'data_up_load.xlsx'
            
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 400
		return resp



@app.route('/noc_project/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', account=session)
    return redirect(url_for('login'))
 

def W_chack(sql):
    sql_str = sql
    sql_list = sql.split(' ')
    if "Where" not in sql_list:
        sql_str = sql_str+" Where"
        return(sql_str)
    else:
        sql_str = sql_str+" and"
        return(sql_str)


def adv_search(inputdata):
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    cursor = connection.cursor()
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
            if str(i[2]).upper() == str(n[2]).upper():
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


    #print(table_main)
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
        #print(table_main_data)
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

    table_list = [table_main_data,circuit_table,equipment_table,project_table,site_table]
    return table_list


if __name__ == '__main__' :
    app.run(debug=True)

