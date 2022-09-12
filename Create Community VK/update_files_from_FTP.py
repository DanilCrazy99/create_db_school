from ftplib import FTP
import os
from Variables.Var_community import main_path, host, user, passwd

ftp = FTP(host=host)  # Авторизация на FTP сервере

def iteration_list_folder(path_folder):
    path_in_def = path_folder
    list_in_folder = []
    ftp.retrlines('NLST', list_in_folder.append)
    for item in list_in_folder:
        if '.' not in item:
            path_creating_folder = os.path.join(path_in_def, item)
            try:
                os.mkdir(path_creating_folder)
            except FileExistsError:
                print(f'Эта папка уже существует: {item}')
            except FileNotFoundError:
                new_folder_path = path_in_def
                os.mkdir(new_folder_path)
                try:
                    os.mkdir(path_creating_folder)
                except FileExistsError:
                    print(f'Эта папка уже существует: {item}')
            ftp.cwd(f'{item}')
            iteration_list_folder(path_creating_folder)
        include_files(item, path_in_def)
    ftp.cwd('..')


def include_files(list_files, path_file):
    if list_files != '.':
        if list_files != '..':
            if '.' in list_files:
                with open(f'{os.path.join(path_file, list_files)}', 'wb') as fp:
                    ftp.retrbinary(f'RETR {list_files}', fp.write)


try:
    ftp.login(user=user, passwd=passwd)
    ftp.cwd('school17')
except Exception:
    pass

iteration_list_folder(main_path)
ftp.quit()
