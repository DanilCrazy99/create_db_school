# -*- coding: utf-8 -*-

from Create_Community_VK.Bot.db.database import DataBase
from Create_Community_VK.Bot.Group.group import Group

if __name__ == '__main__':
    db = DataBase()
    gr = Group()
    result = gr.grouping_chats_level()
    print(result)
