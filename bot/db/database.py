# -*- coding: utf-8 -*-

# файл для работы с бд Postgresql
import psycopg2
import logging
import datetime
import time

from Variables.Var_database import schoolName, user, password, host, port, path_timetable

class DataBase:
    def __init__(self):
        self.__connect = psycopg2.connect(
                        database=schoolName,
                        user=user,
                        password=password,
                        host=host,
                        port=port
        )
        self.__cursor = self.__connect.cursor()

    def select_timetable_class(self):
        sql = 'SELECT id, class, lesson_number, academic_discipline, day_of_week, editor, time_update FROM timetable;'
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result
