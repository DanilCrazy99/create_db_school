# -*- coding: utf-8 -*-

import time
import logging
import traceback

# подключаем конфигурацию
from Create_Community_VK.Config.Var_community import path_logFile
from Create_Community_VK.Bot.vk_bot import VkBot
from Create_Community_VK.Bot.db.database import DataBase

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
# db.insert_chat()  # раскомментировать после тестов

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
