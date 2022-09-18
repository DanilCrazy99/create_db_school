import vk_api
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
        self.getConversation = self.vk_api.messages.getConversationMembers
        self.getChatList = self.vk_api.messages.getConversations

    def get_members(self, id_chat):
        list_items = self.getConversation(peer_id=id_chat)
        list_members = []
        for a in range(len(list_items['items'])):
            list_members.append(list_items['items'][a]['member_id'])
        return list_members

    def get_chats_ids(self):
        list_items = self.getChatList()
        list_ids = []
        for a in range(len(list_items['items'])):
            if list_items['items'][a]['conversation']['peer']['type'] == 'chat':
                list_ids.append(list_items['items'][a]['conversation']['peer']['id'])
        return list_ids

    def check_is_member_chat(self, user_id):
        chat_list_this_id = []
        list_chats_id = self.get_chats_ids()
        for a in range(len(list_chats_id)):
            list_members = self.get_members(list_chats_id[a])
            if user_id in list_members:
                chat_list_this_id.append(list_chats_id[a])
        return chat_list_this_id

    # получаем название чатов. ответ в виде списка
    def title_chat(self, user_id):
        list_chat_title =[]
        for items in self.check_is_member_chat(user_id):
            title = self.vk_api.messages.getConversationsById(peer_ids=items)
            list_chat_title.append(title['items'][0]['chat_settings']['title'])
        return list_chat_title
