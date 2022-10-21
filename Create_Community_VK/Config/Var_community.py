# -*- coding: utf-8 -*-

from pathlib2 import Path

from Create_Community_VK.Config.token import token_admin, token_group

user_admin = 1640521
group_id = 215601456
vk_token = token_admin
token_group = token_group
path_home = Path.cwd()
path_logFile = "log.log"

path_timetableFile = Path(path_home, "file", "timetable.xlsx")
# последний класс начальной школы
LEVEL_PRIMARY = 4

# Переменные для создания сообщества
title = 'Опять программирую'
description = 'Группа для того чтобы написать базу данных школ'
type_community = 'group'
