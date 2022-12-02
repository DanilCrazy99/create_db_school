# -*- coding: utf-8 -*-
# класс по работе с чатами

from Create_Community_VK.Bot.db.database import DataBase


class Chat:
    """
    Класс чат. Работа с чатами.
    """
    def __init__(self):
        self.db = DataBase()

    def data_chat_from_db(self, id_chat_vk=None):
        """
        Получить данные чата/чатов пользователя.
        :param id_chat_vk: ID чата в ВК
        :return: список чатов
        """
        sql = "SELECT id, id_chat_vk, title_chat, link_chat FROM chat_link"
        if id_chat_vk:
            sql += f" WHERE id_chat_vk={id_chat_vk};"
        else:
            sql += ";"
        result = self.db.select_db(sql=sql)
        return result




if __name__ == '__main__':
    print('test')
