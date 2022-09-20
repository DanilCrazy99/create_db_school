import vk_api
import requests
from Create_Community_VK.Config.Var_community import token_group


class Community:
    def __init__(self, token_in_class=token_group):
        # присваиваю переменной token токен группы
        # по дефолту равно токену из конфига
        self.__token = token_in_class
        self.vk = vk_api.VkApi(token=self.__token)
        # используем .vk_api() для вызова API
        self.vk_api = self.vk.get_api()
        # self.id_chat = ''
        self.getConversation_Mem = self.vk_api.messages.getConversationMembers  #
        self.getChatList = self.vk_api.messages.getConversations

        def get_chats_ids():  # Получаю на выходе список id чатов группы
            list_items = self.getChatList()
            list_ids = []
            for a in range(len(list_items['items'])):
                if list_items['items'][a]['conversation']['peer']['type'] == 'chat':
                    list_ids.append(list_items['items'][a]['conversation']['peer']['id'])
            return list_ids
        self.list_ids = get_chats_ids()

    def get_members(self, id_chat):  # Получаю на вход id чата в котором нужно узнать участников
        list_items = self.getConversation_Mem(peer_id=id_chat)
        list_members = []
        for a in range(len(list_items['items'])):
            list_members.append(list_items['items'][a]['member_id'])
        return list_members  # Получаю на выходе список id участников этого чата

    # Получаем возраст пользователя. API с токеном пользователя
    def age_indicated(self, user_id):
        info = self.vk_api.account.getProfileInfo()
        print('info =', info)
        pass

    def check_is_member_chat(self, user_id):  # Получаю на вход id пользователя которого необходимо проверить
        chat_list_this_id = []
        for a in range(len(self.list_ids)):
            list_members = self.get_members(self.list_ids[a])
            if user_id in list_members:
                chat_list_this_id.append(self.list_ids[a])
        return chat_list_this_id  # На выход получаю id чатов в которых состоит участник

    # Получаем название чатов. Ответ в виде списка
    def title_chat(self, user_id):
        list_chat_title = []
        for items in self.check_is_member_chat(user_id):
            title = self.vk_api.messages.getConversationsById(peer_ids=items)
            list_chat_title.append(title['items'][0]['chat_settings']['title'])
        return list_chat_title

    def get_xl_file_from_msg(self, id_editor=1640521):
        def give_file_from_url(url):
            r = requests.get(url, allow_redirects=True)
            with open('timetable.xlsx', 'wb') as o:
                o.write(r.content)

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
                    give_file_from_url(url_value)

