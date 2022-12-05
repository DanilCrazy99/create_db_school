# -*- coding: utf-8 -*-
# класс по работе с чатами

from operator import itemgetter
from Create_Community_VK.Bot.db.database import DataBase
from Create_Community_VK.Config.Var_community import LEVEL_PRIMARY
from Create_Community_VK.Bot.Users.user import Community


class Chat:
    """
    Класс чат. Работа с чатами.
    """
    def __init__(self):
        self.db = DataBase()
        self.user = Community()

    def data_chat_from_db(self, id_chat_vk=None):
        """
        Получить данные чата/чатов.
        :param id_chat_vk: ID чата в ВК
        :return: список чатов
        """
        sql = "SELECT id, id_chat_vk, title_chat, link_chat FROM chat_link"
        params = {}
        if id_chat_vk:
            sql += f" WHERE "
            params = {'id_chat_vk': id_chat_vk}

        result = self.db.select_db(sql=sql, parameters=params)
        return result

    def number_letter_chat(self, title_chat):
        """
        Создаем список вида (цифра, буква)
        :param title_chat: Название чата
        :return: list {(),()}
        """
        number_letter = []
        for item in title_chat:
            number_letter.append((item[2][:-1], item[2][-1:]))
        return number_letter

    def grouping_chats_number(self, primary_school=False):
        """
        Группировка чатов в списки по критерию начальная/средняя школа

        :return: словарь поток классов
        """

        # получаем данные по чатам из БД
        chat = self.number_letter_chat(self.data_chat_from_db())

        class_level = []
        level_p = 0
        level_h = 0
        if chat:
            for a in chat:
                number_level = int(a[0])
                if primary_school and number_level <= LEVEL_PRIMARY:
                    if not (number_level in class_level):
                        class_level.append(number_level)
                if not primary_school and number_level > LEVEL_PRIMARY:
                    if not (number_level in class_level):
                        class_level.append(number_level)
            class_level.sort()
        return class_level

    def litter_level_chat(self, level):
        """
        Получаем список по срезу потока

        :param level: int номер потока
        :return: список.(Title chat and url chat)
        """
        chat = self.data_chat_from_db()
        # создаем список с полями (поток/буква/title/url)
        new_list_chat = []
        for item in chat:
            if int(item[2][:-1]) == level:
                new_list_chat.append((item[2][:-1], item[2][-1:], item[2], item[3]))
        # сортируем список по 2-му ключу вложенного списка
        sort_chat = sorted(new_list_chat, key=itemgetter(2))
        return sort_chat

    def title_chat(self, user_id_vk):
        """
        Получаем название чатов группы, где состоит пользователь.
        :param user_id_vk: ID пользователя в ВК
        :return: Список названий чатов
        """
        result = ()
        # получаем список ID чатов из бд, где зарегистрирован пользователь.
        list_chat_id_user_db = self.user.chat_id_from_user_db(user_id_vk=user_id_vk)[0]
        list_chat_title = []
        sql = 'SELECT id, id_chat_vk, title_chat, link_chat	FROM chat_link'
        # Создаем SQL запрос. Проверка на пустоту первого элемента списка ID чатов.
        if list_chat_id_user_db[0]:
            if len(list_chat_id_user_db[0]) != 0:
                sql += ' WHERE'
                sql += " OR ".join([
                    f" id = {item}" for item in list_chat_id_user_db[0]
                ])
                sql += ';'

                result = self.db.select_db(sql=sql)

        for items in result:
            # вытаскиваем Названия чатов.
            list_chat_title.append(items[2])
        return list_chat_title


if __name__ == '__main__':
    print('test')
