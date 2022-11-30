# -*- coding: utf-8 -*-
import vk_api
import requests
from Create_Community_VK.Config.Var_community import token_group, user_admin
from Create_Community_VK.Bot.Group.group import Group
from Create_Community_VK.Bot.db.database import DataBase
from Create_Database.Send_timetable import send_timetable


class Community:
    """
    Класс для работы с данными пользователя
    """
    def __init__(self, token_in_class=token_group):
        # присваиваю переменной token токен группы
        self.vk = vk_api.VkApi(token=token_in_class)
        # используем .vk_api() для вызова API
        self.vk_api = self.vk.get_api()
        # self.id_chat = ''
        # self.getConversation_Mem = self.vk_api.messages.getConversationMembers
        # self.getChatList = self.vk_api.messages.getConversations
        self.list_ids = []
        self.db = DataBase()
        self.group = Group()

    def get_members(self, id_chat):
        """
        Получение списка участников чата
        :param id_chat: ID чата
        :return: список участников
        """
        # list_items = self.getConversation_Mem(peer_id=id_chat)
        list_items = self.vk_api.messages.getConversationMembers(peer_id=id_chat, group_id=215601456)
        list_members = []
        for a in range(len(list_items['items'])):
            list_members.append(list_items['items'][a]['member_id'])
        return list_members

    def user_account_check(self, user_id_vk):
        """
        Проверка учета юзера в базе данных.

        :param user_id_vk:  int ID юзера в ВК
        :return: str. role user
        """
        # обновляем роль юзера в БД по данным ВК
        user_role = self.user_role_in_group(user_id=user_id_vk)
        id_role = self.db.select_id_role(role=user_role)
        self.db.insert_user(user_id=user_id_vk, role_id=id_role)
        # если роль участника группы, то invitation_sent ставим в True
        # if user_role != 'visitor':
        #     self.db.update_invitation_msg_user(user_id_vk=user_id_vk)
        return user_role

    def user_role_in_group(self, user_id):
        """
        Получение роли пользователя в группе или роль visitor

        :param user_id: int ID юзера в ВК
        :return: str название роли
        """
        result = self.group.admins_group()
        for item in result:
            if item['id'] == user_id:
                role = item['role']
                return role
        # проверить на участие в группе.
        if self.group.member_group(id_user=user_id):
            return 'user'
        # если не участник
        return 'visitor'

    def create_user(self, user_id):
        """
        Создание/сохранение данных о новом юзере

        :param user_id: int ID пользователя в ВК
        :return: int ID пользователя в БД
        """

        role_id = self.db.select_id_role(role=self.user_role_in_group(user_id=user_id))
        result = self.db.insert_user(user_id=user_id, role_id=role_id)
        # Устанавливаем статус сервера состояния =1 (новый юзер. 1-й уровень)
        self.db.insert_user_status_server(user_id_vk=user_id, status_id=1)
        return result

    def check_is_member_chat(self, user_id):
        """
        Получение ID где состоит пользователь
        :param user_id:  ID пользователя в ВК
        :return: список ID чатов
        """
        self.list_ids = self.group.get_chats_ids()
        chat_list_this_id = []
        for a in range(len(self.list_ids)):
            list_members = self.get_members(self.list_ids[a])
            if user_id in list_members:
                chat_list_this_id.append(self.list_ids[a])
        return chat_list_this_id

    def control_access_command(self, user_id_vk):
        """
        Проверка разрешения юзеру доступка к переданной команде
        :param user_id_vk:   ID пользователя в ВК
        :return: bool
        """
        return True

    def title_chat(self, user_id):
        """
        Получаем название чатов группы, где состоит пользователь.
        :param user_id: ID пользователя в ВК
        :return: Список названий чатов
        """
        list_chat_title = []
        for items in self.check_is_member_chat(user_id):
            title = self.vk_api.messages.getConversationsById(peer_ids=items)
            list_chat_title.append(title['items'][0]['chat_settings']['title'])
        return list_chat_title

    def get_user_status_server(self, id_user_vk):
        """
        Получение статуса юзера в таблице status_server
        :param id_user_vk: ID пользователя в ВК
        :return: int ID статуса из таблицы status
        """
        if not self.db.select_user_status_server(id_user_vk=id_user_vk):
            # если записи нет то создаем с id_status у которой key_stats_1 = 1
            id_status = self.db.select_status(1)
            # добавляем запись  в таблицу status_server
            self.db.insert_user_status_server(user_id_vk=id_user_vk, status_id=id_status)
        else:
            # если запись есть достаем по iD статуса значение key_stats_1
            id_status = self.db.select_user_status_server(id_user_vk=id_user_vk)[0]
        return id_status

    def set_user_status_server(self, id_user_vk, id_status):
        """
        устанавливаем статус юзера в сервере состояний
        :param id_user_vk: ID пользователя в ВК
        :param id_status: ID статуса состояний по таблице status
        """
        # создать или обновить запись в сервере состояний
        if self.db.select_user_status_server(id_user_vk=id_user_vk):
            # обновляем запись
            self.db.update_status_user(id_user_vk=id_user_vk, number_status=id_status)
        else:
            # создаём запись
            self.db.insert_user_status_server(user_id_vk=id_user_vk, status_id=id_status)

    def get_xl_file_from_msg(self, id_editor=user_admin):
        """
        Загрузка файла расписания
        :param id_editor: ID ВК загружающего пользователя
        """
        info_msg_editor = {}
        url_value = ''
        # id_msg = self.getChatList()
        id_msg = self.vk_api.messages.getConversations()
        if id_msg:
            for a in range(len(id_msg['items'])):
                if id_msg['items'][a]['conversation']['peer']['id'] == id_editor:
                    info_msg_editor = id_msg['items'][a]
                    last_id_msg = info_msg_editor['conversation']['last_conversation_message_id']
                    list_items = self.vk_api.messages.getByConversationMessageId(peer_id=id_editor,
                                                                                 conversation_message_ids=last_id_msg)
                    if len(list_items['items'][0]['attachments']) == 1:
                        attachment = list_items['items'][0]['attachments'][0]['doc']
                        if attachment['ext'] == 'xls':
                            url_value = attachment['url']
                        if url_value:
                            r = requests.get(url_value, allow_redirects=True)
                            with open("timetable.xls", 'wb') as o:
                                o.write(r.content)
                                print('файл сохранён в директории')
                            o.close()
                            # запускаем загрузку данных в БД
                            send_timetable()

