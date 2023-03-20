import os
import pandas as pd
import numpy as np
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

def displaytest(msg):
    for i in msg[0]:
        print("duplicate parameter",i)
    for i in msg[1]:
        print("missingparameter",i)   

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



    
x = in_xlsx_duplicate()
print(len(x[0]))

# for i in x:
#     print(i)