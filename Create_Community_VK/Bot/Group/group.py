# -*- coding: utf-8 -*-
import vk_api
import requests
from Create_Community_VK.Config.Var_community import token_group


class Group:
    """
    Класс для работы с данными группы
    """
    def __init__(self, token_in_class=token_group):
        # присваиваю переменной token токен группы
        self.__token = token_in_class
        self.vk = vk_api.VkApi(token=self.__token)
        # используем .vk_api() для вызова API
        self.vk_api = self.vk.get_api()
        # self.id_chat = ''
        self.getConversation_Mem = self.vk_api.messages.getConversationMembers
        self.getChatList = self.vk_api.messages.getConversations
        self.list_ids = []

    def get_chats_ids(self):
        """
        Получаем ID чатов группы
        :return: список ID чатов
        """
        list_items = self.getChatList()
        list_ids = []
        for a in range(len(list_items['items'])):
            if list_items['items'][a]['conversation']['peer']['type'] == 'chat':
                list_ids.append(list_items['items'][a]['conversation']['peer']['id'])
        return list_ids

    def get_chats_title(self):
        """
        Получение названий всех чатов группы
        :return: список чатов классов
        """
        pass

    def grouping_chats(self):
        """
        Группировка чатов в списки по критерию начальная/средняя школа
        :return: словарь сгруппированных словарей чатов: уровень школы / поток классов
        """
        # Пример: {'primary': {1: {'A': 'link', 'B': 'link'}, 2:{}}, 'secondary': {5: {'A': 'link', 'B': 'link'}, 6:{}}}
        # генерируем списки уровней школы, потоков классов и ссылки на литеры классов потока
        level_school = dict.fromkeys(['primary', 'secondary'])
        class_flow = dict.fromkeys(['flow', 'number'])
        class_level = dict.fromkeys(['liter', 'linc'])
        pass
