import psycopg2
from psycopg2 import Error 
from datetime import date
from datetime import datetime
import datetime
username = "admin"
password = "1234"
role = "admin" 
def connect():
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="python2565")
    return connection
try:
    #connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="postgres")
    connection = connect()
    table = ['accounts','circuit','contract','equipment','event_logs','interface','project','site']
    cursor = connection.cursor()
    for i in table:
        cursor = connection.cursor()
        sql = 'DROP TABLE '+i
        cursor.execute(sql)
        connection.commit()
    # sql = '''DROP table IF EXISTS accounts '''
  
    
    # cursor.execute(sql)
    # connection.commit()
except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 
try:
    connection = connect()
    #connection = psycopg2.connect(user="webadmin",password="BFCqhr46914", host="node4943-env-2254395.th.app.ruk-com.cloud", port="11043", database="pythonlogin")

    try:
        cursor = connection.cursor()
        # TABLE accounts
        create_table_guery = '''CREATE TABLE accounts 
            (user_id SERIAL PRIMARY KEY,
            username      VARCHAR(50) NOT NULL,
            password      VARCHAR(50) NOT NULL,
            role      VARCHAR(50)); '''
        cursor.execute(create_table_guery)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error while creating PostgreSQL table", error) 
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
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSOL connection is closed")
try:
    connection = connection = connect()
    #connection = psycopg2.connect(user="webadmin",password="BFCqhr46914", host="node4943-env-2254395.th.app.ruk-com.cloud", port="11043", database="pythonlogin")

    cursor = connection.cursor()
    try:
        postgres_insert_query = """ INSERT INTO accounts (username, password, role) VALUES (%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(username,password,role))
        connection.commit()
    except Exception as error:
        print(error,"user")
    # postgres_insert_query = """ INSERT INTO circuit (equipment_ref, circuit_id, ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
    #     link_number,original_isp,owner_isp,isp_contact_tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    # cursor.execute(postgres_insert_query,(equipment_ref,circuit_id,ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
    # link_number,original_isp,owner_isp,isp_contact_tel))
    try:
        data = [["DC-TIDC-TT","FG6H0ETB20906010","Fortinet","FG-600E","SiS Distribution (Thailand) PCL.","074-559082-4","support_pack@sisthai.com",
            "16/02/2001","16/02/2002","Yes","MAIN","Makro"]]
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
        data = [["Makro","SO200162","01/10/2022","01/10/2023","01/10/2022","01/10/2023","IP : 58.97.106.134\nPort : 10443\nUsername : pplus\nPassword : pplus@123",
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
        data = [["Officemate","Sale PPLUS","Suchat Onjai","088-8888888","เก็บข้อมูล detail ขนาดใหญ่ เว้นบรรทัดได้ "]]
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
        data = [["SuperTrader","SuperTrader","394 ชั้น4 ตึกธนาคารกรุงเทพ , ตรงข้ามสยามพารากอน, ปทุมวัน, เขตปทุมวัน กรุงเทพมหานคร 10330","088-8888888","เก็บข้อมูล detail ขนาดใหญ่ เว้นบรรทัดได้ ",
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
        data = [["9610663051","FG200FT922929184","Fortinet","FG-200F","Wan3","-","-"]]
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
        data = [["FG100FTK20022966","O13944","171.103.24.161","171.103.24.162","255.255.255.252","10.11.220.166","Internet","3","CAT","TRUE","1239*6"]]
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
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSOL connection is closed")