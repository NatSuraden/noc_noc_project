import psycopg2
connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
cursor = connection.cursor()
display_list = []
cursor.execute('SELECT * FROM circuit')
circuit = cursor.fetchall()
cursor.execute('SELECT * FROM equipment')
equipment = cursor.fetchall()
cursor.execute('SELECT * FROM site')
site = cursor.fetchall()
cursor.execute('SELECT * FROM project')
project = cursor.fetchall()
cursor.execute('SELECT * FROM interface')
interface = cursor.fetchall()
cursor.execute('SELECT * FROM contract')
contract = cursor.fetchall()

# ต้องการ circuit_id , project_name , site_name , serial_number ,  Equipment_Loopback , IP_address_CE 
## basic data stage 0
# data = []
# for i in circuit:
#     data_in_process = []
#     data_in_process.append(i[0])     #circuit_id  added
#     for a in equipment:
#         if i[1] == a[0]:
#             data_in_process.append(a[1]) #project_name added
#             data_in_process.append(a[2]) #site_name added
#             data_in_process.append(a[0]) #serial_number added
#             break
#     data_in_process.append(i[5])     #Equipment_Loopback  added
#     data_in_process.append(i[3])   #IP_address_CE  added
#     data.append(data_in_process)
# print('basic data stage 0')
# for i in data:
#     print(i)
# print("********************")



# search by circuit_id
# circuit_id = "U15480"
# data = []
# for i in circuit:
#         data_in_process = [circuit_id] #circuit_id  added
#         if i[0] == data_in_process[0]:
#             for a in equipment:
#                 if i[1] == a[0]:
#                     data_in_process.append(a[1]) #project_name added
#                     data_in_process.append(a[2]) #site_name added
#                     data_in_process.append(a[0]) #serial_number added
#                     break
#             data_in_process.append(i[5])     #Equipment_Loopback  added
#             data_in_process.append(i[3])   #IP_address_CE  added
#             data.append(data_in_process)
#             break
# print("search by circuit_id")
# for i in data:
#     print(i)
# print("********************")



# # search by project_name
data = []
project_name = "Makro"
for i in equipment:
    data_in_process = ["",project_name,"","","",""] #project_name added
    if i[1] == project_name:
        data_in_process[2] = i[2] #site_name added
        data_in_process[3] = i[0] #serial_number added 
        for a in circuit:
            if a[1] == i[0]:
                data_in_process[0] = a[0] #circuit_id  added
                data_in_process[-2] = a[5] #Equipment_Loopback  added
                data_in_process[-1] = a[3] #IP_address_CE added
                break
        data.append(data_in_process)
print("search by project_name")
for i in data:
     print(i)
# print("********************")



# # search by site_name
# site_name = "ลาดกระบัง"
# data = []
# for a in equipment:
#     data_in_process = ["","",site_name,"","",""] #site_name added
#     if a[2] == data_in_process[2]:
#         data_in_process[3] = a[0] #serial_number added 
#         data_in_process[1] = a[1] #project_name added
#         for x in circuit:
#             if x[1] == data_in_process[3]:
#                 data_in_process[0] = x[0]   #circuit_id  added
#                 data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                 data_in_process[-1] = x[3]  #IP_address_CE added
#                 break
#         data.append(data_in_process)
# print("search by site_name")
# for i in data:
#      print(i)           
# print("********************")

# # search by serial_number
# serial_number = "S108EN5920004706"
# data = []
# for i in equipment:
#     data_in_process = ["","","",serial_number,"",""] #serial_number added
#     if i[0] == data_in_process[3]:
#         data_in_process[2] = i[2] #site_name added
#         data_in_process[1] = i[1] #project_name added
#         for x in circuit:
#             if x[1] == data_in_process[3]:
#                 data_in_process[0] = x[0]   #circuit_id  added
#                 data_in_process[-2] = x[5]  #Equipment_Loopback  added
#                 data_in_process[-1] = x[3]  #IP_address_CE added
#                 break
#         data.append(data_in_process)
# print("search by serial_number")
# for i in data:
#      print(i)           
# print("********************")

# search by IP
# ip_address = '171.103.210.226'
# data = []
# for i in circuit:
#     data_in_process = ["","","","",ip_address,""] #Equipment_Loopback  added
#     if i[5] == data_in_process[4]:
#         data_in_process[0] = i[0]   #circuit_id  added
#         data_in_process[-1] = i[3]  #IP_address_CE added
#         data_in_process[3] = i[1]   #serial_number added
#         for x in equipment:
#             if x[0] == data_in_process[3]:
#                 data_in_process[1] = x[1] #project_name added
#                 data_in_process[2] = x[2] #site_name added
#                 break
#         data.append(data_in_process)
# if len(data) > 0:
#     print("search by IP")
#     for i in data:
#         print(i)           
#     print("********************")
# else:
#     for i in circuit:
#         data_in_process = ["","","","","",ip_address] # IP_address_CE added
#         if i[3] == data_in_process[-1]:
#             data_in_process[0] = i[0]   #circuit_id  added
#             data_in_process[-2] = i[5]  #IP_address_CE added
#             data_in_process[3] = i[1]   #serial_number added
#             for x in equipment:
#                 if x[0] == data_in_process[3]:
#                     data_in_process[1] = x[1] #project_name added
#                     data_in_process[2] = x[2] #site_name added
#                     break
#             data.append(data_in_process)
#     if len(data) == 0:
#         print("NOT FOUND")
#     else:
#         print("search by IP")
#         for i in data:
#             print(i)           
#         print("********************")     

