import glob
import os
import time
import datetime
import pathlib
import pandas as pd

from dotenv import load_dotenv


if __name__ == "__main__":
    while True:

        def time_normal(time):
            return datetime.datetime.strptime(time, "%c")

        print('Data manager')
        load_dotenv()
        print(str(os.environ.get('GLOB_FILE_PATH')) + r'\**\*.xl*')
        len_dir = len(str(os.environ.get('GLOB_FILE_PATH'))) + 1

        file_list = glob.glob(str(os.environ.get('GLOB_FILE_PATH')) + r'\**\*.xl*', recursive=True)
        # print(file_list)
        df_new = pd.DataFrame()
        for file in file_list:
            # making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y")
            making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%c")
            modify_time = time.ctime(os.path.getmtime(file))
            file_name = pathlib.Path(file).stem
            # print(file_name, making_time )
            df_new = df_new.append(pd.DataFrame([[file_name,making_time, modify_time,  file]], columns=[ 'file_name', 'making_time','modify_time', 'file_path']))

        print(df_new)
        # df_new.to_excel('DB.xlsx', index=False)

        df_old = pd.read_excel('./DB.xlsx')
        print(df_old)

        path_list_new = df_new['file_path'].to_list()
        for i, path in enumerate(path_list_new):
            if len(df_old.query(f'file_path == @path')) == 0:
                print(df_new.query("file_path == @path").loc[:,['making_time']])
                print('new data: ', path[len_dir:], ' ,Date: ' ,df_new['making_time'].to_list()[i])

            elif len(df_old.query(f'file_path == @path')) > 0:
                if df_old.query(f'file_path == @path')['modify_time'].values[0] != df_new.query(f'file_path == @path')['modify_time'].values[0]:
                    print( 'modifided: ',path[len_dir:], 'Date: ', time_normal(df_old.query(f'file_path == @path')['modify_time'].values[0]), '-->' ,time_normal(df_new.query(f'file_path == @path')['modify_time'].values[0]))

        process_do = input('Continue(any)? or Save(save): ')
        if process_do == "save":
            df_new.to_excel('DB.xlsx', index=False)
            print('saved new data')
            break
        elif process_do == 'q':
            break
        else:
            pass