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

    def select_timetable_class(self, week_day=[], class_letter=[]):
        # формируем условия запроса по дню недели
        sql_week = ''
        sql_week += " OR ".join([f"day_of_week ='{item}'" for item in week_day])

        # формируем условия запроса по классу
        sql_class_letter = ''
        sql_class_letter += " OR ".join([f"class ='{item}'" for item in class_letter])

        sql = "SELECT id, class, lesson_number, academic_discipline, day_of_week, editor, time_update " \
              f"FROM timetable WHERE ({sql_class_letter}) AND ({sql_week});"
        print('sql= ', sql)
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result
