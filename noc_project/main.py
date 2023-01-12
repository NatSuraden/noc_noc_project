from flask import Flask, render_template, request, redirect, url_for, session,Markup
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

app = Flask(__name__)
app.secret_key = 'how_to_be_got_A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pplus1234@127.0.0.1:5432/python2565'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = "upload/"
db = SQLAlchemy(app)

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


@app.route('/noc_project/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


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
            data_in_process = [inputdata] #circuit_id  added
            if i[0] == data_in_process[0]:
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
            data_in_process = ["",inputdata,"","","",""] #project_name added
            if i[1] == inputdata:
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
            data_in_process = ["","",inputdata,"","",""] #site_name added
            if a[2] == data_in_process[2]:
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
            data_in_process = ["","","",inputdata,"",""] #serial_number added
            if i[0] == data_in_process[3]:
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
            #msg = 'Not Found data'
            break
    return(data)   
@app.route('/noc_project/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        data = []
        if request.method == "POST" and 'data_search' in request.form:
            search_data = request.form['data_search']
            data = search(search_data)
            if len(data) == 0:
                msg = "Not Found"
            else:
                msg = "We Found"
            return render_template('home.html', text=msg ,data = data)
        if request.method == "POST" and 'data' in request.form:
            circuit = session['circuit']
            equipment = session['equipment']
            interface = session['interface']
            site = session['site']
            project = session['project']
            contrat = session['contrat']
            msg = request.form['data']
            a = request.form['data']
            #print(a)
            res = ast.literal_eval(a)
            data = []
            data.append(res[0])
            index = res[0].index(res[1])
            # printing final result and its type
            if index == 0: #circuit_ID
                zone1 = [res[0][1]] #Project Name
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
                        #print(zone4[-1])
                return render_template('circuit_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5)
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
                
                return render_template('project_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3)
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
                return render_template('site_detial.html',zone1 = zone1,zone2 = zone2)

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
                return render_template('serial_number_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4)
            return render_template('home.html', text=msg ,data = data)
        return render_template('home.html', text='Hello '+str(session['role']),data = data)
    return redirect(url_for('login'))


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

@app.route('/noc_project/upload_file', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        print(filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)

        #file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        #content = file.read()   
        return render_template('home.html',text='upload {} successfully'.format(filename)) 
    return render_template('upload.html') 

@app.route('/noc_project/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', account=session)
    return redirect(url_for('login'))
 
if __name__ == '__main__' :
    app.run(debug=True)

