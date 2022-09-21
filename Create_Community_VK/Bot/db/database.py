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
              f"FROM timetable WHERE ({sql_class_letter}) AND ({sql_week}) " \
              "ORDER BY class, day_of_week, lesson_number ASC ;"

        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result

    def select_roles_with_vk_id(self, id_user):  # Проверка на наличие специфичной роли в postgres
        with self.__cursor() as cursor:
            cursor.execute(
                "SELECT * FROM role INNER JOIN users ON role.id = users.role_id;"
            )
            a = cursor.fetchall()  # Забираю результат командной строки
            b = []
            d = []
            for c in range(len(a)):
                b.append(a[c][1])  # Получаю роли
                d.append(a[c][4])  # Получаю id
            e = {'role': b}
            f = {'id': d}
            if id_user in f['id']:
                for i in range(len(f['id'])):
                    if f['id'][i] == id_user:
                        return e['role'][i]

