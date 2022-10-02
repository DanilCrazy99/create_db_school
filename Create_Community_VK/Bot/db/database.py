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
        :return: строка SQL запроса и словарь из параметров
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
        """
        Добавляет новый статус в таблицу status
        :param status_name: описание статуса
        """
        sql = "INSERT INTO status(status) VALUES (%s);"
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        logging.info(f'Добавлен новый статус {status_name}')

    def select_status(self, key_stat):
        """
        Получаем ID статуса по ключу статуса в таблице статусов
        :param key_stat: int
        :return: int
        """
        sql = f"SELECT id FROM public.status WHERE key_stats_1 = {key_stat};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        return result

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

    def update_status_server(self, user_id, status_id):
        """
        Обновление статуса пользователя в таблице status_server
        :param user_id: ID пользователя в ВК
        :param status_id: ID устанавливаемого статуса из таблицы status
        """
        sql = "UPDATE status_server SET id_status=%s WHERE id_user_vk=%s;"
        parameter = (status_id, user_id)
        self.__cursor.execute(sql, parameter)
        self.__connect.commit()

    def select_key_stats_1(self, status_id):
        """
        Получаем INT значение статуса по его ID
        :param status_id: ID статуса в таблице status
        :return: int значение key_stats_1
        """
        sql = f"SELECT key_stats_1 FROM status WHERE id={status_id};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        return result

    def insert_user_status_server(self, user_id_vk, status_id):
        """
        Добавление записи в БД по юзеру с указанием его текущего статуса
        :param user_id_vk: идентификатор пользователя в ВК
        :param status_id: ID статуса состояний юзера
        """
        sql = "INSERT INTO status_server(id_user_vk, id_status) VALUES (%s, %s);"
        parameter = (user_id_vk, status_id)
        self.__cursor.execute(sql, parameter)
        self.__connect.commit()
        logging.info(f'Изменен статус пользователя {user_id_vk} на {status_id}')

    # удаление описателя статуса
    def delete_status(self, status_name):
        # проверка использования статуса в таблице сервера состояний

        sql = "DELETE FROM status WHERE id = %s;"
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        logging.info(f'Удаление статуса {status_name}')

    def current_schedule(self):
        """
        Получение начального и конечного ID таблицы timetable
        :return: начальный и конечный id. Если таблица пуста присвоить значения 0
        """
        result = []
        sql = "SELECT id, time_update, time_activate, editor_user_id, id_timetable " \
              "FROM timetable_time_activate " \
              "WHERE time_activate <= CURRENT_DATE ORDER BY time_activate DESC;"
        self.__cursor.execute(sql)
        response = self.__cursor.fetchone()
        start_id = response[4]  # получение начала в таблице time_table
        id_start_activate = response[0]
        stop_id = self.next_post_id_activate(id_start_activate)  # получение окончания в таблице time_table

        result.append(start_id)
        result.append(stop_id)
        return result

    def next_post_id_activate(self, start_id):
        """
        Получение ID окончания данных залитого файла в таблице time_table
        :param start_id: ID первой записи
        :return: последняя запись
        """
        sql = f"SELECT id, id_timetable FROM timetable_time_activate WHERE id > {start_id} ORDER BY id_timetable ASC;"
        self.__cursor.execute(sql)
        stop_id = self.__cursor.fetchone()  # получение конца таблицы расписания в time_table
        if stop_id:
            # если есть записи после активного расписания
            result = stop_id[1] - 1
        else:
            # если записей выше не нашло, то вытаскиваем MAX значение из таблицы time_table
            sql = "SELECT MAX(id) FROM timetable;"
            self.__cursor.execute(sql)
            stop_id = self.__cursor.fetchone()  # получение последнего ID в time_table
            result = stop_id[0]
        return result

    def select_time_table_activate(self, class_letter='', week_day=''):
        """
        получаем текущее активное расписание
        :param class_letter: название запрашиваемого класса
        :param week_day: день недели если пустой то вся неделя
        :return: список активного расписания
        """
        id_table_borders = self.current_schedule()  # получаем границы активного расписания
        sql = "SELECT id, class, lesson_number, academic_discipline, day_of_week " \
              "FROM timetable " \
              f"WHERE id >= {id_table_borders[0]} AND id <= {id_table_borders[1]} "
        if class_letter != '':
            sql += f" AND class = '{class_letter}' "
        if week_day != '':
            sql += f" AND day_of_week = '{week_day}' "
        sql += "ORDER BY class, day_of_week, lesson_number ASC;"
        self.__cursor.execute(sql)
        response = self.__cursor.fetchall()  # получение последнего ID в time_table
        return response

    def select_user_data(self, id_user_vk):
        """
        Получение данных по пользователю из таблицы users
        :param id_user_vk: ID пользователя ВК
        :return: list(role_id, invitation_sent, time_unanswered_msg)
        """
        sql = f"SELECT role_id, invitation_sent, time_unanswered_msg FROM users WHERE user_id_vk={id_user_vk};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()
        return result

    def select_role_data(self, id_role):
        """
        Получение описания роли по её ID
        :param id_role: int
        :return: list
        """
        sql = f"SELECT id, role, description FROM public.role WHERE id={id_role};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()
        return result
