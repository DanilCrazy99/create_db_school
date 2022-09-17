import vk_api.vk_api

from Create_Community_VK.Config.Var_community import token_group


class User:
    def __init__(self, from_id=0):
        self.__from_id = from_id
        # подключаемся к VK
        self.vk = vk_api.VkApi(token=self.__api_token)
        # для использования методов VK
        self.vk_api = self.vk.get_api()

    def set_user_id(self, user_id):
        self.__from_id = user_id
        return self.__from_id



