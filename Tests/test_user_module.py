# -*- coding: utf-8 -*-
# тесты для проверки функций работы с данными в user.py

import unittest

from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Config.Var_community import user_admin
from Create_Community_VK.Bot.Chat.chat import Chat


class ControlUser(unittest.TestCase):
    def setUp(self) -> None:
        """
        Создаём экземпляр класса User
        """
        self.user = Community()
        self.chat = Chat()
        self.user_id = user_admin

    # def test_chat_vk(self):
    #     """
    #     Тестирование чатов
    #     """
    #     self.assertTrue(self.user.title_chat(user_id=self.user_id))

    def test_select_chat_db(self):
        """
        Тест доступности данных о чатах из БД.
        """
        # позитивный сценарий
        self.assertTrue(self.chat.data_chat_from_db())

    def test_select_list_chat_db(self):
        """
        Тест получения данных о чатах из БД.
        """
        # позитивный сценарий
        self.assertTrue(self.chat.data_chat_from_db() != [])

    def test_select_list_id_chat_user(self):
        """
        Тест получения списка ID из БД, чатов пользователя.
        """
        self.assertTrue(len(self.user.chat_id_from_user_db(user_id_vk=696195563)) != 0)


if __name__ == '__main__':
    unittest.main()
