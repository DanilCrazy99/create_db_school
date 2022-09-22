# -*- coding: utf-8 -*-

# файл для работы с бд Postgresql
import psycopg2
import logging

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

    @staticmethod
    def format_args(sql, parameters: dict):
        """
        Создание параметра запроса для WHERE с условием AND
        :param sql: начальная часть запроса с WHERE
        :param parameters: именованный словарь с условиями. пример: {"поле_БД": переменная по которой будет выборка}
        :return: строка SQL запроса и кортеж из параметров
        """
        sql += " AND ".join([
            f"{item} = %s" for item in parameters
        ])
        return sql, tuple(parameters.values())

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

    # Проверка на наличие специфичной роли в postgres
    def select_roles_with_vk_id(self, id_user):
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

    # добавление описателя статуса
    def insert_status_name(self, status_name):
        sql = "INSERT INTO status(status) VALUES (%s);"
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        logging.info(f'Добавлен новый статус {status_name}')

    # получение текущего состояния юзера в сервере статусов
    def select_user_status_server(self, user_id):
        """
        Получение текущего состояния юзера в сервере статуса
        :param user_id: идентификатор пользователя в ВК
        :return: возвращает описание статуса и id статуса
        """
        sql = "SELECT status_server.id_status, status.status " \
              "FROM status_server INNER JOIN status ON status_server.id_status=status.id " \
              f"WHERE status_server.id_user_vk={user_id};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        return result

    # удаление описателя статуса
    def delete_status(self, status_name):
        # проверка использования статуса в таблице сервера состояний

        sql = "DELETE FROM status WHERE id = %s;"
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        logging.info(f'Удаление статуса {status_name}')
