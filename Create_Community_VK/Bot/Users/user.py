import vk_api
from Create_Community_VK.Config.Var_community import token_group
from Create_Community_VK.Config.token import token


class Community:
    def __init__(self, token_in_class=token):
        # присваиваю переменной token токен группы
        # по дефолту равно токену из конфига
        self.__token = token_in_class
        self.vk = vk_api.VkApi(token=self.__token)
        # используем .vk_api() для вызова API
        self.vk_api = self.vk.get_api()
        # self.id_chat = ''
        self.getConversation = self.vk_api.messages.getConversationMembers

    def get_members(self, id_chat):
        list_items = self.getConversation(peer_id=id_chat)
        list_members = []
        for a in range(len(list_items['items'])):
            list_members.append(list_items['items'][a]['member_id'])
        return list_members


test1 = Community()
print(test1.get_members(2000000001))  # В скобки ввести id беседы
