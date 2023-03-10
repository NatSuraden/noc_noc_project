import psycopg2
from psycopg2 import Error 

try:
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    #connection = psycopg2.connect(user="webadmin",password="BFCqhr46914", host="node4943-env-2254395.th.app.ruk-com.cloud", port="11043", database="pythonlogin")

    try:
        cursor = connection.cursor()
        # TABLE accounts
        """  create_table_guery = '''CREATE TABLE accounts 
            (user_id SERIAL PRIMARY KEY,
            username      VARCHAR(50) NOT NULL,
            password      VARCHAR(50) NOT NULL,
            role      VARCHAR(50)); '''
        """
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
            event      VARCHAR(50)); ''' 
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
    print("Table created successfully in PostgreSOL ")

except (Exception, psycopg2.DatabaseError) as error: 
    print("Error while creating PostgreSQL table", error) 
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSOL connection is closed")