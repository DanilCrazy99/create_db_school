# -*- coding: utf-8 -*-

import sys
import os

import time
import logging
import traceback

sys.path.insert(1, os.path.join(sys.path[0], 'Create_Community_VK'))

# подключаем конфигурацию
from Config.Var_community import path_logFile
from Bot.vk_bot import VkBot
from Bot.db.database import DataBase

# настройка логирования
path_log = path_logFile
logging.basicConfig(handlers=[logging.FileHandler(filename=path_log, encoding='utf-8', mode='a+')],
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%F %A %T",
                    level=logging.INFO)
logging.info('Запуск бота....')

# Закидываем данные о существующих чатах в БД
print('загрузка данных по чатам')
logging.info('Загрузка данных по чатам группы.')
db = DataBase()
db.insert_chat()

# запускаем бесконечный цикл
while True:
    try:
        # создаем экземпляр класса
        print('Запуск бота')
        logging.info('Запуск бота.')
        bot = VkBot()
        # запуск
        bot.start()

    except Exception:
        error_msg = traceback.format_exc()
        # print(f'Произошла ошибка в главном файле:\n    {error_msg}\nПерезапуск...')
        logging.error(f'Произошла ошибка в главном файле:{error_msg}')
        logging.info('Перезапуск...')
        time.sleep(10)
