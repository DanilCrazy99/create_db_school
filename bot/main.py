# -*- coding: utf-8 -*-

import time
import logging
import traceback

# подключаем конфигурацию
from Variables.Var_community import path_logFile
from vk_bot import VkBot

# настройка логирования
path_log = path_logFile
logging.basicConfig(handlers=[logging.FileHandler(filename=path_log, encoding='utf-8', mode='a+')],
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%F %A %T",
                    level=logging.INFO)
logging.info('Запуск бота....')

# запускаем бесконечный цикл
while True:
    try:
        # создаем экземпляр класса
        bot = VkBot()
        # запуск
        print('Запуск бота')
        bot.start()

    except Exception:
        error_msg = traceback.format_exc()
        # print(f'Произошла ошибка в главном файле:\n    {error_msg}\nПерезапуск...')
        logging.error(f'Произошла ошибка в главном файле:{error_msg}')
        logging.info('Перезапуск...')
        time.sleep(10)
