import glob
import os
import time
import datetime
import pathlib
import pandas as pd

from dotenv import load_dotenv


if __name__ == "__main__":


    def is_target_name(file_name: str)-> str :
        name_split = file_name.split(" ")
        for name in name_split:
            if len(name[:6]) == 6 and name[:3].isalpha() and name[3:6].isdigit():
                return name[:6]
            else:
                return 'error'
    def time_normal(time):
        return datetime.datetime.strptime(time, "%c")



    while True:





        print('Data manager')
        load_dotenv()
        print(str(os.environ.get('GLOB_FILE_PATH')) + r'\**\*.xl*')
        len_dir = len(str(os.environ.get('GLOB_FILE_PATH'))) + 1

        file_list = glob.glob(str(os.environ.get('GLOB_FILE_PATH')) + r'\**\*.xl*', recursive=True)

        df_new = pd.DataFrame()

        for file in file_list:
            # making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y")
            making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%c")
            modify_time = time.ctime(os.path.getmtime(file))
            file_name = pathlib.Path(file).stem
            df_new = df_new.append(pd.DataFrame([[file_name,making_time, modify_time,  file, is_target_name(file_name)]], columns=[ 'file_name', 'making_time','modify_time', 'file_path', 'target']))


        df_old = pd.read_excel('./DB.xlsx')


        # analysis
        exp_new_list = df_new['file_path'].values
        exp_new_list = list(set(list(map(lambda x: x[len_dir:].split("\\")[0], exp_new_list))))
        # print(exp_new_list)
        df_analy = pd.DataFrame({'name': exp_new_list, 'days':[0]*len(exp_new_list), 'count':[0]*len(exp_new_list)})


        # print(df_old)
        print()
        path_list_new = df_new['file_path'].to_list()
        for i, path in enumerate(path_list_new):
            if len(df_old.query(f'file_path == @path')) == 0:
                print('new data: ', path[len_dir:].split("\\")[0], path[len_dir:].split("\\")[-1], ' ,Date: ' ,df_new['making_time'].to_list()[i])

            elif len(df_old.query(f'file_path == @path')) > 0:
                if df_old.query(f'file_path == @path')['modify_time'].values[0] != df_new.query(f'file_path == @path')['modify_time'].values[0]:
                    print( 'modifided: ',path[len_dir:].split("\\")[0], path[len_dir:].split("\\")[-1], 'Date: ', time_normal(df_old.query(f'file_path == @path')['modify_time'].values[0]), '-->' ,time_normal(df_new.query(f'file_path == @path')['modify_time'].values[0]))

            
            if path[len_dir:].split("\\")[0] in exp_new_list:
                exp_name = path[len_dir:].split("\\")[0]

                aa = df_analy.query('name == @exp_name')
                # print(aa)
                df_analy.at[aa.index.to_list()[0], 'count'] = aa.at[aa.index.to_list()[0], 'count'] +1
                # print(df_analy.query('name == @exp_name'))
        
        

        
        print(df_analy)

        df_analy.to_excel('./Analysis DB.xlsx')

        # print(df_new)
        process_do = input('Continue(any)? or Save(save): ')
        
        if process_do == "save":
            df_new.to_excel('DB.xlsx', index=False)
            print('saved new data')
            break
        elif process_do == 'q':
            break
        else:
            pass