import os
import pandas as pd
import numpy as np
ex_name_sheet = ['Project','Contract','Site','Equipment','Circuit','Interface']
        #ex_name_sheet = ['Project']
for i in ex_name_sheet:
    filename = 'data_up_load.xlsx'
    data = pd.read_excel(os.path.join("noc_project/upload/", filename),sheet_name=i)
    data = data.replace(np.nan, '-', regex=True)
    data = data.replace('', '-', regex=True)
    data = data.replace('NaT', '-', regex=True)
    data = data.replace('None', '-', regex=True)
    if i == "Equipment":
        #print(data.duplicated(subset=['Serial_number']))
        duplicateRows = data[data.duplicated(['Serial_number'])]
        print(duplicateRows)
        #print(len(duplicateRows))
        duplicateRows = duplicateRows.values.tolist()
        for x in duplicateRows:
            print(x[1])
 