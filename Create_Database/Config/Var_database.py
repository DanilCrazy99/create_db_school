# -*- coding: utf-8 -*-

main_database = 'postgres'

# для сервера UBUNTU
# user = 'school'
# password = '123qwer'
# schoolName = 'school17'

# для локального сервера
user = 'sergey'
password = '5482173'
schoolName = 'schooltestbd'
schoolPass = '87654321'

host = 'localhost'
port = 5432
class_school = '1A'

path_timetable = r'Config/CopyTimetable.xlsx'

default_data_role = ['user', 'creator', 'editor', 'visitor', 'administrator', 'editor_time_table']
default_data_status = [['начало диалога', 1],
                       ['потоки младших классов', 2],
                       ['выбор ссылки на чат класса', 3],
                       ['получение расписания', 4],
                       ['потоки старших классов', 21],
                       ['InLine клавиатура', 41]
                       ]
