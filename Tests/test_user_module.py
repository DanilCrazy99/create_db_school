# -*- coding: utf-8 -*-
# тесты для проверки функций работы с данными в user.py

import unittest

from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Config.Var_community import user_admin


class ControlUser(unittest.TestCase):
    def setUp(self) -> None:
        """
        Создаём экземпляр класса User
        """
        self.user = Community()
        self.user_id = user_admin

    def test_chat_vk(self):
        """
        Тестирование чатов
        """
        self.assertTrue(self.user.title_chat(user_id=self.user_id))

    def test_select_chat_db(self):
        """
        Тест доступности данных о чатах из БД.
        """



if __name__ == '__main__':
    unittest.main()
