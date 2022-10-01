import vk_api
import requests
from Create_Community_VK.Config.Var_community import token_group
from Create_Community_VK.Bot.Group.group import Group
from Create_Community_VK.Bot.db.database import DataBase


class Community:
    """
    Класс для работы с данными пользователя
    """
    def __init__(self, token_in_class=token_group):
        # присваиваю переменной token токен группы
        self.__token = token_in_class
        self.vk = vk_api.VkApi(token=self.__token)
        # используем .vk_api() для вызова API
        self.vk_api = self.vk.get_api()
        # self.id_chat = ''
        self.getConversation_Mem = self.vk_api.messages.getConversationMembers  #
        self.getChatList = self.vk_api.messages.getConversations
        self.list_ids = []
        self.db = DataBase()
        self.group = Group()

    def get_members(self, id_chat):
        """
        Получение списка участников чата
        :param id_chat: ID чата
        :return: список участников
        """
        list_items = self.getConversation_Mem(peer_id=id_chat)
        list_members = []
        for a in range(len(list_items['items'])):
            list_members.append(list_items['items'][a]['member_id'])
        return list_members

    def age_indicated(self, user_id):
        """
        Получить возраст пользователя
        :param user_id: ID пользователя в ВК
        :return:
        """
        info = self.vk_api.users.get(user_ids=user_id, fields='bdate')
        print('info =', info)
        pass

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
        Получение статуса юзера
        :param id_user_vk: ID пользователя в ВК
        :return: int номер статуса
        """
        if not self.db.select_user_status_server(user_id=id_user_vk):
            # если записи нет то создаем с id_status у которой key_status_1 = 1
            id_status = self.db.select_status(1)
            # добавляем запись  в таблицу status_server
            self.db.insert_user_status_server(user_id_vk=id_user_vk, status_id=id_status)
            return id_status
        # если запись есть достаем по iD статуса значение key_stats_1
        status_id = self.db.select_user_status_server(user_id=id_user_vk)
        result = self.db.select_key_stats_1(status_id=status_id)
        return result

    def get_xl_file_from_msg(self, id_editor=1640521):
        """
        Загрузка файла расписания
        :param id_editor: ID загружающего пользователя
        :return:
        """
        info_msg_editor = {}
        url_value = ''
        id_msg = self.getChatList()
        if id_msg:
            for a in range(len(id_msg['items'])):
                if id_msg['items'][a]['conversation']['peer']['id'] == id_editor:
                    info_msg_editor = id_msg['items'][a]
            last_id_msg = info_msg_editor['conversation']['last_conversation_message_id']
            get_info_about_msg = self.vk_api.messages.getByConversationMessageId
            list_items = get_info_about_msg(peer_id=id_editor, conversation_message_ids=last_id_msg)
            if len(list_items['items'][0]['attachments']) == 1:
                attachment = list_items['items'][0]['attachments'][0]['doc']
                if attachment['ext'] == 'xlsx':
                    url_value = attachment['url']
                if url_value:
                    r = requests.get(url_value, allow_redirects=True)
                    with open('timetable.xlsx', 'wb') as o:
                        o.write(r.content)

