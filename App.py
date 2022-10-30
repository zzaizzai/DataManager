import glob
import os
import time
import datetime
import pathlib
import pandas as pd
import uuid

file_list = glob.glob(r'C:\Users\junsa\Desktop\junsai\**\*.xl*', recursive=True)
# print(file_list)


df_new = pd.DataFrame()
for file in file_list:
    # making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y")
    making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%c")
    modify_time = time.ctime(os.path.getmtime(file))
    file_name = pathlib.Path(file).stem
    # print(file_name, making_time )
    df_new = df_new.append(pd.DataFrame([[uuid.uuid4() ,file_name,making_time, file]], columns=['uuid', 'file_name', 'making_time','file_path']))

print(df_new)

# df_new.to_excel('DB.xlsx', index=False)

df_old = pd.read_excel('./DB.xlsx')
print(df_old)

path_list_new = df_new['file_path'].to_list()
for path in path_list_new:
    if len(df_old.query(f'file_path == @path')) == 0:
        print('new data', path)