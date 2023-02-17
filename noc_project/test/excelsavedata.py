import pandas as pd
import psycopg2
import numpy as np
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
data = pd.read_excel("noc_project/test/output.xlsx",sheet_name='Project')
#data = pd.read_excel("noc_project/upload/data_up_load.xlsx",sheet_name='Project')
print(data)