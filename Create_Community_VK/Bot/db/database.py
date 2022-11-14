# -*- coding: utf-8 -*-
# файл для работы с бд Postgresql

import sys
import os
import psycopg2
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../../Create_Database'))
sys.path.insert(1, os.path.join(sys.path[0], 'Create_Database'))

from Config.Var_database import schoolName, user, password, host, port

sys.path.insert(1, os.path.join(sys.path[0], '../../Create_Community_VK'))
sys.path.insert(1, os.path.join(sys.path[0], 'Create_Community_VK'))

from Bot.Group.group import Group


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
        self.__group = Group()

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

    def load_data(self, data=[]):
        """
        Загрузка данных в БД
        :param data: список данных ([])
        :return:
        """
        for item in data:
            sql = "INSERT INTO status(status_member, key_stats_1) VALUES (%s, %s);"
            parametr = (item[0], item[1])
            self.__cursor.execute(sql, parametr)
            self.__connect.commit()

    def select_timetable_class(self, week_day=[], class_letter=[]):
        """
        Получение выборки расписания по дню недели
        """
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

    def select_roles_with_vk_id(self, id_user):
        """
        Проверка на наличие специфичной роли в postgres
        """
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

    def update_status_user(self, id_user_vk, number_status):
        """
        Обновление статуса юзера в таблице сервера состояний
        :param id_user_vk: ID пользователя в ВК
        :param number_status: Номер текущего статуса пользователя.
        """
        sql = "UPDATE status_server SET id_status=%s WHERE id_user_vk=%s;"
        params = (number_status, id_user_vk)
        self.__cursor.execute(sql, params)
        self.__connect.commit()

    def select_status(self, key_stat):
        """
        Получаем ID статуса по ключу статуса в таблице статусов
        :param key_stat: int
        :return: int
        """
        sql = f"SELECT id FROM status WHERE key_stats_1 = {key_stat};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        return result

    def select_user_status_server(self, id_user_vk):
        """
        Получение текущего состояния юзера в сервере статуса

        :param id_user_vk: идентификатор пользователя в ВК
        :return: возвращает описание статуса и id статуса
        """
        sql = "SELECT status_server.id_status, status.status_member, status.key_stats_1 " \
              "FROM status_server INNER JOIN status ON status_server.id_status=status.id " \
              f"WHERE status_server.id_user_vk={id_user_vk};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        return result

    def insert_user_status_server(self, user_id_vk, status_id):
        """
        Добавление записи в БД по юзеру с указанием его текущего статуса

        :param user_id_vk: идентификатор пользователя в ВК
        :param status_id: ID статуса состояний юзера
        """
        if not self.select_user_status_server(id_user_vk=user_id_vk):
            sql = "INSERT INTO status_server(id_user_vk, id_status) VALUES (%s, %s);"
            parameter = (user_id_vk, status_id)
            self.__cursor.execute(sql, parameter)
            self.__connect.commit()
            logging.info(f'Добавлен пользователь в таб status_server {user_id_vk} на {status_id}')

    def select_user(self, user_id):
        """
        Получение текущего данных юзера.

        :param user_id: идентификатор пользователя в ВК
        :return: возвращает данные по юзеру
        """
        sql = f"SELECT user_id_vk, role_id, invitation_sent, command_executable, time_completion " \
              f"FROM users WHERE user_id_vk={user_id};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        return result

    def insert_user(self, user_id, role_id):
        """
        Добавление данных нового юзера.

        :param user_id: идентификатор пользователя в ВК
        :param role_id: идентификатор роли в БД
        :return: возвращает ID юзера в БД
        """
        # проверка на наличие в БД юзера с пришедшим ID
        result = self.select_user(user_id=user_id)
        if not result:
            sql = "INSERT INTO users(user_id_vk, role_id, invitation_sent) VALUES (%s, %s, %s) RETURNING id;"
            # параметр invitation_sent ставим в False (не отправлено)
            invitation = False
            parameter = (user_id, role_id, invitation)
            self.__cursor.execute(sql, parameter)
            id_user_db = self.__cursor.fetchone()[0]
            self.__connect.commit()
            logging.info(f'У нас новый член группы id={user_id}')
            return id_user_db
        else:  # иначе обновляем данные по юзеру
            self.update_user(user_id_vk=user_id, role_id=role_id)
            id_user_db = self.select_user_data(id_user_vk=user_id)
            return id_user_db[0]

    def select_invitation_msg_user(self, user_id_vk):
        """
        Статуса контроля отправки приглашения вступления в группу

        :param user_id_vk: int ID пользователя в БД
        :return: bool Статус отправки приглашения
        """
        result = False
        sql = f"SELECT invitation_sent FROM users WHERE user_id_vk={user_id_vk};"
        self.__cursor.execute(sql)
        response = self.__cursor.fetchone()  # получение единичной записи
        if response:
            result = response[0]
        return result

    def update_invitation_msg_user(self, user_id_vk, invitation=True):
        """
        Меняем статус отправки приглашения вступления в группу на TRUE

        :param user_id_vk: int ID пользователя в ВК
        :param invitation: статус отправки приглашения пользователю
        """
        sql = f"UPDATE users SET invitation_sent={invitation} WHERE user_id_vk={user_id_vk};"
        self.__cursor.execute(sql)
        self.__connect.commit()

    def update_user(self, user_id_vk, role_id=0, schedule_date=''):
        """
        Обновление данных пользователя

        :param user_id_vk: ID юзера в ВК
        :param role_id: ID роли в БД
        :param schedule_date: Дата последнего запроса расписания.
        :return: возвращает ID юзера в БД
        """
        parameter = []
        sql = "UPDATE users SET"
        if role_id != 0:
            sql += " role_id=%s"
            parameter.append(role_id)
        if schedule_date != '':
            sql += " latest_schedule_date=%s"
            parameter.append(schedule_date)
        sql += " WHERE user_id_vk=%s;"
        parameter.append(user_id_vk)
        self.__cursor.execute(sql, parameter)
        self.__connect.commit()

    def select_id_role(self, role):
        """
        Получение ID роли пользователя согласно БД

        :param role: str Роль юзера в группе
        :return: int ID роли в БД.
        """
        sql = f"SELECT id, role, description FROM role WHERE role='{role}';"
        self.__cursor.execute(sql)
        request = self.__cursor.fetchone()  # получение единичной записи
        if not request:
            # Добавляем новую роль
            result = self.insert_role(role_name=role)
        else:
            result = request[0]
        return result

    def insert_role(self, role_name, role_desc=''):
        """
        Добавляем новую роль
        :param role_name: str имя роли
        :param role_desc: str описание роли
        :return: ID новой роли
        """
        # проверяем существование роли в таблице role
        check = self.select_role_data(name_role=role_name)
        if check:
            result = check[0][0]
        else:
            parameter = (role_name, role_desc)
            sql = "INSERT INTO role(role, description) VALUES (%s, %s) RETURNING id;"
            self.__cursor.execute(sql, parameter)
            result = self.__cursor.fetchone()[0]
            self.__connect.commit()
            logging.info(f'Добавлена новая роль {role_name}')
        return result

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

    # удаление описателя статуса
    def delete_status(self, status_name):
        """
        Проверка использования статуса в таблице сервера состояний.

        :param status_name: str Имя статуса.
        """
        sql = "DELETE FROM status WHERE id = %s;"
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        logging.info(f'Удаление статуса {status_name}')

    def current_schedule(self, selected_day='', class_letter=''):
        """
        Получение начального и конечного ID таблицы timetable
        :param selected_day: дата выбранного дня(вида "10/24/2022")
        :param class_letter: обозначение потока класса
        :return: начальный и конечный id. Если таблица пуста присвоить значения 0
        """
        result = []
        # Запрос получения данных относительно текущего календарного дня
        # с сортировкой заливки файла от последнего к первому.
        sql = "SELECT id, time_update, time_activate, editor_user_id, id_timetable " \
              "FROM timetable_time_activate " \
              f"WHERE time_activate <= '{selected_day}' AND class_flow = '{get_flow(class_letter)}' " \
              f"ORDER BY time_activate DESC;"  # LOCALTIMESTAMP
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

    def select_time_table_activate(self, class_letter='', week_day='', selected_day=''):
        """
        Получаем текущее активное расписание для конкретного класса.

        :param class_letter: название запрашиваемого класса.
        :param week_day: день недели если пустой то вся неделя.
        :param selected_day: tr дата выбранного дня(вида "10/24/2022")
        :return: список активного расписания
        """
        # получаем границы активного расписания для конкретного класса
        id_table_borders = self.current_schedule(selected_day=selected_day, class_letter=class_letter)
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
        :return: list(role_id, invitation_sent, command_executable, time_completion)
        """
        sql = f"SELECT id, role_id, invitation_sent, command_executable, time_completion FROM users WHERE user_id_vk={id_user_vk};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()
        return result

    def select_role_data(self, id_role=None, name_role=None):
        """
        Получение описания роли по её ID или Name

        :param id_role: int Не обязательный
        :param name_role: str Не обязательный
        :return: list содержит кортеж(и) с данными
        """
        sql = f"SELECT id, role, description FROM public.role"
        if not name_role and not id_role:
            sql += ';'

        if name_role:
            sql += f" WHERE role='{name_role}';"

        # Если имя роли было пустым, то выборка по ID
        if id_role and not name_role:
            sql += f" WHERE id={id_role};"
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result

    def insert_chat(self):
        """
        Добавляем данные о существующих чатах группы в таблицу чатов БД.
        """
        data_chat = self.__group.get_chats()
        for item in data_chat:
            if self.select_chat(item[3]):
                # если запись существует обновляем её
                self.update_chat(id_chat_vk=item[3], title_chat=item[2], link_chat=item[5])
            else:
                # если нет записи. то создаём
                parameter = (item[3], item[2], item[5])
                sql = "INSERT INTO public.chat_link(id_chat_vk, title_chat, link_chat) VALUES (%s, %s, %s);"
                self.__cursor.execute(sql, parameter)
                self.__connect.commit()

    def update_chat(self, id_chat_vk, title_chat, link_chat):
        """
        Обновление данных чата.
        :param id_chat_vk: int ID чата в ВК
        :param title_chat: название чата
        :param link_chat: ссылка на чат
        :return:
        """
        sql = "UPDATE chat_link SET title_chat=%s, link_chat=%s WHERE id_chat_vk=%s;"
        parameter = (title_chat, link_chat, id_chat_vk)
        self.__cursor.execute(sql, parameter)
        self.__connect.commit()

    def select_chat(self, id_chat_vk=None):
        """
        Получение данных чата из БД
        :param id_chat_vk:  int ID чата в ВК
        :return:
        """
        sql = "SELECT id, id_chat_vk, title_chat, link_chat FROM chat_link"
        if id_chat_vk:
            sql += f" WHERE id_chat_vk={id_chat_vk};"
        else:
            sql += ";"
        # print('sql= ', sql)
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        return result

    def delete_chat(self, id_chat_vk):
        """
        Удаление данных чата из БД
        :param id_chat_vk:  int ID чата в ВК
        :return:
        """
        sql = f"DELETE FROM chat_link WHERE id_chat_vk=%s;"
        self.__cursor.execute(sql, id_chat_vk)
        self.__connect.commit()
        logging.info(f'Удаление данных чата {id_chat_vk}')


def get_flow(class_letter=''):
    """
    Получаем поток класса
    :param class_letter: обозначение класса
    :return: str
    """
    flow = str(class_letter[:-1])
    return flow
