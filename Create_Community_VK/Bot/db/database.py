# -*- coding: utf-8 -*-

# файл для работы с бд Postgresql
import psycopg2

from Create_Database.Config.Var_database import schoolName, user, password, host, port


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

    def select_timetable_class(self, week_day, class_letter):
        sql = "SELECT id, class, lesson_number, academic_discipline, day_of_week, editor, time_update " \
              f"FROM timetable WHERE class='{class_letter}' AND day_of_week = '{week_day}';"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result
