from flask import Flask, render_template, request, redirect, url_for, session,Markup,jsonify,send_from_directory,flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import random
from datetime import date
from datetime import datetime
import datetime
import numpy as np
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pplus1234@127.0.0.1:5432/pyreturnthon2565'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = "noc_test/noc_project/upload/"
#app.config["DOWNLOAD_FOLDER"] = "noc_project/test/"
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['xlsx'])

project_update = []
project_new = []
contract_update = []
contract_new = []

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
        connection = connect()
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
            global_data()
            event = 'Login'
            save_log(event)

            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/check_test',methods=["POST","GET"])
def check_test():
    if request.method == 'POST':
        submit_request = request.form['test']
        if submit_request == 'submit_done':
            try:
                global project_new,project_update,contract_new,contract_update,site_update,site_new,equipment_update,equipment_new,circuit_new,circuit_update
                global equipment,site,circuit,interface,project,contrat,interface_update,interface_new
                if session['in_cell_check'] == 0:
                    session['project_error'] = []
                    if len(project_update) != 0:
                        project_table_update(project_update)
                    if len(project_new) != 0:
                        project_table_new_data(project_new)
                    if len(contract_update) != 0:
                        contract_table_update(contract_update)
                    if len(contract_new) != 0:
                        contract_table_new_data(contract_new)
                    if len(site_update) != 0:
                        site_table_update(site_update)
                    if len(site_new) != 0:
                        site_table_new_data(site_new)
                    if len(equipment_update) != 0:
                        equipment_table_update(equipment_update)
                    if len(equipment_new) != 0:
                        equipment_table_new_data(equipment_new)
                    if len(circuit_update) != 0:
                        circuit_table_update(circuit_update)
                    if len(circuit_new) != 0:
                        circuit_table_new_data(circuit_new)
                    if len(interface_update) != 0:
                        interface_table_update(interface_update)
                    if len(interface_new) != 0:
                        interface_table_new_data(interface_new)
                        
                        #print(len(interface_new))
                    connection = connect()
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
                    contrat = cursor.fetchall()
                    cursor.execute('SELECT * FROM site')
                    site = cursor.fetchall()
                    cursor.close()
                    connection.close()
                    event = 'update data to database.'
                    save_log(event)
                else:
                    session['project_error'] = ['file xlsx not ready']
            except (Exception) as error:
                msg = []
                error = str(error)  
                msg.append(error)
                session['project_error'] += msg
                event = 'error update data to database.'
                save_log(event)
            if len(session['project_error']) != 0:
                # for i in session['project_error']:
                #     print(i)
                return render_template('upload.html',error = session['project_error'])
    return render_template('upload.html')

def project_table_new_data(data):
    
    try:
        connection = connect()
        #cursor = connection.cursor()
        #print(len(data))
        for i in data:
            msg = []
            cursor = connection.cursor()
            try:
                if i[2] != "-":
                    i[2] = i[2].strftime('%Y/%m/%d')
                    i[2] = datetime.datetime.strptime(i[2], '%Y/%m/%d')
                if i[3] != "-":
                    i[3] = i[3].strftime('%Y/%m/%d')
                    i[3] = datetime.datetime.strptime(i[3], '%Y/%m/%d')
                if i[4] != "-":
                    i[4] = i[4].strftime('%Y/%m/%d')
                    i[4] = datetime.datetime.strptime(i[4], '%Y/%m/%d')
                if i[5] != "-":
                    i[5] = i[5].strftime('%Y/%m/%d')
                    i[5] = datetime.datetime.strptime(i[5], '%Y/%m/%d')

                if i[2] == "-":
                    d = "2001/2/16"
                    i[2] = d
                    i[2] = datetime.datetime.strptime(i[2], '%Y/%m/%d')
                if i[3] == "-":
                    d = "2002/2/16"
                    i[3] = d
                    i[3] = datetime.datetime.strptime(i[3], '%Y/%m/%d')
                if i[4] == "-":
                    d = "2001/2/16"
                    i[4] = d
                    i[4] = datetime.datetime.strptime(i[4], '%Y/%m/%d')
                if i[5] == "-":
                    d = "2002/2/16"
                    i[5] = d
                    i[5] = datetime.datetime.strptime(i[5], '%Y/%m/%d')
                #print(data , 'new data')
                #print(i[0])
                cursor.execute('SELECT * FROM project WHERE project_name = %s ',(i[0],))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_project")
                else:
                    postgres_insert_query = """ INSERT INTO project (project_name,s_o,customer_start_of_contract,customer_end_of_contract,
                    disty_start_of_contract,disty_end_of_contract,vpn_detail,Important_Detail,
                    Addition_Detail,Remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]))
                    connection.commit()
            except (Exception) as error: 
                error = "project add",i[0],str(error)  
                msg.append(error)
                session['project_error'] += msg
                connection.close()
                connection = connect()
        cursor.close()
        connection.close()
    except (Exception) as error: 
        error = "project",str(error)  
        msg.append(error)
        session['project_error'] += msg

def project_table_update(data):
    connection = connect()
    cursor = connection.cursor()
    for data_update_project in data:
        #print(data_update_project)
        try:
            if data_update_project[1] != "-":
                sql_update_query = """Update project set s_o = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[1], data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "s_o",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[2] != "-":
                data_update_project[2] = data_update_project[2].strftime('%Y/%m/%d')
                date_2 = datetime.datetime.strptime(data_update_project[2], '%Y/%m/%d')
                sql_update_query = """Update project set customer_start_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_2, data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "customer_start_of_contract",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[3] != "-":
                data_update_project[3] = data_update_project[3].strftime('%Y/%m/%d')
                date_3 = datetime.datetime.strptime(data_update_project[3], '%Y/%m/%d')
                sql_update_query = """Update project set customer_end_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_3, data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "customer_end_of_contract",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[4] != "-":
                data_update_project[4] = data_update_project[4].strftime('%Y/%m/%d')
                date_4 = datetime.datetime.strptime(data_update_project[4], '%Y/%m/%d')
                #print(date_4)
                sql_update_query = """Update project set disty_start_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_4, data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "disty_start_of_contract",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[5] != "-":
                data_update_project[5] = data_update_project[5].strftime('%Y/%m/%d')
                date_5 = datetime.datetime.strptime(data_update_project[5], '%Y/%m/%d')
                sql_update_query = """Update project set disty_end_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_5, data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "disty_end_of_contract",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[6] != "-":
                sql_update_query = """Update project set vpn_detail = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[6], data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "vpn_detail",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[7] != "-":
                sql_update_query = """Update project set important_detail = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[7], data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "important_detail",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[8] != "-":
                sql_update_query = """Update project set addition_detail = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[8], data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "addition_detail",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_project[9] != "-":
                sql_update_query = """Update project set remark = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[9], data_update_project[0]))
                connection.commit()
        except (Exception) as error:
            error = "remark",data_update_project[0],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        # print(data_update_project)
        # print(msg)
    cursor.close()
    connection.close()

def contract_table_new_data(data):
    
    try:
        connection = connect()
        #cursor = connection.cursor()
        for i in data:
            msg = []
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT * FROM contract WHERE project_name = %s AND role = %s AND name = %s',(i[0],i[1],i[2],))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_contract")
                else:
                    postgres_insert_query = """ INSERT INTO contract (project_name,role,name,tel,
                    additional_detail) VALUES (%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4]))
                    connection.commit()
            except (Exception) as error:
                error = "contract add",i[0],i[2],str(error)  
                msg.append(error)
                session['project_error'] += msg
                connection.close()
                connection = connect()
        cursor.close()
        connection.close()
    except (Exception) as error:
        error = "contract",str(error)  
        msg.append(error)
        session['project_error'] += msg

def contract_table_update(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    for data_update_contract in data:
        # try:
        #     if data_update_contract[2] != "-":
        #         sql_update_query = """Update contract set name = %s where contrat_id = %s"""
        #         cursor.execute(sql_update_query, (data_update_contract[2], data_update_contract[-1]))
        #         connection.commit()
        # except (Exception) as error:
        #     error = "name",data_update_contract[0],data_update_contract[1],str(error)
        #     msg = []
        #     msg.append(error)
        #     session['project_error'] += msg
        try:
            if data_update_contract[3] != "-":
                sql_update_query = """Update contract set tel = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[3], data_update_contract[-1]))
                connection.commit()
        except (Exception) as error:
            error = "tel",data_update_contract[0],data_update_contract[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_contract[4] != "-":
                sql_update_query = """Update contract set additional_detail = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[4], data_update_contract[-1]))
                connection.commit()
        except (Exception) as error:
            error = "additional_detail",data_update_contract[0],data_update_contract[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
    cursor.close()
    connection.close()

def site_table_new_data(data):
    
    try:
        connection = connect()
        
        for i in data:
            msg = []
            try:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM site WHERE project_name = %s AND site_name = %s AND location = %s',(i[0],i[1],i[2],))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_site")
                else:
                    postgres_insert_query = """ INSERT INTO site (project_name,site_name,location,site_short_name,
                    contact_owner_site,contact,type) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                    connection.commit()
            except (Exception) as error:
                error = "add",i[0],i[1],str(error)  
                msg.append(error)
                session['project_error'] += msg
                connection.close()
                connection = connect()
        cursor.close()
        connection.close()
    except (Exception) as error:
        error = "site",str(error)  
        msg.append(error)
        session['project_error'] += msg

def site_table_update(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    for data_update_site in data:
        # try:
        #     if data_update_site[2] != "-":
        #         sql_update_query = """Update site set location = %s where site_id = %s"""
        #         cursor.execute(sql_update_query, (data_update_site[2], data_update_site[-1]))
        #         connection.commit()
        # except (Exception) as error:
        #     error = "location",data_update_site[2],data_update_site[3],str(error)
        #     msg = []
        #     msg.append(error)
        #     session['project_error'] += msg
        try:
            if data_update_site[3] != "-":
                sql_update_query = """Update site set site_short_name = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[3], data_update_site[-1]))
                connection.commit()
        except (Exception) as error:
            error = "site_short_name ",data_update_site[2],data_update_site[3],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_site[4] != "-":
                sql_update_query = """Update site set contact_owner_site = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[4], data_update_site[-1]))
                connection.commit()
        except (Exception) as error:
            error = "contact_owner_site",data_update_site[2],data_update_site[3],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_site[5] != "-":
                sql_update_query = """Update site set contact = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[5], data_update_site[-1]))
                connection.commit()
        except (Exception) as error:
            error = "contact",data_update_site[2],data_update_site[3],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_site[6] != "-":
                sql_update_query = """Update site set type = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[6], data_update_site[-1]))
                connection.commit()
        except (Exception) as error:
            error = "type",data_update_site[2],data_update_site[3],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
    cursor.close()
    connection.close()       

def equipment_table_new_data(data):
    #msg = []
    try:
        connection = connect()
        for i in data:
            connection = connect()
            msg = []
            try:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM equipment')
                equipment_for_count = cursor.fetchall()
                if i[1] == "-":
                    i[1] = str(len(equipment_for_count))
                if i[7] != "-":
                    i[7] = i[7].strftime('%Y/%m/%d')
                    i[7] = datetime.datetime.strptime(i[7], '%Y/%m/%d')
                if i[8] != "-":
                    i[8] = i[-4].strftime('%Y/%m/%d')
                    i[8] = datetime.datetime.strptime(i[8], '%Y/%m/%d')

                if i[7] == "-":
                    d = "2001/2/16"
                    i[7] = d
                    i[7] = datetime.datetime.strptime(i[7], '%Y/%m/%d')
                if i[8] == "-":
                    d = "2002/2/16"
                    i[8] = d
                    i[8] = datetime.datetime.strptime(i[8], '%Y/%m/%d')
                cursor.execute('SELECT * FROM equipment WHERE serial_number = %s AND site_name = %s AND project_name = %s',(i[1],i[0],i[-1],))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_equipment")
                    cursor.close()
                else:
                    postgres_insert_query = """ INSERT INTO equipment (serial_number, project_name,site_name, brand,model,disty_name,disty_contact,
                    open_case_contact,start_of_warranty,end_of_warranty,ha_status,ha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(i[1],i[-1],i[0],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    connection.commit()
                    # try:
                    #     postgres_insert_query = """ INSERT INTO equipment (serial_number, project_name,site_name, brand,model,disty_name,disty_contact,
                    #     open_case_contact,start_of_warranty,end_of_warranty,ha_status,ha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    #     cursor.execute(postgres_insert_query,(i[1],i[-1],i[0],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    #     connection.commit()
                    # except (Exception) as error:
                    #     error = "SUPER equipment add",i[0],str(error)  
                    #     msg.append(error)
                    #     session['project_error'] += msg
                    #     cursor.close()
                    #     connection.close()
                    #     connection = connect()
            except (Exception) as error:
                error = "equipment add",i[0],str(error)  
                msg.append(error)
                session['project_error'] += msg
                cursor.close()
                connection.close()
                connection = connect()
        cursor.close()
        connection.close()
    except (Exception) as error:
        error = "equipment",str(error)  
        msg.append(error)
        session['project_error'] += msg


def equipment_table_update(data):
    connection = connect()
    #cursor = connection.cursor()
    for data_update_equipment in data:
        cursor = connection.cursor()
        try:
            if data_update_equipment[0] != "-":
                sql_update_query = """Update equipment set site_name = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[0], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "site_name",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[2] != "-":
                sql_update_query = """Update equipment set brand = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[2], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "brand",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[3] != "-":
                sql_update_query = """Update equipment set model = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[3], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "model",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[4] != "-":
                sql_update_query = """Update equipment set disty_name = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[4], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "disty_name",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[5] != "-":
                sql_update_query = """Update equipment set disty_contact = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[5], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "disty_contact",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[6] != "-":
                sql_update_query = """Update equipment set open_case_contact = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[6], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "open_case_contact",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[7] != "-":
                data_update_equipment[7] = data_update_equipment[7].strftime('%Y/%m/%d')
                data_update_equipment[7] = datetime.datetime.strptime(data_update_equipment[7], '%Y/%m/%d')
                sql_update_query = """Update equipment set start_of_warranty = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[7], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "start_of_warranty",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[8] != "-":
                data_update_equipment[8] = data_update_equipment[8].strftime('%Y/%m/%d')
                date_8 = datetime.datetime.strptime(data_update_equipment[8], '%Y/%m/%d')
                sql_update_query = """Update equipment set end_of_warranty = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (date_8, data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "end_of_warranty",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[9] != "-":
                #print(data_update_equipment[9],print(type(data_update_equipment[9])))
                sql_update_query = """Update equipment set ha = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[9], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "ha",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[10] != "-":
                #print(data_update_equipment[10])
                sql_update_query = """Update equipment set ha_status = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[10], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "ha_status",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_equipment[11] != "-":
                sql_update_query = """Update equipment set project_name = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[11], data_update_equipment[1]))
                connection.commit()
        except (Exception) as error:
            error = "project_name",data_update_equipment[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
    cursor.close()
    connection.close()

def circuit_table_new_data(data):
   
    try:
        connection = connect()
        
        for i in data:
            msg = []
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT * FROM circuit')
                circuit_for_count = cursor.fetchall()
                if i[1] == "-":
                    i[1] = str(len(circuit_for_count))
                i[-3] = str(i[-3]).upper()
                i[-4] = str(i[-4]).upper()
                try:
                    i[7] = float(i[7])
                    i[7] = int(i[7])
                    i[7] = str(i[7])
                except:
                    pass
                #print(i)
                cursor = connection.cursor()
                #cursor.execute('SELECT * FROM circuit WHERE equipment_ref = %s AND owner_isp = %s', (a, b,))
                cursor.execute('SELECT * FROM circuit WHERE circuit_id = %s AND equipment_ref = %s AND ip_address_pe = %s',(str(i[1]),str(i[0]),str(i[2]),))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_circuit")
                else:
                    postgres_insert_query = """ INSERT INTO circuit (circuit_id, equipment_ref, ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
                    link_number,original_isp,owner_isp,isp_contact_tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(str(i[1]),str(i[0]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6]),
                    str(i[7]),str(i[8]),str(i[9]),str(i[10])))
                    connection.commit()
            except (Exception) as error:
                error = "add",i[1],str(error)  
                msg.append(error)
                session['project_error'] += msg
                connection.close()
                connection = connect()
        cursor.close()
        connection.close()
    except (Exception) as error:
        error = "circuit",str(error)  
        msg.append(error)
        session['project_error'] += msg

def circuit_table_update(data):
    connection = connect()
    cursor = connection.cursor()
    for data_update_circuit in data:
        try:
            if data_update_circuit[0] != "-":
                sql_update_query = """Update circuit set equipment_ref = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[0]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "equipment_ref",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[2] != "-":
                sql_update_query = """Update circuit set ip_address_pe = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[2]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "ip_address_pe",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[3] != "-":
                sql_update_query = """Update circuit set ip_address_ce = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[3]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "ip_address_ce",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[4] != "-":
                sql_update_query = """Update circuit set subnet = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[4]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "subnet",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[5] != "-":
                sql_update_query = """Update circuit set loopback = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[5]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "loopback",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[6] != "-":
                sql_update_query = """Update circuit set circuit_type = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[6]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "circuit_type",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[7] != "-":
                sql_update_query = """Update circuit set link_number = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[7]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "link_number",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[8] != "-":
                sql_update_query = """Update circuit set original_isp = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[8]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "original_isp",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[9] != "-":
                sql_update_query = """Update circuit set owner_isp = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[9]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "owner_isp",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_circuit[10] != "-":
                sql_update_query = """Update circuit set isp_contact_tel = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[10]), str(data_update_circuit[1])))
                connection.commit()
        except (Exception) as error:
            error = "isp_contact_tel",data_update_circuit[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
    cursor.close()
    connection.close()

def interface_table_new_data(data):
    
    try:
        connection = connect()
        msg = []
        for i in data:
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT * FROM interface WHERE circuit_id = %s AND equipment_serial = %s AND equipment_brand = %s',(str(i[0]),str(i[1]),str(i[2]),))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_interface")
                else:
                    postgres_insert_query = """ INSERT INTO interface (circuit_id,equipment_serial,equipment_brand,
                    equipment_model,physical_interface,vlan_id,tunnel_interface_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(str(i[0]),str(i[1]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6])))
                    connection.commit()
            except (Exception) as error:
                error = "add",i[0],i[1],str(error)  
                msg.append(error)
                session['project_error'] += msg
                connection.close()
                connection = connect()
        cursor.close()
        connection.close()
    except (Exception) as error:
        error = "interface",str(error)  
        msg.append(error)
        session['project_error'] += msg

def interface_table_update(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    for data_update_interface in data:
        try:
            if data_update_interface[2] != "-":
                sql_update_query = """Update interface set equipment_brand = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[2]), str(data_update_interface[-1])))
                connection.commit()
        except (Exception) as error:
            error = "equipment_brand",data_update_interface[0],data_update_interface[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_interface[3] != "-":
                sql_update_query = """Update interface set equipment_model = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[3]), str(data_update_interface[-1])))
                connection.commit()
        except (Exception) as error:
            error = "equipment_model",data_update_interface[0],data_update_interface[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_interface[4] != "-":
                sql_update_query = """Update interface set physical_interface = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[4]), str(data_update_interface[-1])))
                connection.commit()
        except (Exception) as error:
            error = "physical_interface",data_update_interface[0],data_update_interface[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_interface[5] != "-":
                sql_update_query = """Update interface set vlan_id = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[5]), str(data_update_interface[-1])))
                connection.commit()
        except (Exception) as error:
            error = "vlan_id",data_update_interface[0],data_update_interface[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
        try:
            if data_update_interface[6] != "-":
                sql_update_query = """Update interface set tunnel_interface_name = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[6]), str(data_update_interface[-1])))
                connection.commit()
        except (Exception) as error:
            error = "tunnel_interface_name",data_update_interface[0],data_update_interface[1],str(error)
            msg = []
            msg.append(error)
            session['project_error'] += msg
    cursor.close()
    connection.close()

@app.route('/noc_project/log', methods=['GET', 'POST'])
def log():
    if 'loggedin' in session:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM event_logs')
        log_table = cursor.fetchall()
        log_table = log_table[::-1]
        return render_template('act_log.html',log_table = log_table,username=session['username'])
    return redirect(url_for('log'))    

@app.route('/check_cell',methods=["POST","GET"])
def check_cell():
    try:
        if request.method == 'POST':
            msg = in_xlsx_duplicate()
            session['in_cell_check'] = msg[1]
            if msg[1] == 0:
                msg = check_data()
                return jsonify({'htmlcheck_cell': render_template('check_cell.html',msg = msg)})
            else:
                msg = msg
                return jsonify({'htmlin_cell': render_template('in_cell.html',msg = msg[0])})
        msg = [[]]
        return jsonify({'htmlcheck_cell': render_template('check_cell.html',msg = msg)})
    except Exception as error:
        msg = error
        return render_template('upload.html',error = msg)

def duplicateparameter(index,data):
    list1 = []
    duplicate= []
    missingparameter =[]
    data = data.values.tolist()
    count = 1
    count2 = 0
    for i in data:
        count += 1
        if i[index] != "-":
            if i[index] not in list1:
                list1.append(i[index])
            elif i[index] in list1:
                duplicate.append([count,i])
                count2 += 1
        else:
            missingparameter.append([count,i])
            count2 += 1
    total = [duplicate,missingparameter,count2]
    return total
def duplicateparameter2(name,data):
    list1 = []
    duplicate= []
    missingparameter =[]
    data = data.values.tolist()
    count = 1
    count2 = 0
    if name != 'Interface':
        for i in data:
            count += 1
            if i[0] != "-" and i[1] != "-" and i[2] != "-":
                if [i[0],i[1],i[2]] not in list1:
                    list1.append([i[0],i[1],i[2]])
                elif [i[0],i[1],i[2]] in list1:
                    duplicate.append([count,i])
                    count2 += 1
            else:
                missingparameter.append([count,i])
                count2 += 1
    else:
        for i in data:
            count += 1
            if i[0] != "-" and i[1] != "-":
                if [i[0],i[1],i[2]] not in list1:
                    list1.append([i[0],i[1]])
                elif [i[0],i[1]] in list1:
                    duplicate.append([count,i])
                    count2 += 1
            else:
                missingparameter.append([count,i])
                count2 += 1

    total = [duplicate,missingparameter,count2]
    return total

def in_xlsx_duplicate():
    ex_name_sheet = ['Project','Contract','Site','Equipment','Circuit','Interface']
    msg_list = []
    count = 0
    for i in ex_name_sheet:
        filename = 'data_up_load.xlsx'
        data = pd.read_excel(os.path.join("noc_project/upload/", filename),sheet_name=i)
        data = data.replace(np.nan, '-', regex=True)
        data = data.replace('', '-', regex=True)
        data = data.replace('NaT', '-', regex=True)
        data = data.replace('None', '-', regex=True)
        if i == "Project":
            msg = duplicateparameter(0,data)
            msg_list.append(msg[:2])
            count+= msg[2]
        elif i == "Contract":
            msg = duplicateparameter2(i,data)
            msg_list.append(msg[:2])
            count+= msg[2]
        elif i == "Site":
            msg = duplicateparameter2(i,data)
            msg_list.append(msg[:2])
            count+= msg[2]
        elif i == "Equipment":
            msg = duplicateparameter(1,data)
            msg_list.append(msg[:2])
            count+= msg[2]
        elif i == "Circuit":
            msg = duplicateparameter(1,data)
            msg_list.append(msg[:2])
            count+= msg[2]
        elif i == "Interface":
            msg = duplicateparameter2(i,data)
            msg_list.append(msg[:2])
            count+= msg[2]
    return msg_list,count


@app.route('/download')
def download():
    connection = connect()
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

    Project_Name = []
    S_O = []
    Customer_Start_of_contract = []
    Customer_End_of_contract = []
    Disty_Start_of_contract = []
    Disty_End_of_contract = []
    Vpn_Detail = []
    Important_Detail = []
    Addition_Detail = []
    Remark = []
    for i in project:
        Project_Name.append(i[0])
        S_O.append(i[1])
        Customer_Start_of_contract.append(i[2].strftime("%d/%m/%Y"))
        Customer_End_of_contract.append(i[3].strftime("%d/%m/%Y"))
        Disty_Start_of_contract.append(i[4].strftime("%d/%m/%Y"))
        Disty_End_of_contract.append(i[5].strftime("%d/%m/%Y"))
        Vpn_Detail.append(i[6])
        Important_Detail.append(i[7])
        Addition_Detail.append(i[8])
        Remark.append(i[9])

    p_data = [Project_Name, S_O,Customer_Start_of_contract,Customer_End_of_contract,
    Disty_Start_of_contract,Disty_End_of_contract,Vpn_Detail,Important_Detail,
    Addition_Detail,Remark]
    columns =["Project Name", "S/O","Customer_Start_of_contract","Customer_End_of_contract",
    "Disty_Start_of_contract","Disty_End_of_contract","Vpn Detail",
    "Important_Detail","Addition_Detail","Remark"]
    df1 = pd.DataFrame(dict(zip(columns, p_data)))

    Project_Name_contract = []
    role = []
    name = []
    Tel = []
    Addition_Detail_contract = []

    for i in contract:
        #print(i)
        Project_Name_contract.append(i[1])
        role.append(i[2])
        name.append(i[3])
        Tel.append(i[4])
        Addition_Detail_contract.append(i[5])

    con_data = [Project_Name_contract,role,name,Tel,Addition_Detail_contract]
    columns = ["Project Name","Role","Name","Tel.","Additional Detail"]
    df2 = pd.DataFrame(dict(zip(columns, con_data)))

    Project_Name_site = []
    site_name = []
    location = []
    site_short_name = []
    contract_owner_site = []
    contact = []
    type = []

    for i in site:
        Project_Name_site.append(i[1])
        site_name.append(i[2])
        location.append(i[3])
        site_short_name.append(i[4])
        contract_owner_site.append(i[5])
        contact.append(i[6])
        type.append(i[7])
    site_data = [Project_Name_site,site_name,location,site_short_name,contract_owner_site,contact,type]
    columns = ["Project_Ref","Site_name","location","site_short_name.","contact_owner_site","contact_owner_Tel","type"]
    df3 = pd.DataFrame(dict(zip(columns, site_data)))

    serial_number = []
    project_name = []
    site_name_e = []
    brand = []
    model = []
    disty_name = []
    disty_contact = []
    open_case_contact = []
    stract_of_warranty = []
    end_of_warranty = []
    ha_status = []
    ha = []

    for i in equipment:
        serial_number.append(i[0])
        project_name.append(i[1])
        site_name_e.append(i[2])
        brand.append(i[3])
        model.append(i[4])
        disty_name.append(i[5])
        disty_contact.append(i[6])
        open_case_contact.append(i[7])
        stract_of_warranty.append(i[8].strftime("%d/%m/%Y"))
        end_of_warranty.append(i[9].strftime("%d/%m/%Y"))
        ha_status.append(i[10])
        ha.append(i[11])

    equipment_data = [site_name_e,serial_number,brand,model,
                    disty_name,disty_contact,open_case_contact,stract_of_warranty,
                    end_of_warranty,ha,ha_status,project_name]
    columns = ["Site_Ref","Serial_number","Equipment Brand","Equipment Model"
            ,"Disty_name","Disty_contact","Open_case_contact","Start of warranty"
            ,"End of warranty","HA","HA Status","Project_Ref"]
    df4 = pd.DataFrame(dict(zip(columns, equipment_data)))

    circuit_id = []
    equipment_ref = []
    ip_address_pe = []
    ip_address_ce = []
    subnet = []
    loopback = []
    circuit_type = []
    link_number = []
    original_isp = []
    owner_isp = []
    isp_contact_tel = []

    for i in circuit:
        circuit_id.append(i[0])
        equipment_ref.append(i[1])
        ip_address_pe.append(i[2])
        ip_address_ce.append(i[3])
        subnet.append(i[4])
        loopback.append(i[5])
        circuit_type.append(i[6])
        link_number.append(i[7])
        original_isp.append(i[8])
        owner_isp.append(i[9])
        isp_contact_tel.append(i[10])
    circuit_data = [equipment_ref,circuit_id,ip_address_pe,ip_address_ce,
                    subnet,loopback,circuit_type,link_number,original_isp,
                    owner_isp,isp_contact_tel]
    columns = ["Equipment_Ref","Circuit_ID","IP_address_PE","IP_address_CE",
            "Subnet mask","Equipment_Loopback","Circuit_type","Link_number","Original_ISP","Owner ISP","ISP_contact_Tel"]
    df5 = pd.DataFrame(dict(zip(columns, circuit_data)))

    circuit_id = []
    equipment_serial = []
    equipment_brand= []
    equipment_model= []
    physical_interface= []
    vlan_id= []
    tunnel_interface_name = []
    for i in interface:
        circuit_id.append(i[1])
        equipment_serial.append(i[2])
        equipment_brand.append(i[3])
        equipment_model.append(i[4])
        physical_interface.append(i[5])
        vlan_id.append(i[6])
        tunnel_interface_name.append(i[7])
    interface_data = [circuit_id,equipment_serial,equipment_brand,equipment_model,physical_interface,vlan_id,tunnel_interface_name]
    columns = ["Circuit_ID","Equipment Serial","Equipment Brand","Equipment Model","Physical Interface","VLAN_ID","Tunnel Interface Name"]
    df6 = pd.DataFrame(dict(zip(columns, interface_data)))


    with pd.ExcelWriter('noc_project/test/output.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Project', index=False)
        df2.to_excel(writer, sheet_name='Contract', index=False)
        df3.to_excel(writer, sheet_name='Site', index=False)
        df4.to_excel(writer, sheet_name='Equipment', index=False)
        df5.to_excel(writer, sheet_name='Circuit', index=False)
        df6.to_excel(writer, sheet_name='Interface', index=False)
    return send_from_directory("../noc_project/test",
                                "output.xlsx", as_attachment=True)
    # return send_from_directory("C:/Users/nat03/Documents/noc_noc_project/noc_project/test/",
    #                            "output.xlsx", as_attachment=True)

def check_data():
    connection = connect()
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
    try:
        ex_name_sheet = ['Project','Contract','Site','Equipment','Circuit','Interface']
        #ex_name_sheet = ['Project']
        for i in ex_name_sheet:
            filename = 'data_up_load.xlsx'
            data = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename),sheet_name=i)
            #data = pd.read_excel("noc_project/upload/data_up_load.xlsx",sheet_name=i)
            data = data.replace(np.nan, '-', regex=True)
            data = data.replace('', '-', regex=True)
            data = data.replace('NaT', '-', regex=True)
            data = data.replace('None', '-', regex=True)
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
        try:
            msg_new = ["","","","","",""]
            msg_old = ["","","","","",""]
            msg_project_old = ''
            msg_project_update = ''
            global project_new,project_update
            project_update = []
            project_new = []
            # project table check
            for i in project_data:
                #print(i)
                #print(i[4])
                p_new = i[0]
                count = 0
                if i[0] != "-":
                    try:
                        if type(i[2]) == str:
                            i[2] = datetime.datetime.strptime(i[2], '%d/%m/%Y')
                    except (Exception) as error:
                            #print("project",i[2],error)
                            pass
                    try:
                        if type(i[3]) == str:
                            i[3] = datetime.datetime.strptime(i[3], '%d/%m/%Y')
                    except (Exception) as error:
                        #print("project",i[3],error)
                        pass
                    try:
                        if type(i[4]) == str:
                            i[4] = datetime.datetime.strptime(i[4], '%d/%m/%Y')
                    except (Exception) as error:
                        #print("project",i[4],error)
                        pass
                    try:
                        if type(i[5]) == str:
                            i[5] = datetime.datetime.strptime(i[5], '%d/%m/%Y')
                    except (Exception) as error:
                        #print("project",i[5],error)
                        pass

                    # print(i[2],type(i[2])) 
                    # print(i[3],type(i[3])) 
                    # print(i[4],type(i[4]))
                    # print(i[5],type(i[5]))
                    for x in project:
                        p_old = x[0]
                        if p_new == p_old:
                            count += 1
                            if i[0] == x[0] and i[1] == x[1] and i[2] == x[2] and i[3] == x[3] and i[4] == x[4] and i[5] == x[5] and i[6] == x[6] and i[7] == x[7] and i[8] == x[8] and i[9] == x[9]:
                                msg_project_old += p_new+' already in database\n'
                                
                            else:
                                msg_project_update += p_new+' will update\n'
                                
                                project_update.append(i)
                            break
                    if count == 0:
                        project_new.append(i)
                        #print(i)
                        msg_project_update += p_new+' new data\n'

            if len(msg_project_update) != 0:
                msg_project_update = msg_project_update[:-1]

            if len(project_update) != 0:
                #session['project_update'] = project_update
                pass
            if len(project_new) != 0:
                #session['project_new'] = project_new
                pass
            if len(msg_project_old) != 0:
                msg_project_old = msg_project_old[:-1]
            msg_project_old = str(msg_project_old).replace("\n"," <br/> ")
            msg_project_update = str(msg_project_update).replace("\n"," <br/> ")
            msg_project_old = Markup(msg_project_old)
            msg_project_update = Markup(msg_project_update)
            msg_new[0] = msg_project_update
            msg_old[0] = msg_project_old
        except (Exception) as error:
            print(error)
        try:
            global contract_new,contract_update
            msg_contract_old = ''
            msg_contract_update = ''
            contract_update = []
            contract_new = []
            # project table check
            for i in contract_data:
                #print(i)
                if i[0] != "-" and i[1] != "-" and i[2] != "-":
                    con_new = ['','','']
                    con_new[0] = i[0]
                    con_new[1] = i[1]
                    con_new[2] = i[2]
                    count = 0
                    for x in contract:
                        con_old = ['','','']
                        con_old[0] = x[1]
                        con_old[1] = x[2]
                        con_old[2] = x[3]
                        if con_new[0] == con_old[0] and con_new[1] == con_old[1] and con_new[2] == con_old[2]:
                            count += 1
                            if i[0] == x[1] and i[1] == x[2] and i[2] == x[3] and i[3] == x[4] and i[4] == x[5]:
                                msg_contract_old += con_new[0]+","+con_new[1]+' already in database\n'
                            else:
                                msg_contract_update += con_new[0]+","+con_new[1]+' will update\n'
                                i.append(x[0])
                                contract_update.append(i)
                            break
                    if count == 0:
                        msg_contract_update += con_new[0]+","+con_new[1]+' new data\n'
                        contract_new.append(i)

            if len(msg_contract_update) != 0:
                msg_contract_update = msg_contract_update[:-1]

            if len(contract_update) != 0:
                # session['contract_update'] = contract_update
                pass
            if len(contract_new) != 0:
                # session['contract_new'] = contract_new
                pass
            if len(msg_contract_old) != 0:
                msg_contract_old = msg_contract_old[:-1]

            msg_contract_old = str(msg_contract_old).replace("\n"," <br/> ")
            msg_contract_update = str(msg_contract_update).replace("\n"," <br/> ")
            msg_contract_old = Markup(msg_contract_old)
            msg_contract_update = Markup(msg_contract_update)
            msg_new[1] = msg_contract_update
            msg_old[1] = msg_contract_old
        except (Exception) as error:
            print(error)

        try:
            global site_update,site_new
            msg_site_old = ''
            msg_site_update = ''
            site_update = []
            site_new = []
            # project table check
            for i in site_data:
                if i[0] != "-" and i[1] != "-" and i[2] != "-":
                    s_new = ['','','']
                    s_new[0] = i[0]
                    s_new[1] = i[1]
                    s_new[2] = i[2]
                    count = 0
                    for x in site:
                        s_old = ['','','']
                        s_old[0] = x[1]
                        s_old[1] = x[2]
                        s_old[2] = x[3]
                        if s_new[0] == s_old[0] and s_new[1] == s_old[1] and s_new[2] == s_old[2]:
                            count += 1
                            if i[0] == x[1] and i[1] == x[2] and i[2] == x[3] and i[3] == x[4] and i[4] == x[5] and i[5] == x[6] and i[6] == x[7]:
                                msg_site_old += s_new[0]+","+s_new[1]+' already in database\n'
                            else:
                                msg_site_update += s_new[0]+","+s_new[1]+' will update\n'
                                i.append(x[0])
                                site_update.append(i)
                            break
                    if count == 0:
                        msg_site_update += s_new[0]+","+s_new[1]+' new data\n'
                        site_new.append(i)

            if len(msg_site_update) != 0:
                msg_site_update = msg_site_update[:-1]

            if len(msg_site_old) != 0:
                msg_site_old = msg_site_old[:-1]

            if len(site_update) != 0:
                #session['site_update'] = site_update
                pass

            if len(site_new) != 0:
                #session['site_new'] = site_new
                pass
            msg_site_old = str(msg_site_old).replace("\n"," <br/> ")
            msg_site_update = str(msg_site_update).replace("\n"," <br/> ")
            msg_site_old = Markup(msg_site_old)
            msg_site_update = Markup(msg_site_update)
            msg_new[2] = msg_site_update
            msg_old[2] = msg_site_old
        except (Exception) as error:
            print(error)
        try:
            global equipment_update,equipment_new
            msg_equipment_old = ''
            msg_equipment_update = ''
            equipment_update = []
            equipment_new = []
            # equipment table check
            for i in equipment_data:
                if i[1] != "-":
                    e_new = i[1]
                    #print(e_new)
                    count = 0
                    try:
                        if type(i[7]) == str:
                            i[7] = datetime.datetime.strptime(i[7], '%d/%m/%Y')
                        if type(i[8]) == str:
                            i[8] = datetime.datetime.strptime(i[8], '%d/%m/%Y')
                    except (Exception) as error:
                        #print("project",error)
                        pass
                    for x in equipment:
                        e_old = x[0]
                        if e_old == e_new:
                            count += 1
                            # if i[0] != x[2]:
                            #     print(i[0],x[2])
                            # if i[1] != x[0]:
                            #     print(i[1],x[0])
                            # if i[2] != x[3]:
                            #     print(i[2],x[3])
                            # if i[3] != x[4]:
                            #     print(i[3],x[4])
                            # if i[4] != x[5]:
                            #     print(i[4],x[5])
                            # if i[5] != x[6]:
                            #     print(i[5],x[6])
                            # if i[6] != x[7]:
                            #     print(i[6],x[7])
                            # if i[7] != x[8]:
                            #     print(i[7],x[8])
                            # if i[8] != x[9]:
                            #     print(i[8],x[9])
                            # if i[9] != x[11]:
                            #     print(i[9],x[11])
                            # if i[10] != x[-2]:
                            #     print(i[10],x[-2])
                            # if i[11] != x[1]:
                            #     print(i[11],x[1])
                            # print("***")
                            if i[0] == x[2] and i[1] == x[0] and i[2] == x[3] and i[3] == x[4] and i[4] == x[5] and i[5] == x[6] and i[6] == x[7] and i[7] == x[8] and i[8] == x[9] and i[9] == x[11] and i[10] == x[-2] and i[11] == x[1]:
                                msg_equipment_old += e_new+' already in database\n'
                            else:
                                msg_equipment_update += e_new+' will update\n'
                                equipment_update.append(i)
                            break
                    if count == 0:
                        msg_equipment_update += e_new+' new data\n'
                        equipment_new.append(i)
            if len(msg_equipment_update) != 0:
                msg_equipment_update = msg_equipment_update[:-1]

            if len(msg_equipment_old) != 0:
                msg_equipment_old = msg_equipment_old[:-1]
            
            if len(equipment_update) != 0:
                #session['equipment_update'] = equipment_update
                pass
            if len(equipment_new) != 0:
                #session['equipment_new'] = equipment_new
                pass
            msg_equipment_old = str(msg_equipment_old).replace("\n"," <br/> ")
            msg_equipment_update = str(msg_equipment_update).replace("\n"," <br/> ")
            msg_equipment_old = Markup(msg_equipment_old)
            msg_equipment_update = Markup(msg_equipment_update)
            msg_new[3] = msg_equipment_update
            msg_old[3] = msg_equipment_old
        except (Exception) as error:
            print(error)

        try:
            # อาจมีอัปเดจ
            global circuit_new,circuit_update
            msg_circuit_old = ''
            msg_circuit_update = ''
            circuit_update = []
            circuit_new = []
            # equipment table check
            for i in circuit_data:
                if i[1] != "-":
                    cir_new = str(i[1])
                    count = 0
                    #print(i)
                    for x in circuit:
                        cir_old = x[0]
                        if cir_new == cir_old:
                            count += 1
                            i[7] = str(i[7])
                            i[8] = (str(i[8])).upper()
                            i[9] = (str(i[9])).upper()
                            # print(i[9])
                            # if str(i[9]) == "True":
                            #     i[9] = 'TRUE'
                            #     #print(i[9])
                            # if str(i[8]) == "True":
                            #     i[8] = 'TRUE'
                            # if i[0] != x[1]:
                            #     print(i[0],x[1])
                            # if i[1] != x[0]:
                            #     print(i[1],x[0])
                            # if i[2] != x[2]:
                            #     print(i[2],x[2])
                            # if i[3] != x[3]:
                            #     print(i[3],x[3])
                            # if i[4] != x[4]:
                            #     print(i[4],x[4])
                            # if i[5] != x[5]:
                            #     print(i[5],x[5])
                            # if i[6] != x[6]:
                            #     print(i[6],x[6])
                            # if i[7] != x[7]:
                            #     print(i[7],x[7])
                            #     print(type(i[7]),type(x[7]))
                            # if i[8] != x[8]:
                            #     print(i[8],x[8])
                            # if i[9] != x[9]:
                            #     print(i[9],x[9])
                            # if i[10] != x[10]:
                            #     print(i[10],x[10])
                            if str(i[0]) == x[1] and str(i[1]) == x[0] and str(i[2]) == x[2] and str(i[3]) == x[3] and str(i[4]) == x[4] and str(i[5]) == x[5] and str(i[6]) == x[6] and str(i[7]) == x[7] and str(i[8]) == x[8] and str(i[9]) == x[9] and str(i[10]) == x[10]: 
                                msg_circuit_old += cir_new+' already in database\n'
                            else:
                                msg_circuit_update += cir_new+' will update\n'
                                #print(i)
                                circuit_update.append(i)
                            break
                    if count == 0:
                        msg_circuit_update += cir_new+' new data\n'
                        circuit_new.append(i)
            if len(msg_circuit_update) != 0:
                msg_circuit_update = msg_circuit_update[:-1]
            if len(msg_circuit_old) != 0:
                msg_circuit_old = msg_circuit_old[:-1]

            if len(circuit_update) != 0:
                #session['circuit_update'] = circuit_update
                pass
            if len(circuit_new) != 0:
                #session['circuit_new'] = circuit_new
                pass
            msg_circuit_old = str(msg_circuit_old).replace("\n"," <br/> ")
            msg_circuit_update = str(msg_circuit_update).replace("\n"," <br/> ")
            msg_circuit_old = Markup(msg_circuit_old)
            msg_circuit_update = Markup(msg_circuit_update)
            msg_new[4] = msg_circuit_update
            msg_old[4] = msg_circuit_old
        except (Exception) as error:
            print(error,"111")

        try:
            global interface_update,interface_new
            msg_interface_old = ''
            msg_interface_update = ''
            # project table check
            interface_update = []
            interface_new = []
            for i in interface_data:
                if i[0] != '-' and i[1] != '-':
                    inter_new = ['','']
                    inter_new[0] = str(i[0])
                    inter_new[1] = str(i[1])
                    count = 0
                    for x in interface:
                        inter_old = ['','']
                        inter_old[0] = x[1]
                        inter_old[1] = x[2]
                        if str(inter_new[0]) == inter_old[0] and str(inter_new[1]) == inter_old[1]:
                            count += 1
                            if str(i[0]) == x[1] and str(i[1]) == x[2] and str(i[2]) == x[3] and str(i[3]) == x[4] and str(i[4]) == x[5] and str(i[5]) == x[6] and str(i[6]) == x[7]:
                                msg_interface_old += inter_new[0]+","+inter_new[1]+' already in database\n'
                            else:
                                msg_interface_update += inter_new[0]+","+inter_new[1]+' will update\n'
                                i.append(x[0])
                                interface_update.append(i)
                            break
                    if count == 0:
                        msg_interface_update += inter_new[0]+","+inter_new[1]+' new data\n'
                        interface_new.append(i)
            if len(msg_interface_update) != 0:
                msg_interface_update = msg_interface_update[:-1]
            if len(msg_interface_old) != 0:
                msg_interface_old = msg_interface_old[:-1]

            if len(interface_update) != 0:
                #session['interface_update'] = interface_update
                pass
            if len(interface_new) != 0:
                #session['interface_new'] = interface_new
                pass
            msg_interface_old = str(msg_interface_old).replace("\n"," <br/> ")
            msg_interface_update = str(msg_interface_update).replace("\n"," <br/> ")
            msg_interface_old = Markup(msg_interface_old)
            msg_interface_update = Markup(msg_interface_update)
            msg_new[5] = msg_interface_update
            msg_old[5] = msg_interface_old
        except (Exception) as error:
            print(error,'222')
        msg_list = [msg_new,msg_old]
        return msg_list
    except (Exception) as error:
        print(error,'333')

@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        #global equipment,site,circuit,interface,project,contrat
        global_data()
        #circuit_data = request.get_json()
        circuit_data = request.form['circuit_data']
        #print(circuit_data)
        # circuit = session['circuit']
        # equipment = session['equipment']
        # interface = session['interface']
        # site = session['site']
        # project = session['project']
        # contrat = session['contrat']
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
            return jsonify({'htmlcircuit_detial': render_template('circuit_detail.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5,zone5_num = zone5_num,username=session['username'])})
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
                return jsonify({'htmlcircuit_detial': render_template('circuit_detail.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5,zone5_num = zone5_num,username=session['username'])})
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
                        
                    return jsonify({'htmlproject_detial': render_template('project_detail.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,username=session['username'])})
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
                    return jsonify({'htmlsite_detial': render_template('site_detial.html',zone1 = zone1,zone2 = zone2,username=session['username'])})
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
                    return jsonify({'htmlserial_number_detial': render_template('serial_number_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone4_num=zone4_num,username=session['username'])})


@app.route('/noc_project/logout')
def logout():
    event = 'Logout'
    save_log(event)
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


def search(inputdata):
    global circuit,equipment
    # circuit = session['circuit']
    # equipment = session['equipment']
    data = []
    data_len = len(data)
    while data_len == 0:
        #search by circuit_id
        for i in circuit:
            data_in_process = ["","","","","",""]
            if str(i[0]).upper() == str(inputdata).upper():
                data_in_process[0] = i[0]
                for a in equipment:
                    if i[1] == a[0]:
                        data_in_process[1] = a[1]
                        data_in_process[2] = a[2]
                        data_in_process[3] = a[0]
                        break
                data_in_process[4] = i[5]
                data_in_process[5] = i[3]
                data.append(data_in_process)
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
    global circuit,equipment
    # circuit = session['circuit']
    # equipment = session['equipment']
    data = []
    for i in circuit:
        data_in_process = ["","","","","",""]
        data_in_process[0] = i[0]
        for a in equipment:
            if i[1] == a[0]:
                data_in_process[1] = a[1]
                data_in_process[2] = a[2]
                data_in_process[3] = a[0]
                break
        data_in_process[4] = i[5]
        data_in_process[5] = i[3]
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
        global_data()
        data = []
        if request.method == "POST" and 'data_search' in request.form:
            search_data = request.form['data_search']
            data = search(search_data)
            if len(data) == 0:
                msg = "Not Found"
            else:
                msg = "Search Found "
                event = 'normal search '+search_data
                save_log(event)
            return render_template('home.html', text=msg ,data = data ,username=session['username'])
        return render_template('home.html', text='Hello '+str(session['role']) +" "+ str(session['username']),data = data, username=session['username'])
    return redirect(url_for('login'))

@app.route('/noc_project/advance_search', methods=['GET', 'POST'])
def advanced_search():
    global_data()
    main_table = []
    # project = session['project']
    # equipment = session['equipment']
    # site = session['site']
    site2 = [[],[]]
    # circuit = session['circuit']
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
        delete_empty = [ele for ele in inputdata if ele.strip()]
        event = 'advance search'+ str(delete_empty)
        save_log(event)
        #log
        table_data = adv_search(inputdata)
        main_table = table_data[0]
        circuit_table = table_data[1]
        equipment_table = table_data[2]
        project_table = table_data[3]
        site_table = table_data[4]

    return render_template('advanced_search.html', text='Hello '+str(session['role']),main_table = main_table,project=project,
    equipment = equipment,equipment2=equipment2,circuit=circuit,circuit2=circuit2,site2 = site2 ,project_table = project_table,
    site_table = site_table,equipment_table = equipment_table,circuit_table= circuit_table,username=session['username'])

@app.route('/noc_project/serial_number_detial', methods=['GET', 'POST'])
def serial_number_detial():
    if request.method == "POST" and 'data' in request.form:
        connection = connect()
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
        return render_template('circuit_detial.html',zone1 = zone1,zone2 = zone2,zone3 = zone3,zone4 = zone4,zone5 = zone5,username=session['username'])
@app.route('/noc_project/register_user', methods=['GET', 'POST'])
def register_user():
    if 'admin' in session['role'] or 'super_user' in session['role']:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
            A_username = request.form['username']
            A_password = request.form['password']
            A_role = request.form['role']
            #print(A_role)
            connection = connect()
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
                event = 'register ' + A_username
                save_log(event)
                return render_template('home.html',text='Register Successfully')
        return render_template('register_user.html')
    return render_template('home.html',text='role != admin')

@app.route('/noc_project/user_table', methods=['GET', 'POST'])
def user_table():
    if 'admin' in session['role'] or 'super_user' in session['role']:
        # columns = ['Username', 'password', 'Role']
        # session['columns'] = columns
        # return render_template('user_table.html', columns=columns)
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts')
        account = cursor.fetchall()
        columns = ['Username', 'password', 'Role']
        return render_template('user_table.html', columns=columns,data=account,username=session['username'])
    return render_template('home.html',text='role != admin')


@app.route('/noc_project/page_upload', methods = ['GET', 'POST'])
def page_upload():
    error = None
    return render_template('upload.html',error = error,username=session['username']) 

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
                event = 'uploaded '+str(file.filename)
                save_log(event)            
            else:
                errors[file.filename] = 'File type is not allowed'
                event = 'error uploaded '+str(file.filename)
                save_log(event)  
        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 206
            return resp
        if success:
            resp = jsonify({'message' : 'Files successfully uploaded'})
            resp.status_code = 201
            #log_event
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp
    
@app.route("/ajaxfile_delete",methods=["POST","GET"])
def ajaxfile_delete():
    if request.method == 'POST':
        msg = request.form['msg']
        res = ast.literal_eval(msg)
     
        session['delete_pk'] = res[0]
        
        return jsonify({'htmldelete_pop': render_template('delete_pop.html',msg=res,tablename = session['delete_table_name'])})

@app.route("/ajaxfile_delete_user",methods=["POST","GET"])
def ajaxfile_delete_user():
    if request.method == 'POST':
        msg = request.form['msg']
        res = ast.literal_eval(msg)
     
        session['delete_pk'] = res[0]
        
        return jsonify({'htmldelete_pop': render_template('delete_pop.html',msg=res,tablename = 'accounts')})

#@app.route('/delete_table')
def delete_table():
    data = session['delete_table_name']
    global equipment,site,circuit,interface,project,contrat
    try:
        if data == 'Project':
            project1 = replace_space(project)
            return project1
        elif data == 'Contract':
            #contrat = session['contrat']
            contrat1 = replace_space(contrat)
            return contrat1
        elif data == 'Site':
            #site = session['site']
            site1 = replace_space(site)
            return site1
        elif data == 'Equipment':
            #site = session['equipment']
            equipment1 = replace_space(equipment)
            return equipment1
        elif data == 'Circuit':
            #site = session['circuit']
            circuit1 = replace_space(circuit)
            return circuit1
        elif data == 'Interface':
            #site = session['interface']
            interface1 = replace_space(interface)
            return interface1
    except:
        data = [["1","2"]]
        return data

def connect():
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    return connection

def delete_search_option(tablename):
    try:
        connection = connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM "+tablename
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        data = replace_space(data)
        data2 = []
        if tablename.lower() == "interface":
            for i in data:
                if i[2] not in data2:
                    data2.append(i[2])
            return data2
        elif tablename.lower() == "site":
            for i in data:
                if i[1] not in data2:
                    data2.append(i[1])
            return data2
        elif tablename.lower() == "contract":
            for i in data:
                if i[1] not in data2:
                    data2.append(i[1])
            return data2
        else:
            for i in data:
                if i[0] not in data2:
                    data2.append(i[0])
            return data2
    except Exception as error:
        print('delete_search_option',error)
        data = []
        return data2

def global_data():
    global equipment,site,circuit,interface,project,contrat
    connection = connect()
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
    contrat = cursor.fetchall()
    cursor.execute('SELECT * FROM site')
    site = cursor.fetchall()
    cursor.close()
    connection.close()

@app.route('/delete_page', methods=['GET', 'POST'])
def delete_page():
    if 'admin' in session['role'] or 'super_user' in session['role']:
        # session['delete_table_name'] = 'Project'
        if request.method == 'POST' and 'table_name' in request.form:
            tablename = request.form['table_name']
            if tablename == 'Project':
                columns = ['project_name','s/o','C_S_C','C_E_C','D_S_C','D_E_C','Vpn_Detail','Important_Detail','Addition_Detail','Remark']
                session['columns_delete'] = columns
                session['delete_table_name'] = 'Project'
                data_display = delete_table()
                data_option = delete_search_option(tablename)
            elif tablename == 'Contract':
                columns = ['contrat_id','project_name','role','name','tel','additional_detail']
                session['columns_delete'] = columns
                session['delete_table_name'] = 'Contract'
                data_display = delete_table()
                data_option = delete_search_option(tablename)
            elif tablename == 'Site':
                columns = ["site_id","project_name","site_name","location","short_name","contact_owner_site","contact","type"]
                session['columns_delete'] = columns
                session['delete_table_name'] = 'Site'
                data_display = delete_table()
                data_option = delete_search_option(tablename)
            elif tablename == 'Equipment':
                columns = ["serial_number","project_name","site_name","brand","model","disty_name","disty_contact",
                "open_case_contact","s_o_w","e_o_w","ha_status","ha"]
                session['columns_delete'] = columns
                session['delete_table_name'] = 'Equipment'
                data_display = delete_table()
                data_option = delete_search_option(tablename)
            elif tablename == 'Circuit':
                columns = ["circuit_id","equipment_ref","ip_address_pe","ip_address_ce","subnet","loopback",
                "circuit_type","link_number","original_isp","owner_isp","isp_contact_tel"]
                session['columns_delete'] = columns
                session['delete_table_name'] = 'Circuit'
                data_display = delete_table()
                data_option = delete_search_option(tablename)
            elif tablename == 'Interface':
                columns = ["interface_id","circuit_id","e_serial","e_brand","e_model","physical_interface","vlan_id","tunnel_interface_name"]
                session['columns_delete'] = columns
                session['delete_table_name'] = 'Interface'
                data_display = delete_table()
                data_option = delete_search_option(tablename)
            
        if request.method == 'POST' and 'PK' in request.form:
            if request.form['PK'] == "/reset_data" and 'admin' in session['role']:
                data = []
                resetdata()
                global_data()
                return render_template('home.html', text="Reset data by admin!" ,data = data ,username=session['username'])
            if request.form['PK'] == "/reset_user" and 'admin' in session['role']:
                data = []
                data=[]
                resetuser()
                return render_template('home.html', text="Reset user by admin!" ,data = data ,username=session['username'])
            if 'delete_table_name' not in session:
                tablename = 'Project'
            else:
                tablename = session['delete_table_name']
            PK_name = request.form['PK']
            # print(PK_name)
            data_display = delete_search(PK_name,session['delete_table_name'],session['columns_delete'][0])
            data_option = delete_search_option(tablename)
            return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])
        if 'delete_table_name' in session:
            tablename = session['delete_table_name']
            data_display = delete_table()
            data_option = delete_search_option(tablename)
        if 'delete_table_name' not in session:
            columns = ['project_name','s/o','C_S_C','C_E_C','D_S_C','D_E_C','Vpn_Detail','Important_Detail','Addition_Detail','Remark']
            session['columns_delete'] = columns
            session['delete_table_name'] = 'Project'
            tablename = 'Project'
            data_display = delete_table()
            data_option = delete_search_option(tablename)
        global_data()
        return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])
    return render_template('home.html',text='role != admin')


@app.route('/delete_pop_get', methods=['GET', 'POST'])
def delete_pop_get():
    try:
        if request.method == 'POST':
            submit_request = request.form['test']
            if submit_request == 'submit_done':
                table_delete(str(session['delete_pk']),session['delete_table_name'],session['columns_delete'][0])
                data_display = delete_table()
                tablename = session['delete_table_name']
                data_option = delete_search_option(tablename)
                return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display ,data_option = data_option,username=session['username'])
    except Exception as error:
        print("delete_pop_get",error)
        data_display = delete_table()
        tablename = session['delete_table_name']
        data_option = delete_search_option(tablename)
        return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display ,data_option = data_option,username=session['username'])

@app.route('/delete_pop_get_user', methods=['GET', 'POST'])
def delete_pop_get_user():
    try:
        if request.method == 'POST':
            submit_request = request.form['test']
            if submit_request == 'submit_done':
                if str(session['delete_pk']) != "1":
                    table = 'accounts'
                    column = 'user_id'
                    table_delete(str(session['delete_pk']),table,column)
                return redirect(url_for('user_table'))
    except Exception as error:
        text = 'delete user Error '+error
        return render_template('home.html',text=text)

def delete_search(PK_name,tablename,columns_delete):
    try:
        connection = connect()
        cursor = connection.cursor()
        tablename = tablename.lower()
        if tablename.lower() == "interface":
            columns_delete = "equipment_serial"
        elif tablename.lower() == "site":
            columns_delete = "project_name"
        elif tablename.lower() == "contract":
            columns_delete = "project_name"
        sql = "SELECT * FROM "+tablename+" WHERE "+columns_delete+" LIKE "+"'{}%'".format(str(PK_name))
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        data = replace_space(data)
        return data
    except (Exception) as error:
        msg = 'search Fail delete page ' + KeyError
        print(msg)
        return msg
def table_delete(PK_name,tablename,columns_delete):
    try:
        connection = connect()
        cursor = connection.cursor()
        tablename = tablename.lower()
        sql = "DELETE FROM " +tablename+" WHERE "+columns_delete+" = "+"'{}'".format(PK_name)
        #cursor.execute("DELETE FROM %s WHERE %s = %s", (tablename,columns_delete,PK_name))
        cursor.execute(sql)
        connection.commit()
        msg = "DELETE "+PK_name+" form "+tablename+' successfully'
        save_log(msg)
        cursor.close()
        connection.close()
        global_data()
        return msg
    except (Exception) as error:
        msg = "Fail to DELETE "+PK_name+" form "+tablename
        save_log(msg)
        return msg +" "+error

def project_table_update_edit(data):
    connection = connect()
    cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_project in data:
        #print(data_update_project)
        try:
            if data_update_project[1] != "-":
                sql_update_query = """Update project set s_o = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[1], data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[1])
        except (Exception) as error:
            error = "s_o",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[2] != "-":
                data_update_project[2] = data_update_project[2].strftime('%Y/%m/%d')
                date_2 = datetime.datetime.strptime(data_update_project[2], '%Y/%m/%d')
                sql_update_query = """Update project set customer_start_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_2, data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[2])
        except (Exception) as error:
            error = "customer_start_of_contract",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[3] != "-":
                data_update_project[3] = data_update_project[3].strftime('%Y/%m/%d')
                date_3 = datetime.datetime.strptime(data_update_project[3], '%Y/%m/%d')
                sql_update_query = """Update project set customer_end_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_3, data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[3])
        except (Exception) as error:
            error = "customer_end_of_contract",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[4] != "-":
                data_update_project[4] = data_update_project[4].strftime('%Y/%m/%d')
                date_4 = datetime.datetime.strptime(data_update_project[4], '%Y/%m/%d')
                #print(date_4)
                sql_update_query = """Update project set disty_start_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_4, data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[4])
        except (Exception) as error:
            error = "disty_start_of_contract",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[5] != "-":
                data_update_project[5] = data_update_project[5].strftime('%Y/%m/%d')
                date_5 = datetime.datetime.strptime(data_update_project[5], '%Y/%m/%d')
                sql_update_query = """Update project set disty_end_of_contract = %s where project_name = %s"""
                cursor.execute(sql_update_query, (date_5, data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[5])
        except (Exception) as error:
            error = "disty_end_of_contract",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[6] != "-":
                sql_update_query = """Update project set vpn_detail = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[6], data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[6])
        except (Exception) as error:
            error = "vpn_detail",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[7] != "-":
                sql_update_query = """Update project set important_detail = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[7], data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[7])
        except (Exception) as error:
            error = "important_detail",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[8] != "-":
                sql_update_query = """Update project set addition_detail = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[8], data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[8])
        except (Exception) as error:
            error = "addition_detail",data_update_project[0],str(error)
            msg_error.append(error)
        try:
            if data_update_project[9] != "-":
                sql_update_query = """Update project set remark = %s where project_name = %s"""
                cursor.execute(sql_update_query, (data_update_project[9], data_update_project[0]))
                connection.commit()
                msg_successful.append(data_update_project[9])
        except (Exception) as error:
            error = "remark",data_update_project[0],str(error)
            msg_error.append(error)
    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)
    cursor.close()
    connection.close()

def contract_table_update_edit(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_contract in data:
        try:
            if data_update_contract[1] != "-":
                sql_update_query = """Update contract set project_name = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[1], data_update_contract[0]))
                connection.commit()
                msg_successful.append(data_update_contract[1])
        except (Exception) as error:
            error = "name",data_update_contract[0],data_update_contract[1],str(error)
            msg_error.append(error)
        try:
            if data_update_contract[2] != "-":
                sql_update_query = """Update contract set role = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[2], data_update_contract[0]))
                connection.commit()
                msg_successful.append(data_update_contract[2])
        except (Exception) as error:
            error = "name",data_update_contract[0],data_update_contract[1],str(error)
            msg_error.append(error)
        try:
            if data_update_contract[3] != "-":
                sql_update_query = """Update contract set name = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[3], data_update_contract[0]))
                connection.commit()
                msg_successful.append(data_update_contract[3])
        except (Exception) as error:
            error = "name",data_update_contract[0],data_update_contract[1],str(error)
            msg_error.append(error)
        try:
            if data_update_contract[4] != "-":
                sql_update_query = """Update contract set tel = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[4], data_update_contract[0]))
                connection.commit()
                msg_successful.append(data_update_contract[4])
        except (Exception) as error:
            error = "tel",data_update_contract[0],data_update_contract[1],str(error)
            msg_error.append(error)
        try:
            if data_update_contract[5] != "-":
                sql_update_query = """Update contract set additional_detail = %s where contrat_id = %s"""
                cursor.execute(sql_update_query, (data_update_contract[5], data_update_contract[0]))
                connection.commit()
                msg_successful.append(data_update_contract[5])
        except (Exception) as error:
            error = "additional_detail",data_update_contract[0],data_update_contract[1],str(error)
            msg_error.append(error)
    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)
    cursor.close()
    connection.close()

def site_table_update_edit(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_site in data:
        try:
            if data_update_site[1] != "-":
                sql_update_query = """Update site set project_name = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[1], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[1])
        except (Exception) as error:
            error = "location",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)
        try:
            if data_update_site[2] != "-":
                sql_update_query = """Update site set site_name = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[2], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[2])
        except (Exception) as error:
            error = "location",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)
        try:
            if data_update_site[3] != "-":
                sql_update_query = """Update site set location = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[3], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[3])
        except (Exception) as error:
            error = "location",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)
        try:
            if data_update_site[4] != "-":
                sql_update_query = """Update site set site_short_name = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[4], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[4])
        except (Exception) as error:
            error = "site_short_name ",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)
        try:
            if data_update_site[5] != "-":
                sql_update_query = """Update site set contact_owner_site = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[5], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[5])
        except (Exception) as error:
            error = "contact_owner_site",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)
        try:
            if data_update_site[6] != "-":
                sql_update_query = """Update site set contact = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[6], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[6])
        except (Exception) as error:
            error = "contact",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)
        try:
            if data_update_site[7] != "-":
                sql_update_query = """Update site set type = %s where site_id = %s"""
                cursor.execute(sql_update_query, (data_update_site[7], data_update_site[0]))
                connection.commit()
                msg_successful.append(data_update_site[7])
        except (Exception) as error:
            error = "type",data_update_site[1],data_update_site[2],str(error)
            msg_error.append(error)

    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)
    cursor.close()
    connection.close()  

def equipment_table_update_edit(data):
    connection = connect()
    #cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_equipment in data:
        cursor = connection.cursor()
        try:
            if data_update_equipment[1] != "-":
                sql_update_query = """Update equipment set project_name = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[1], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[1])
        except (Exception) as error:
            error = "project_name",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[2] != "-":
                sql_update_query = """Update equipment set site_name = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[2], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[2])
        except (Exception) as error:
            error = "site_name",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[3] != "-":
                sql_update_query = """Update equipment set brand = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[3], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[3])
        except (Exception) as error:
            error = "brand",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[4] != "-":
                sql_update_query = """Update equipment set model = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[4], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[4])
        except (Exception) as error:
            error = "model",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[5] != "-":
                sql_update_query = """Update equipment set disty_name = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[5], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[5])
        except (Exception) as error:
            error = "disty_name",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[6] != "-":
                sql_update_query = """Update equipment set disty_contact = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[6], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[6])
        except (Exception) as error:
            error = "disty_contact",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[7] != "-":
                sql_update_query = """Update equipment set open_case_contact = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[7], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[7])
        except (Exception) as error:
            error = "open_case_contact",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[8] != "-":
                data_update_equipment[8] = data_update_equipment[8].strftime('%Y/%m/%d')
                data_update_equipment[8] = datetime.datetime.strptime(data_update_equipment[8], '%Y/%m/%d')
                sql_update_query = """Update equipment set start_of_warranty = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[8], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[8])
        except (Exception) as error:
            error = "start_of_warranty",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[9] != "-":
                data_update_equipment[9] = data_update_equipment[9].strftime('%Y/%m/%d')
                date_8 = datetime.datetime.strptime(data_update_equipment[9], '%Y/%m/%d')
                sql_update_query = """Update equipment set end_of_warranty = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (date_8, data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[9])
        except (Exception) as error:
            error = "end_of_warranty",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[11] != "-":
                #print(data_update_equipment[9],print(type(data_update_equipment[9])))
                sql_update_query = """Update equipment set ha = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[11], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[11])
        except (Exception) as error:
            error = "ha",data_update_equipment[0],str(error)
            msg_error.append(error)
        try:
            if data_update_equipment[10] != "-":
                #print(data_update_equipment[10])
                sql_update_query = """Update equipment set ha_status = %s where serial_number = %s"""
                cursor.execute(sql_update_query, (data_update_equipment[10], data_update_equipment[0]))
                connection.commit()
                msg_successful.append(data_update_equipment[10])
        except (Exception) as error:
            error = "ha_status",data_update_equipment[0],str(error)
            msg_error.append(error)

    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)
    
    cursor.close()
    connection.close()

def circuit_table_update_edit(data):
    connection = connect()
    cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_circuit in data:
        try:
            if data_update_circuit[1] != "-":
                sql_update_query = """Update circuit set equipment_ref = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[1]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[1])
        except (Exception) as error:
            error = "equipment_ref",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[2] != "-":
                sql_update_query = """Update circuit set ip_address_pe = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[2]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[2])
        except (Exception) as error:
            error = "ip_address_pe",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[3] != "-":
                sql_update_query = """Update circuit set ip_address_ce = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[3]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[3])
        except (Exception) as error:
            error = "ip_address_ce",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[4] != "-":
                sql_update_query = """Update circuit set subnet = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[4]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[4])
        except (Exception) as error:
            error = "subnet",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[5] != "-":
                sql_update_query = """Update circuit set loopback = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[5]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[5])
        except (Exception) as error:
            error = "loopback",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[6] != "-":
                sql_update_query = """Update circuit set circuit_type = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[6]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[6])
        except (Exception) as error:
            error = "circuit_type",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[7] != "-":
                sql_update_query = """Update circuit set link_number = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[7]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[7])
        except (Exception) as error:
            error = "link_number",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[8] != "-":
                sql_update_query = """Update circuit set original_isp = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[8]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[8])
        except (Exception) as error:
            error = "original_isp",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[9] != "-":
                sql_update_query = """Update circuit set owner_isp = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[9]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[9])
        except (Exception) as error:
            error = "owner_isp",data_update_circuit[0],str(error)
            msg_error.append(error)
        try:
            if data_update_circuit[10] != "-":
                sql_update_query = """Update circuit set isp_contact_tel = %s where circuit_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_circuit[10]), str(data_update_circuit[0])))
                connection.commit()
                msg_successful.append(data_update_circuit[10])
        except (Exception) as error:
            error = "isp_contact_tel",data_update_circuit[0],str(error)
            msg_error.append(error)

    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)
    
    cursor.close()
    connection.close()


def interface_table_update_edit(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_interface in data:
        try:
            if data_update_interface[1] != "-":
                sql_update_query = """Update interface set circuit_id = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[1]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[1])
        except (Exception) as error:
            error = "circuit_id",data_update_interface[0],str(error)
            msg_error.append(error)
        try:
            if data_update_interface[2] != "-":
                sql_update_query = """Update interface set equipment_serial = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[2]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[2])
        except (Exception) as error:
            error = "equipment_serial",data_update_interface[0],str(error)
            msg_error.append(error)
        try:
            if data_update_interface[3] != "-":
                sql_update_query = """Update interface set equipment_brand = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[3]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[3])
        except (Exception) as error:
            error = "equipment_brand",data_update_interface[0],str(error)
            msg_error.append(error)
        try:
            if data_update_interface[4] != "-":
                sql_update_query = """Update interface set equipment_model = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[4]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[4])
        except (Exception) as error:
            error = "equipment_model",data_update_interface[0],str(error)
            msg_error.append(error)
        try:
            if data_update_interface[5] != "-":
                sql_update_query = """Update interface set physical_interface = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[5]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[5])
        except (Exception) as error:
            error = "physical_interface",data_update_interface[0],str(error)
            msg_error.append(error)
        try:
            if data_update_interface[6] != "-":
                sql_update_query = """Update interface set vlan_id = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[6]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[6])
        except (Exception) as error:
            error = "vlan_id",data_update_interface[0],str(error)
            msg_error.append(error)
        try:
            if data_update_interface[7] != "-":
                sql_update_query = """Update interface set tunnel_interface_name = %s where interface_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_interface[7]), str(data_update_interface[0])))
                connection.commit()
                msg_successful.append(data_update_interface[7])
        except (Exception) as error:
            error = "tunnel_interface_name",data_update_interface[0],str(error)
            msg_error.append(error)
    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)

    cursor.close()
    connection.close()

def user_table_update_edit(data):
    #recheck
    connection = connect()
    cursor = connection.cursor()
    msg_successful = []
    msg_error = []
    for data_update_user in data:
        try:
            if data_update_user[1] != "-":
                sql_update_query = """Update accounts set username = %s where user_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_user[1]), str(data_update_user[0])))
                connection.commit()
                msg_successful.append(data_update_user[1])
        except (Exception) as error:
            error = "username",data_update_user[0],str(error)
            msg_error.append(error)
        try:
            if data_update_user[2] != "-":
                sql_update_query = """Update accounts set password = %s where user_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_user[2]), str(data_update_user[0])))
                connection.commit()
                msg_successful.append(data_update_user[2])
        except (Exception) as error:
            error = "password",data_update_user[0],str(error)
            msg_error.append(error)
        try:
            if data_update_user[3] != "-":
                sql_update_query = """Update accounts set role = %s where user_id = %s"""
                cursor.execute(sql_update_query, (str(data_update_user[3]), str(data_update_user[0])))
                connection.commit()
                msg_successful.append(data_update_user[3])
        except (Exception) as error:
            error = "role",data_update_user[0],str(error)
            msg_error.append(error)
    if len(msg_successful) != 0:
        msg = "successful update "+data[0][0]+" "+str(msg_successful)
        save_log(msg)
    if len(msg_error) != 0:
        msg = "error update "+data[0][0]+" "+str(msg_error)
        save_log(msg)

    cursor.close()
    connection.close()

@app.route("/ajax_edit",methods=["POST","GET"])
def ajax_edite():
    if request.method == 'POST':
        global equipment,site,circuit,interface,project,contrat
        msg = request.form['msg']
        res = ast.literal_eval(msg)
        if session['delete_table_name'] == 'Project':
            return jsonify({'htmledit_project': render_template('edit_project.html',msg=res,columns = session['columns_delete'])})
        elif session['delete_table_name'] == 'Contract':
            return jsonify({'htmledit_contract': render_template('edit_contract.html',msg=res,columns = session['columns_delete'])})
        elif session['delete_table_name'] == 'Site':
            return jsonify({'htmledit_site': render_template('edit_site.html',msg=res,columns = session['columns_delete'])})
        elif session['delete_table_name'] == 'Equipment':
            return jsonify({'htmledit_equipment': render_template('edit_equipment.html',msg=res,columns = session['columns_delete'])})
        elif session['delete_table_name'] == 'Circuit':
            return jsonify({'htmledit_circuit': render_template('edit_circuit.html',msg=res,columns = session['columns_delete'])})
        elif session['delete_table_name'] == 'Interface':
            return jsonify({'htmledit_interface': render_template('edit_interface.html',msg=res,columns = session['columns_delete'])})

        
@app.route("/ajax_edit_user",methods=["POST","GET"])
def ajax_edite_user():
    if request.method == 'POST':
        global equipment,site,circuit,interface,project,contrat
        msg = request.form['msg']
        res = ast.literal_eval(msg)
        column = ['user_id','username','password','role']
        return jsonify({'htmledit_user': render_template('edit_user.html',msg=res,columns = column)})

@app.route("/edit_project_page",methods=["POST","GET"])
def edit_project_page():
    if request.method == 'POST':
        # x = request.form
        # print(x)
        inputdata = [request.form['pk'],request.form['s_o'],request.form['c_s_c'],request.form['c_e_c'],
        request.form['d_s_c'],request.form['d_e_c'],request.form['vpn'],request.form['important'],
        request.form['addition'],request.form['remark']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        try:
            if inputdata[2] != "-":
                inputdata[2] = datetime.datetime.strptime(inputdata[2], '%d/%m/%Y')
            if inputdata[3] != "-":
                inputdata[3] = datetime.datetime.strptime(inputdata[3], '%d/%m/%Y')
            if inputdata[4] != "-":
                inputdata[4] = datetime.datetime.strptime(inputdata[4], '%d/%m/%Y')
            if inputdata[5] != "-":
                inputdata[5] = datetime.datetime.strptime(inputdata[5], '%d/%m/%Y')
        except:
            print('edit_project date time error')
        data = [inputdata]
        project_table_update_edit(data)
        global_data()
        tablename = session['delete_table_name']
        data_display = delete_table()
        data_option = delete_search_option(tablename)
    return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])

@app.route("/edit_contract_page",methods=["POST","GET"])
def edit_contract_page():
    if request.method == 'POST':
        inputdata = [request.form['pk'],request.form['project_name'],request.form['role'],request.form['name'],
        request.form['tel'],request.form['additional_detail']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        data = [inputdata]
        contract_table_update_edit(data)
        global_data()
        tablename = session['delete_table_name']
        data_display = delete_table()
        data_option = delete_search_option(tablename)
    return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])

@app.route("/edit_site_page",methods=["POST","GET"])
def edit_site_page():
    if request.method == 'POST':
        inputdata = [request.form['pk'],request.form['project_name'],request.form['site_name'],request.form['location'],
        request.form['short_name'],request.form['contact_owner_site'],request.form['contact'],request.form['type']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        # print(inputdata)
        data = [inputdata]
        site_table_update_edit(data)
        global_data()
        tablename = session['delete_table_name']
        data_display = delete_table()
        data_option = delete_search_option(tablename)
    return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])

@app.route("/edit_equipment_page",methods=["POST","GET"])
def edit_equipment_page():
    if request.method == 'POST':
        inputdata = [request.form['pk'],request.form['project_name'],request.form['site_name'],request.form['brand'],
        request.form['model'],request.form['disty_name'],request.form['disty_contact'],request.form['open_case_contact'],
        request.form['s_o_w'],request.form['e_o_w'],request.form['ha_status'],request.form['ha']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        if inputdata[8] != "-":
            inputdata[8] = datetime.datetime.strptime(inputdata[8], '%d/%m/%Y')
        if inputdata[9] != "-":
            inputdata[9] = datetime.datetime.strptime(inputdata[9], '%d/%m/%Y')
        data = [inputdata]
        equipment_table_update_edit(data)
        global_data()
        tablename = session['delete_table_name']
        data_display = delete_table()
        data_option = delete_search_option(tablename)
    return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])

@app.route("/edit_circuit_page",methods=["POST","GET"])
def edit_circuit_page():
    if request.method == 'POST':
        inputdata = [request.form['pk'],request.form['equipment_ref'],request.form['ip_address_pe'],request.form['ip_address_ce'],
        request.form['subnet'],request.form['loopback'],request.form['circuit_type'],request.form['link_number'],
        request.form['original_isp'],request.form['owner_isp'],request.form['isp_contact_tel']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        data = [inputdata]
        #print(data)
        circuit_table_update_edit(data)
        global_data()
        tablename = session['delete_table_name']
        data_display = delete_table()
        data_option = delete_search_option(tablename)
    return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])

@app.route("/edit_interface_page",methods=["POST","GET"])
def edit_interface_page():
    if request.method == 'POST':
        inputdata = [request.form['pk'],request.form['circuit_id'],request.form['e_serial'],request.form['e_brand'],
        request.form['e_model'],request.form['physical_interface'],request.form['vlan_id'],request.form['tunnel_interface_name']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        # print(inputdata)
        data = [inputdata]
        interface_table_update_edit(data)
        global_data()
        tablename = session['delete_table_name']
        data_display = delete_table()
        data_option = delete_search_option(tablename)
    return render_template('delete_form.html', columns=session['columns_delete'] ,tablename = tablename,data_display = data_display,data_option = data_option,username=session['username'])

@app.route("/edit_user_page",methods=["POST","GET"])
def edit_user_page():
    if request.method == 'POST':
        inputdata = [request.form['pk'],request.form['username'],request.form['password'],
        request.form['role']]
        for i in range(len(inputdata)):
            if inputdata[i] == "":
                inputdata[i] = "-"
        # print(inputdata)
        data = [inputdata]
        if data[0][0] != "1":
            user_table_update_edit(data)
    return redirect(url_for('user_table'))

def replace_space(data):
    data2 = []
    for i in data:
        data3 = []
        for x in i:
            if type(x) == str:
                x.replace('\n','<br />')
                data3.append(x)
            elif type(x) == datetime.datetime:
                x = x.strftime("%d/%m/%Y")
                data3.append(x)
            else:
                data3.append(x)
        data2.append(data3)
    return data2
        
@app.route('/noc_project/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', account=session,username=session['username'])
    return redirect(url_for('login'))

def save_log(event):
    connection = connect()
    cursor = connection.cursor()
    time = datetime.datetime.now()
    try:
        postgres_insert_query = """ INSERT INTO event_logs (username,time,event) VALUES (%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(session['username'],time,event))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print("Log: error",error)

def W_chack(sql):
    sql_str = sql
    sql_list = sql.split(' ')
    if "Where" not in sql_list:
        sql_str = sql_str+" Where"
        return(sql_str)
    else:
        sql_str = sql_str+" and"
        return(sql_str)

def resetuser():
    username = "admin"
    password = "pplus@123"
    role = "admin" 
    try:
        connection = connect()
        table = ['accounts']
        cursor = connection.cursor()
        for i in table:
            cursor = connection.cursor()
            sql = 'DROP TABLE '+i
            cursor.execute(sql)
            connection.commit()
    except (Exception, psycopg2.DatabaseError) as error: 
            print(error) 
    try:
        connection = connect()
        cursor = connection.cursor()
        try:
            # TABLE accounts
            create_table_guery = '''CREATE TABLE accounts 
                (user_id SERIAL PRIMARY KEY,
                username      VARCHAR(50) NOT NULL,
                password      VARCHAR(5000) NOT NULL,
                role      VARCHAR(50) NOT NULL); '''
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error while creating PostgreSQL table", error) 
    try:
        connection = connection = connect()
        
        cursor = connection.cursor()
        try:
            postgres_insert_query = """ INSERT INTO accounts (username, password, role) VALUES (%s,%s,%s)"""
            cursor.execute(postgres_insert_query,(username,password,role))
            connection.commit()
        except Exception as error:
            print(error,"user")
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error while inserting PostgreSQL table", error) 
    
    
def resetdata():
    try:
        connection = connect()
        #table = ['accounts','circuit','contract','equipment','event_logs','interface','project','site']
        table = ['circuit','contract','equipment','event_logs','interface','project','site']
        cursor = connection.cursor()
        for i in table:
            cursor = connection.cursor()
            sql = 'DROP TABLE '+i
            cursor.execute(sql)
            connection.commit()
    except (Exception, psycopg2.DatabaseError) as error: 
            print(error) 



    try:
        connection = connect()
        cursor = connection.cursor()
        try:
            #TABLE circuit
            create_table_guery = '''CREATE TABLE circuit
                (circuit_id  VARCHAR(50) PRIMARY KEY,
                equipment_ref     VARCHAR(50) ,
                ip_address_pe     VARCHAR(50) ,
                ip_address_ce      VARCHAR(50) ,
                subnet      VARCHAR(50) ,
                loopback      VARCHAR(50) ,
                circuit_type      VARCHAR(50) ,
                link_number      VARCHAR(50) ,
                original_isp      VARCHAR(255) ,
                owner_isp      VARCHAR(255) ,
                isp_contact_tel      VARCHAR(255)); ''' 
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 
        try:    
            create_table_guery = '''CREATE TABLE event_logs
                (id SERIAL PRIMARY KEY,
                username     VARCHAR(50) ,
                time     timestamp ,
                event      VARCHAR(500)); ''' 
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 
        try:    
            #TABLE interface
            create_table_guery = '''CREATE TABLE interface
                (interface_id SERIAL PRIMARY KEY,
                circuit_id VARCHAR(50),
                equipment_serial VARCHAR(50),
                equipment_brand VARCHAR(50),
                equipment_model VARCHAR(50),
                physical_interface VARCHAR(50),
                vlan_id VARCHAR(50),
                tunnel_interface_name VARCHAR(255)); '''
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 

        try:
            #TABLE equipment
            create_table_guery = '''CREATE TABLE equipment 
                (serial_number VARCHAR(50) PRIMARY KEY,
                project_name VARCHAR(50) ,
                site_name      VARCHAR(5000) ,
                brand      VARCHAR(50) ,
                model      VARCHAR(50) ,
                disty_name      VARCHAR(500) ,
                disty_contact      VARCHAR(500) ,
                open_case_contact VARCHAR(50) ,
                start_of_warranty timestamp ,
                end_of_warranty timestamp ,
                ha_status VARCHAR(50) ,
                ha      VARCHAR(50)); '''  
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 
        try:
            #TABLE project
            create_table_guery = '''CREATE TABLE project 
                (project_name VARCHAR(50) PRIMARY KEY,
                s_o      VARCHAR(50) ,
                customer_start_of_contract      timestamp ,
                customer_end_of_contract timestamp ,
                disty_start_of_contract timestamp ,
                disty_end_of_contract timestamp ,
                vpn_detail VARCHAR(5000) ,
                Important_Detail VARCHAR(5000) ,
                Addition_Detail VARCHAR(5000) ,
                Remark      VARCHAR(5000)); '''  
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error)    
        try:  
        #TABLE contract
            create_table_guery = '''CREATE TABLE contract 
                (contrat_id SERIAL PRIMARY KEY,
            project_name VARCHAR(50) ,
            role VARCHAR(50) ,
            name VARCHAR(50) ,
            tel VARCHAR(50) ,
            additional_detail VARCHAR(5000)); '''
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 
        try:   
            #TABLE site
            create_table_guery = '''CREATE TABLE site 
                (site_id SERIAL PRIMARY KEY,
                project_name VARCHAR(50) ,
                site_name      VARCHAR(50),
                location      VARCHAR(5000),
                site_short_name VARCHAR(50),
                contact_owner_site VARCHAR(5000),
                contact VARCHAR(50),
                type VARCHAR(50));''' 
            cursor.execute(create_table_guery)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error while creating PostgreSQL table", error) 
        print("Table created successfully in PostgreSOL ")

    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error while creating PostgreSQL table", error) 

    try:
        connection = connection = connect()
        
        cursor = connection.cursor()
        try:
            data = [["Demo_data","FG200FT922929184_Demo","Fortinet","FG-600E","SiS Distribution (Thailand) PCL.","074-559082-4","support_pack@sisthai.com",
                "16/02/2001","16/02/2002","Yes","MAIN","Demo_project"]]
            for i in data:
                    cursor = connection.cursor()
                    cursor.execute('SELECT * FROM equipment')
                    equipment_for_count = cursor.fetchall()
                    if i[1] == "-":
                        i[1] = str(len(equipment_for_count))
                    if i[7] != "-":
                        i[7] = datetime.datetime.strptime(i[7], '%d/%m/%Y')
                    if i[8] != "-":
                        i[8] = datetime.datetime.strptime(i[8], '%d/%m/%Y')

                    if i[7] == "-":
                        d = "2001/2/16"
                        i[7] = d
                        i[7] = datetime.datetime.strptime(i[7], '%Y/%m/%d')
                    if i[8] == "-":
                        d = "2002/2/16"
                        i[8] = d
                        i[8] = datetime.datetime.strptime(i[8], '%Y/%m/%d')
                    cursor.execute('SELECT * FROM equipment WHERE serial_number = %s AND site_name = %s AND project_name = %s',(i[1],i[0],i[-1],))
                    data_in_base = cursor.fetchall()
                    if data_in_base:
                        print("ERROR_equipment")
                    else:
                        postgres_insert_query = """ INSERT INTO equipment (serial_number, project_name,site_name, brand,model,disty_name,disty_contact,
                        open_case_contact,start_of_warranty,end_of_warranty,ha_status,ha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        cursor.execute(postgres_insert_query,(i[1],i[-1],i[0],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                        connection.commit()
        except Exception as error:
            print(error,"equipment")

        try:
            data = [["Demo_project","SO200162_Demo","01/10/2022","01/10/2023","01/10/2022","01/10/2023","IP : 58.97.106.134\nPort : 10443\nUsername : pplus\nPassword : pplus@123",
            "Fortimanager IP : 10.x.x.x","ผู้ติดต่อหลัก : XXXXXXXXXX","Suradech _Test"]]
            for i in data:
                    if i[2] != "-":
                        i[2] = datetime.datetime.strptime(i[2], '%d/%m/%Y')
                    if i[3] != "-":
                        i[3] = datetime.datetime.strptime(i[3], '%d/%m/%Y')
                    if i[4] != "-":
                        i[4] = datetime.datetime.strptime(i[4], '%d/%m/%Y')
                    if i[5] != "-":
                        i[5] = datetime.datetime.strptime(i[5], '%d/%m/%Y')

                    if i[2] == "-":
                        d = "2001/2/16"
                        i[2] = d
                        i[2] = datetime.datetime.strptime(i[2], '%Y/%m/%d')
                    if i[3] == "-":
                        d = "2002/2/16"
                        i[3] = d
                        i[3] = datetime.datetime.strptime(i[3], '%Y/%m/%d')
                    if i[4] == "-":
                        d = "2001/2/16"
                        i[4] = d
                        i[4] = datetime.datetime.strptime(i[4], '%Y/%m/%d')
                    if i[5] == "-":
                        d = "2002/2/16"
                        i[5] = d
                        i[5] = datetime.datetime.strptime(i[5], '%Y/%m/%d')
                    #print(data , 'new data')
                    #print(i[0])
                    cursor.execute('SELECT * FROM project WHERE project_name = %s ',(i[0],))
                    data_in_base = cursor.fetchall()
                    if data_in_base:
                        print("ERROR_project")
                    else:
                        postgres_insert_query = """ INSERT INTO project (project_name,s_o,customer_start_of_contract,customer_end_of_contract,
                        disty_start_of_contract,disty_end_of_contract,vpn_detail,Important_Detail,
                        Addition_Detail,Remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]))
                        connection.commit()
        except Exception as error:
            print(error,"project")

        try:
            data = [["Demo_data","Sale PPLUS","Suchat Onjai","088-8888888","เก็บข้อมูล detail ขนาดใหญ่ เว้นบรรทัดได้ "]]
            for i in data:
                    cursor.execute('SELECT * FROM contract WHERE project_name = %s AND role = %s AND name = %s',(i[0],i[1],i[2],))
                    data_in_base = cursor.fetchall()
                    if data_in_base:
                        print("ERROR_contract")
                    else:
                        postgres_insert_query = """ INSERT INTO contract (project_name,role,name,tel,
                        additional_detail) VALUES (%s,%s,%s,%s,%s)"""
                        cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4]))
                        connection.commit()
        except Exception as error:
            print(error,"contract")
        try:
            data = [["Demo_project","Demo_data","394 ชั้น4 ตึกธนาคารกรุงเทพ , ตรงข้ามสยามพารากอน, ปทุมวัน, เขตปทุมวัน กรุงเทพมหานคร 10330","088-8888888","เก็บข้อมูล detail ขนาดใหญ่ เว้นบรรทัดได้ ",
            "SPTR","-","-","HQ"]]
            for i in data:
                cursor.execute('SELECT * FROM site WHERE project_name = %s AND site_name = %s AND location = %s',(i[0],i[1],i[2],))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_site")
                else:
                    postgres_insert_query = """ INSERT INTO site (project_name,site_name,location,site_short_name,
                    contact_owner_site,contact,type) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                    connection.commit()
        except Exception as error:
            print(error,"site")

        try:
            data = [["9610663051_Demo","FG200FT922929184_Demo","Fortinet","FG-200F","Wan3","-","-"]]
            for i in data:
                cursor.execute('SELECT * FROM interface WHERE circuit_id = %s AND equipment_serial = %s AND equipment_brand = %s',(str(i[0]),str(i[1]),str(i[2]),))
                data_in_base = cursor.fetchall()
                if data_in_base:
                    print("ERROR_interface")
                else:
                    postgres_insert_query = """ INSERT INTO interface (circuit_id,equipment_serial,equipment_brand,
                    equipment_model,physical_interface,vlan_id,tunnel_interface_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(postgres_insert_query,(str(i[0]),str(i[1]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6])))
            connection.commit()
        except Exception as error:
            print(error,'interface')

        try:
            data = [["FG200FT922929184_Demo","9610663051_Demo","171.103.24.161","171.103.24.162","255.255.255.252","10.11.220.166","Internet","3","CAT","TRUE","1239*6"]]
            for i in data:
                    cursor = connection.cursor()
                    cursor.execute('SELECT * FROM circuit')
                    circuit_for_count = cursor.fetchall()
                    if i[1] == "-":
                        i[1] = str(len(circuit_for_count))
                    i[-3] = str(i[-3]).upper()
                    i[-4] = str(i[-4]).upper()
                    #print(i)
                    cursor = connection.cursor()
                    #cursor.execute('SELECT * FROM circuit WHERE equipment_ref = %s AND owner_isp = %s', (a, b,))
                    cursor.execute('SELECT * FROM circuit WHERE circuit_id = %s AND equipment_ref = %s AND ip_address_pe = %s',(str(i[1]),str(i[0]),str(i[2]),))
                    data_in_base = cursor.fetchall()
                    if data_in_base:
                        print("ERROR_circuit")
                    else:
                        postgres_insert_query = """ INSERT INTO circuit (circuit_id, equipment_ref, ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
                        link_number,original_isp,owner_isp,isp_contact_tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        cursor.execute(postgres_insert_query,(str(i[1]),str(i[0]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6]),
                        str(i[7]),str(i[8]),str(i[9]),str(i[10])))
            connection.commit()
        except Exception as error:
            print(error,'circuit')


    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error while creating PostgreSQL table", error) 
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSOL connection is closed")

            
def adv_search(inputdata):
    connection = connect()
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
            data_in_process = ["","","","","",""]
            if str(i[0]).upper() == str(n[0]).upper():
                #data_in_process.append(i[0]) #circuit_id  added
                data_in_process[0] = i[0] #circuit_id  added
                for a in equipment_all:
                    if i[1] == a[0]:
                        # data_in_process.append(a[1]) #project_name added
                        # data_in_process.append(a[2]) #site_name added
                        # data_in_process.append(a[0]) #serial_number added
                        data_in_process[3] = a[0] #serial_number added
                        data_in_process[2] = a[2] #site_name added
                        data_in_process[1] = a[1] #project_name added
                        break
                # data_in_process.append(i[5])     #Equipment_Loopback  added
                # data_in_process.append(i[3])   #IP_address_CE  added
                data_in_process[-2] = i[5]  #Equipment_Loopback  added
                data_in_process[-1] = i[3]  #IP_address_CE added
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
            data_in_process = ["","","","","",""]
            data_in_process[0] = i[0] #circuit_id  added
            for a in equipment_all:
                if i[1] == a[0]:
                    data_in_process[3] = a[0] #serial_number added
                    data_in_process[2] = a[2] #site_name added
                    data_in_process[1] = a[1] #project_name added
                    break
            data_in_process[-2] = i[5]  #Equipment_Loopback  added
            data_in_process[-1] = i[3]  #IP_address_CE added
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
    app.run(debug=True,host="0.0.0.0")

