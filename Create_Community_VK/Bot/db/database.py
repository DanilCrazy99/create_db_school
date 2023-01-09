# -*- coding: utf-8 -*-
# файл для работы с бд Postgresql

import psycopg2
import logging

from Create_Database.Config.Var_database import schoolName, user, password, host, port
from Create_Community_VK.Bot.Group.group import Group


class DataBase:
    def __init__(self):
        self.__connect = psycopg2.connect(
                        database=schoolName,
                        user=user,
                        password=password,
                        host=host,
                        port=port
        )
        self.__cursor = ''  # self.__connect.cursor()
        self.__group = Group()
        self.list_role = []

    def format_args(self, body_sql, parameters: dict):
        """
        Создание параметра запроса для WHERE с условием AND
        :param body_sql: начальная часть запроса с WHERE
        :param parameters: именованный словарь с условиями. пример: {"поле_БД": переменная по которой будет выборка}
        :return: строка SQL запроса и словарь из параметров
        """
        body_sql += " AND ".join([
            f"{item} = %s" for item in parameters
        ])
        body_sql += ';'
        return body_sql, tuple(parameters.values())

    def select_db(self, sql, parameters=None):
        """
        Получение данных из БД.
        :param sql: строка SQL запроса.
        :param parameters: именованный словарь с условиями. пример: {"поле_БД": значение по которому будет выборка}
        :return:
        """
        if not parameters:
            parameters = {}
        sql, parameter = self.format_args(body_sql=sql, parameters=parameters)

        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, parameter)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def change_db(self, sql):
        """
        Изменение/добавление данных в БД
        :param sql: строка SQL запроса.
        :return:
        """

        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        self.__connect.commit()
        self.__cursor.close()
        return True

    def load_data(self, data=[]):
        """
        Загрузка данных в БД
        :param data: список данных ([])
        :return:
        """
        for item in data:
            sql = "INSERT INTO status(status_member, key_stats_1) VALUES (%s, %s);"
            parameter = (item[0], item[1])
            self.__cursor = self.__connect.cursor()
            self.__cursor.execute(sql, parameter)
            self.__connect.commit()
            self.__cursor.close()

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

        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    # добавление описателя статуса
    def insert_status_name(self, status_name):
        """
        Добавляет новый статус в таблицу status
        :param status_name: описание статуса
        """
        sql = "INSERT INTO status(status) VALUES (%s);"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        self.__cursor.close()
        logging.info(f'Добавлен новый статус {status_name}')

    def update_status_user(self, id_user_vk, number_status):
        """
        Обновление статуса юзера в таблице сервера состояний
        :param id_user_vk: ID пользователя в ВК
        :param number_status: Номер текущего статуса пользователя.
        """
        sql = "UPDATE status_server SET id_status=%s WHERE id_user_vk=%s;"
        params = (number_status, id_user_vk)
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, params)
        self.__connect.commit()
        self.__cursor.close()

    def select_status(self, key_stat):
        """
        Получаем ID статуса по ключу статуса в таблице статусов
        :param key_stat: int
        :return: int
        """
        sql = f"SELECT id FROM status WHERE key_stats_1 = {key_stat};"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        self.__cursor.close()
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
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        self.__cursor.close()
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
            self.__cursor = self.__connect.cursor()
            self.__cursor.execute(sql, parameter)
            self.__connect.commit()
            self.__cursor.close()
            logging.info(f'Добавлен пользователь в таб status_server {user_id_vk} на {status_id}')

    def select_user(self, user_id_vk):
        """
        Получение текущего данных юзера.

        :param user_id_vk: идентификатор пользователя в ВК
        :return: возвращает данные по юзеру
        """
        sql = f"SELECT user_id_vk, role_id, invitation_sent, command_executable, time_completion " \
              f"FROM users WHERE user_id_vk={user_id_vk};"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        self.__cursor.close()
        return result

    def insert_user(self, user_id, role_id):
        """
        Добавление данных нового юзера.

        :param user_id: идентификатор пользователя в ВК
        :param role_id: идентификатор роли в БД
        :return: возвращает ID юзера в БД
        """
        # проверка на наличие в БД юзера с пришедшим ID
        result = self.select_user(user_id_vk=user_id)
        if not result:
            sql = "INSERT INTO users(user_id_vk, role_id, invitation_sent) VALUES (%s, %s, %s) RETURNING id;"
            # параметр invitation_sent ставим в False (не отправлено)
            invitation = False
            self.list_role.append(role_id)  # добавляем учет роли
            parameter = (user_id, self.list_role, invitation)
            self.__cursor = self.__connect.cursor()
            self.__cursor.execute(sql, parameter)
            id_user_db = self.__cursor.fetchone()[0]
            self.__connect.commit()
            self.__cursor.close()
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
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        response = self.__cursor.fetchone()  # получение единичной записи
        self.__cursor.close()
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
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        self.__connect.commit()
        self.__cursor.close()

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
            # получить список ролей и обновить его
            list_role = self.new_list_role(role_id_db=role_id, user_id_vk=user_id_vk)
            sql += " role_id=%s"
            parameter.append(list_role)
        if schedule_date != '':
            sql += " latest_schedule_date=%s"
            parameter.append(schedule_date)
        sql += " WHERE user_id_vk=%s;"
        parameter.append(user_id_vk)
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, parameter)
        self.__connect.commit()
        self.__cursor.close()

    def new_list_role(self, role_id_db, user_id_vk):
        """
        обновление списка ролей
        :return: list role
        """
        list_role = self.select_user(user_id_vk=user_id_vk)[1]
        new_role_flag = 1  # флаг добавления новой роли

        if self.select_id_role(role='visitor') == role_id_db:
            # если роль меняется на visitor, то все роли удаляются оставляем только visitor
            new_role_flag = 0  # сброс флага новой роли
            list_role.clear()
            list_role.append(role_id_db)

        if new_role_flag == 1:
            if role_id_db not in list_role:
                list_role.append(role_id_db)

        return list_role

    def select_id_role(self, role):
        """
        Получение ID роли пользователя согласно БД

        :param role: str Роль юзера в группе
        :return: int ID роли в БД.
        """
        sql = f"SELECT id, role, description FROM role WHERE role='{role}';"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        request = self.__cursor.fetchone()  # получение единичной записи
        self.__cursor.close()
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
            self.__cursor = self.__connect.cursor()
            self.__cursor.execute(sql, parameter)
            result = self.__cursor.fetchone()[0]
            self.__connect.commit()
            self.__cursor.close()
            logging.info(f'Добавлена новая роль {role_name}')
        return result

    def select_key_stats_1(self, status_id):
        """
        Получаем INT значение статуса по его ID
        :param status_id: ID статуса в таблице status
        :return: int значение key_stats_1
        """
        sql = f"SELECT key_stats_1 FROM status WHERE id={status_id};"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()  # получение единичной записи
        self.__cursor.close()
        return result

    # удаление описателя статуса
    def delete_status(self, status_name):
        """
        Проверка использования статуса в таблице сервера состояний.

        :param status_name: str Имя статуса.
        """
        sql = "DELETE FROM status WHERE id = %s;"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, status_name)
        self.__connect.commit()
        self.__cursor.close()
        logging.info(f'Удаление статуса {status_name}')

    def current_schedule(self, selected_day='', class_letter=''):
        """
        Получение начального и конечного ID таблицы timetable
        :param selected_day: дата выбранного дня(вида "10/24/2022")
        :param class_letter: обозначение потока класса
        :return: начальный и конечный id. Если таблица пуста присвоить значения 0
        """
        result = []
        start_id = 0
        stop_id = 0
        # Запрос получения данных относительно текущего календарного дня
        # с сортировкой заливки файла от последнего к первому.
        # убрал условие по классу  AND class_flow = '{get_flow(class_letter)}'
        sql = "SELECT id, time_update, time_activate, editor_user_id, id_timetable " \
              "FROM timetable_time_activate " \
              f"WHERE time_activate <= '{selected_day}' AND active = true " \
              f"ORDER BY id DESC;"  # LOCALTIMESTAMP
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        response = self.__cursor.fetchone()
        self.__cursor.close()
        if response:
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
        self.__cursor = self.__connect.cursor()
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

        self.__cursor.close()
        return result

    def select_time_table_activate(self, class_letter='', week_day='', selected_day=''):
        """
        Получаем текущее активное расписание для конкретного класса.

        :param class_letter: название запрашиваемого класса.
        :param week_day: день недели если пустой то вся неделя.
        :param selected_day: дата выбранного дня(вида "10/24/2022")
        :return: список активного расписания
        """
        # получить один ID ближайшего активного расписания.
        id_activate_time_table = self.select_one_activate_timetable(class_letter=class_letter,
                                                                    week_day=week_day,
                                                                    selected_day=selected_day)

        sql = "SELECT class, " \
              "lesson_number, CONCAT(time_lesson, ' ', academic_discipline.name, ' ' , room_lesson), " \
              "day_of_week " \
              "FROM timetable INNER JOIN academic_discipline ON academic_discipline.id = timetable.id_discipline " \
              f"WHERE class = '{class_letter}' " \
              f"AND id_timetable = '{id_activate_time_table}' " \
              f"AND day_of_week = '{week_day}'" \
              "	ORDER BY lesson_number ASC;"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        response = self.__cursor.fetchall()  # получение расписания на день
        self.__cursor.close()
        return response

    def select_one_activate_timetable(self, class_letter='', week_day='', selected_day=''):
        """
        получить один ID ближайшего активного расписания.
        :return: ID активного расписания
        """
        # print('selected_day=', selected_day)
        sql = "SELECT timetable_time_activate.id " \
              "FROM timetable INNER JOIN timetable_time_activate " \
              "ON timetable.id_timetable = timetable_time_activate.id " \
              f"WHERE class = '{class_letter}' AND time_activate <= '{selected_day}' AND day_of_week = '{week_day}' " \
              "ORDER BY time_activate DESC;"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        response = self.__cursor.fetchone()  # получение ID активного расписания
        self.__cursor.close()
        if response:
            response = response[0]
        else:
            response = 0
        return response

    def select_user_data(self, id_user_vk):
        """
        Получение данных по пользователю из таблицы users
        :param id_user_vk: ID пользователя ВК
        :return: list(role_id, invitation_sent, command_executable, time_completion)
        """
        sql = f"SELECT id, role_id, invitation_sent, command_executable, time_completion FROM users WHERE user_id_vk={id_user_vk};"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()
        self.__cursor.close()
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
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def insert_chat(self, data_chat=()):
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
                self.__cursor = self.__connect.cursor()
                self.__cursor.execute(sql, parameter)
                self.__connect.commit()
                self.__cursor.close()

    def editor_time_table_db(self):
        """
        Получить список редакторов расписания.
        :return: list user editor time_table
        """
        list_editor = ['creator', 'editor_time_table']
        sql = 'SELECT user_id_vk FROM users INNER JOIN role on role.id = users.role_id WHERE '
        sql += " AND ".join([
            f" role.role = '{item}'" for item in list_editor
            ])
        sql += ';'
        result = self.select_db(sql=sql)
        return result

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
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, parameter)
        self.__connect.commit()
        self.__cursor.close()

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
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def delete_chat(self, id_chat_vk):
        """
        Удаление данных чата из БД
        :param id_chat_vk:  int ID чата в ВК
        :return:
        """
        sql = f"DELETE FROM chat_link WHERE id_chat_vk=%s;"
        self.__cursor = self.__connect.cursor()
        self.__cursor.execute(sql, id_chat_vk)
        self.__connect.commit()
        self.__cursor.close()
        logging.info(f'Удаление данных чата {id_chat_vk}')


def get_flow(class_letter=''):
    """
    Получаем поток класса
    :param class_letter: обозначение класса
    :return: str
    """
    flow = str(class_letter[:-1])
    return flow
