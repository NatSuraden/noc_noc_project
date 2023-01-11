import psycopg2
from psycopg2 import Error 

""" username = "Nat_Test"
password = "1234"
role = "admin" """

# equipment_ref = "FGT60FTK20054815"
# circuit_id = "V53802"
# ip_address_pe = "10.99.178.17"
# ip_address_ce = "10.99.178.18"
# subnet = "255.255.255.252"
# loopback = "10.11.220.8"
# circuit_type = "MPLS"
# link_number = "WAN1"
# original_isp = "TRUE"
# owner_isp = "TRUE"
# isp_contact_tel = "1239*6"

site_name = 'ลาดกระบัง'
serial_number = 'FGT60FTK20036867'
brand = 'Fortinet'
model = 'FG-60F'
disty_name = 'SiS Distribution (Thailand) PCL.'
disty_contact = '074-559082-4'
open_case_contact ='support_pack@sisthai.com'
start_of_warranty = ''
end_of_warranty = ''
ha = ''
ha_status = 'Backup'


try:
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    #connection = psycopg2.connect(user="webadmin",password="BFCqhr46914", host="node4943-env-2254395.th.app.ruk-com.cloud", port="11043", database="pythonlogin")

    cursor = connection.cursor()

    #postgres_insert_query = """ INSERT INTO accounts (username, password, role) VALUES (%s,%s,%s)"""
    #cursor.execute(postgres_insert_query,(username,password,role))
    
    # postgres_insert_query = """ INSERT INTO circuit (equipment_ref, circuit_id, ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
    #     link_number,original_isp,owner_isp,isp_contact_tel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    # cursor.execute(postgres_insert_query,(equipment_ref,circuit_id,ip_address_pe,ip_address_ce,subnet,loopback,circuit_type,
    # link_number,original_isp,owner_isp,isp_contact_tel))

    postgres_insert_query = """ INSERT INTO equipment (serial_number, site_name, brand,model,disty_name,disty_contact,
    open_case_contact,start_of_warranty,end_of_warranty,ha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(postgres_insert_query,(serial_number, site_name, brand,model,disty_name,disty_contact,
    open_case_contact,start_of_warranty,end_of_warranty,ha,ha_status))



    connection.commit()
    print("successfully in PostgreSOL ")

except (Exception, psycopg2.DatabaseError) as error: 
    print("Error while creating PostgreSQL table", error) 
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSOL connection is closed")