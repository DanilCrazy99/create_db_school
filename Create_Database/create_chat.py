# -*- Coding: utf-8 -*-
# создание чатов в группе по шаблону

import vk_api
from Create_Community_VK.Config.Var_community import token_group, group_id, user_admin
from Create_Community_VK.Bot.Group.group import Group

litter_class = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З']
max_number_class = 12


def create_chat():
    """
    Создание чатов
    """
    __token = token_group
    vk = vk_api.VkApi(token=__token)
    # используем .vk_api() для вызова API
    vk_api_methode = vk.get_api()

    my_group = Group()
    list_chat = my_group.get_chats()
    print('user_admin= ', user_admin)
    print('group_id= ', group_id)
    join_user = (user_admin, 1640521)

    id_new_chat = vk_api_methode.messages.createChat(user_ids=join_user, title='test', group_id=group_id)
    id_chat = 2000000000 + id_new_chat
    link_chat = vk_api_methode.messages.getInviteLink(peer_id=id_chat, reset=0, group_id=group_id)
    print('link_chat= ', link_chat)

    for n in range(1, max_number_class+1):
        for item in litter_class:
            str_litter = str(n) + item
            # проверяем наличие уже имеющегося чата с таким названием
            for existing_chat in list_chat:
                test_letter = existing_chat[2]
                if str_litter == test_letter:
                    break
                else:
                    break


if __name__ == '__main__':
    create_chat()
