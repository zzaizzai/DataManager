import glob
import os
import time
import datetime
import pathlib
import pandas as pd
import workdays
from dotenv import load_dotenv


def count_workdays(start_date: datetime, end_date: datetime) -> int:
    return workdays.networkdays(start_date, end_date)

if __name__ == "__main__":

    print(os.getcwd())

    def is_target_name(file_name: str) -> str:
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

        print('reading files.....')
        file_list = glob.glob(
            str(os.environ.get('GLOB_FILE_PATH')) + r'\**\*.xl*', recursive=True)

        df_new = pd.DataFrame()

        for file in file_list:
            # making_time = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y")
            making_time = time_normal(time.ctime(os.path.getctime(file)))
            modify_time = time_normal(time.ctime(os.path.getmtime(file)))
            file_name = pathlib.Path(file).stem
            df_new = df_new.append(pd.DataFrame([[file_name, making_time, modify_time, file[len_dir:].split("\\")[0],  is_target_name(
                file_name),  -1,file]], columns=['file_name', 'create_time', 'modify_time',  'exp_name', 'target', 'days','file_path']))

        print('new df')
        print(df_new)
        if os.path.isfile('./DB.xlsx'):
            df_old = pd.read_excel('./DB.xlsx')
        else:
            print('none old df')
            df_old = df_new

        # analysis
        exp_new_list = df_new['file_path'].values
        exp_new_list = list(
            set(list(map(lambda x: x[len_dir:].split("\\")[0], exp_new_list))))
        # print(exp_new_list)
        df_analy = pd.DataFrame(
            {'days_mean': [0]*len(exp_new_list), 'count': [0]*len(exp_new_list), 'name': exp_new_list})

        # print(df_old)
        print()
        #  counts
        path_list_new = df_new['file_path'].to_list()
        for i, path in enumerate(path_list_new):
            if len(df_old.query(f'file_path == @path')) == 0:
                print('New data: ', path[len_dir:].split("\\")[0], path[len_dir:].split(
                    "\\")[-1], ' ,Date: ', df_new['create_time'].to_list()[i],
                    count_workdays(df_new['create_time'].to_list()[i], datetime.datetime.today()), 'days ago')

            elif len(df_old.query(f'file_path == @path')) > 0:
                if df_old.query(f'file_path == @path')['modify_time'].values[0] != df_new.query(f'file_path == @path')['modify_time'].values[0]:
                    print('Modifided: ', path[len_dir:].split("\\")[0],
                          path[len_dir:].split("\\")[-1], 'Date: ',
                          str(pd.to_datetime(df_old.query(
                              f'file_path == @path')['modify_time'].values[0])),
                          '-->',
                          pd.to_datetime(df_new.query(f'file_path == @path')['modify_time'].values[0]), 
                          count_workdays(pd.to_datetime(df_new.query(f'file_path == @path')['modify_time'].values[0]), datetime.datetime.today()) , 'days ago')

            if path[len_dir:].split("\\")[0] in exp_new_list:
                exp_name = path[len_dir:].split("\\")[0]

                aa = df_analy.query('name == @exp_name')
                # print(aa)
                df_analy.at[aa.index.to_list()[0], 'count'] = aa.at[aa.index.to_list()[
                    0], 'count'] + 1
                # print(df_analy.query('name == @exp_name'))

        for _, value in enumerate(exp_new_list):
            print(value)
            print(df_new.query('exp_name == @value'))


        # add days data
        target_list = df_new['target'].to_list()
        target_list = list(set(target_list))
        print(target_list)
        df_new = df_new.reset_index(drop=True)

        df_days_all = pd.DataFrame()
        for a_target in target_list:
            df_days_part_by_modi = df_new.query('target == @a_target').sort_values('modify_time')
            print(df_days_part_by_modi)
            date_min = pd.to_datetime(df_days_part_by_modi['modify_time'].min())
            print(df_days_part_by_modi['modify_time'].iat[1])
            print(count_workdays(date_min, df_days_part_by_modi['modify_time'].iat[1]))
            for _, value in enumerate(df_days_part_by_modi['modify_time'].index):
                print(value, df_days_part_by_modi['modify_time'][value])
                # print(count_workdays(date_min, df_days['modify_time'][value]))
                df_days_part_by_modi.loc[value, 'days'] = count_workdays(date_min, df_days_part_by_modi.loc[value, 'modify_time'])
            df_days_all = pd.concat([df_days_all, df_days_part_by_modi])
            
            
        

        #  calculate mean day
        # for _, value in enumerate(exp_new_list):
        #     print(value)
        #     print(df_analy.query('name == @value'))
        #     print(df_days_all.query('exp_name == @value')['days'].mean())
        #     # df_analy.query('name == @value')['days'][0] = df_days_all.query('exp_name == @value')['days'].mean()
        #     # df_analy.query('name == @value')['days'].iat[0] = df_days_all.query('exp_name == @value')['days'].mean()
        #     print(df_analy.query('name == @value')['days'].values[0])
        #     df_analy.query('name == @value')['days'].values[0] = 2
        df_analy = df_analy.reset_index(drop=True)
        for _, value in enumerate(df_analy['name'].index):
            ex_name = df_analy['name'][value]
            df_analy.loc[value,'days_mean'] = df_days_all.query('exp_name == @ex_name')['days'].mean()

        print(df_days_all)

        print()
        df_analy = df_analy.sort_values('count', ascending=False)
        print(df_analy)

        
        df_analy = df_analy.reset_index(drop=True)
        df_analy.to_excel('./Analysis DB.xlsx', index=False)

        # print(df_new)
        process_do = input('Continue(any)? or Save(save): ')
        df_save = df_days_all
        if process_do == "save":
            # df_save = df_save.sort_values(by=['target', 'modify_time'])
            df_save = df_save.reset_index(drop=True)
            df_save.to_excel('DB.xlsx', index=False)
            print('saved new data')
            break
        elif process_do == 'q':
            break
        else:
            pass
