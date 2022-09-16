# -*- coding: utf-8 -*-
from Create_Community_VK.Bot.db.database import DataBase

if __name__ == '__main__':
    db = DataBase()
    for data_week in db.select_timetable_class(week_day=['Пятница', 'Суббота'], class_letter=['5А', '5Б']):
        print(data_week)
