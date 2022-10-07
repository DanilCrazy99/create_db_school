# -*- coding: utf-8 -*-
import vk_api
from Create_Community_VK.Config.Var_community import token_group, group_id, LEVEL_PRIMARY
from operator import itemgetter, attrgetter, methodcaller


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
        self.list_ids = []

    def get_chats_ids(self):
        """
        Получаем ID чатов группы
        :return: список ID чатов
        """
        list_items = self.vk_api.messages.getConversations()
        list_ids = []
        print('list-items= ', list_items)
        for a in range(len(list_items['items'])):
            if list_items['items'][a]['conversation']['peer']['type'] == 'chat':
                list_ids.append(list_items['items'][a]['conversation']['peer']['id'])
        return list_ids

    def get_chats(self):
        """
        Получаем список чатов группы

        :return: список чатов
        """
        list_items = self.vk_api.messages.getConversations()
        list_ids = []
        group_chat = []
        chat_data = []
        for a in range(len(list_items['items'])):
            if list_items['items'][a]['conversation']['peer']['type'] == 'chat':
                title_chat = list_items['items'][a]['conversation']['chat_settings']['title']

                id_chat = list_items['items'][a]['conversation']['peer']['id']

                group_chat.append((title_chat[:-1], title_chat[-1:], title_chat, id_chat))

        return group_chat

    def get_link_chats(self, id_chat, new_link=0):
        """
        Получение ссылки на чат по его ID.
        По умолчанию генерируется новая ссылка. Для получения новой ссылки new_link=1
        :return: ссылка для вступления в chat
        """
        link = self.vk_api.messages.getInviteLink(peer_id=id_chat, reset=new_link, group_id=group_id)['link']
        return link

    def grouping_chats_level(self, primary_school=False):
        """
        Группировка чатов в списки по критерию начальная/средняя школа

        :return: словарь поток классов
        """
        chat = self.get_chats()
        # сортируем список по 2-му ключу вложенного списка
        sort_chat = sorted(chat, key=itemgetter(2))
        class_level = []
        level_p = 0
        level_h = 0
        if chat:
            for a in sort_chat:
                number_level = a[0]
                if primary_school and int(number_level) <= LEVEL_PRIMARY:
                    if number_level != level_p:
                        class_level.append(number_level)
                        level_p = number_level
                if not primary_school and int(number_level) > LEVEL_PRIMARY:
                    if number_level != level_h:
                        class_level.append(number_level)
                        level_h = number_level
        return class_level

    def litter_level_chat(self, level):
        """
        Получаем список по срезу потока

        :param level: int номер потока
        :return: список
        """
        chat = self.get_chats()
        # сортируем список по 2-му ключу вложенного списка
        sort_chat = sorted(chat, key=itemgetter(2))
        class_litter = []
        level_litter = ''
        if chat:
            for a in sort_chat:
                number_level = a[0]
                litter = a[1]
                if str(level) == number_level and litter != level_litter:
                    link_extend = list(a)
                    link_extend.append(self.get_link_chats(id_chat=a[3]))
                    class_litter.append(link_extend)
                    level_litter = litter
        return class_litter

    def member_group(self, id_user):
        """
        Проверка на участие в нашей группе

        :return: True / False
        """
        if group_id != id_user and group_id != (-1 * id_user):
            result = self.vk.method('groups.isMember', {'group_id': group_id,
                                                        'user_id': id_user})
        else:
            result = 1

        if result == 1:
            return True
        return False

    def admins_group(self):
        """
        Достает список администраторов группы

        :return: list
        """
        result = self.vk.method("groups.getMembers", {'group_id': group_id,
                                                      'filter': 'managers'})
        # достаем список администраторов группы
        return result['items']
