# -*- coding utf-8 -*-
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../Create_Community_VK/Bot/db'))

from database import DataBase

list_data = (["начало диалога", 1], ["потоки младших классов", 2], ["выбор ссылки на чат класса", 3],
             ["получение расписания", 4], ["потоки старших классов", 21])


def load_data():
    db = DataBase()
    db.load_data(list_data)
    print('Загрузка завершена')


def test():
    for item in list_data:
        print(f'data1= {item[0]}, data2= {item[1]}')


if __name__ == '__main__':
    load_data()
