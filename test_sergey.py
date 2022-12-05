# -*- coding: utf-8 -*-

from Create_Community_VK.Bot.db.database import DataBase
from Create_Community_VK.Bot.Group.group import Group
from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Bot.Chat.chat import Chat
from Create_Community_VK.Bot.keyboards.keyboard import *

if __name__ == '__main__':
    db = DataBase()
    gr = Group()
    user = Community()
    chat = Chat()
    user_id_vk = 696195563
    # result_user = user.chat_id_from_user_db(user_id_vk=user_id_vk)
    # result_chat = chat.litter_level_chat(level=1)
    # print(result_user, result_chat)

    # получаем края ID актуального расписания
    result = db.current_schedule(selected_day='03/12/2022')
    print('current_schedule= ', result)
    # получаем расписание на один день
    res = db.editor_time_table_db()
    print('editors= ', res)
