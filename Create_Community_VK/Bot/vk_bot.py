# -*- coding: utf-8 -*-


import vk_api.vk_api
import requests
import time
import logging
import traceback

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from Create_Community_VK.Config.token import token_group
from Create_Community_VK.Config.Var_community import group_id
from Create_Community_VK.Bot.keyboard import Keyboards
from Create_Community_VK.Bot.db.database import DataBase


class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)
                # Перехват ошибки сервера, без остановки бота
                continue


class VkBot:
    def __init__(self):
        # для longpoll
        __api_token = token_group
        __group_id = group_id

        # подключаемся к VK
        self.vk = vk_api.VkApi(token=__api_token)
        # подключение к long_poll
        self.long_poll = MyLongPoll(self.vk, __group_id)

        # для использования методов VK
        self.vk_api = self.vk.get_api()

        self.from_id = 0
        self.new_msg = ''
        self.kb = Keyboards()
        self.db = DataBase()

# Отправка сообщения пользователю (+ вложение + клавиатура)
    def send_msg(self, message, attachment: list = [], keyboard=None):
        # print('отправка лс')
        parameters = {'message': message,
                      'keyboard': keyboard,
                      'attachment': attachment,
                      'random_id': 0}  # личное сообщение
        parameters.update({'user_id': self.from_id})
        self.vk.method('messages.send', parameters)

    def correct_msg(self, msg):
        tmp_str = msg.lower()
        return tmp_str

    def create_msg_table(self, class_letter=['5А', '5Б'], week_day=['Вторник', 'Понедельник']):
        data_timetable = self.db.select_timetable_class(class_letter=class_letter, week_day=week_day)
        str_table = ''
        for data_week in data_timetable:
            str_table = '\n' + data_week[2]  # номер урока
            str_table += ' - ' + data_week[3]  # предмет
        return str_table


    def start(self):
        logging.info('Запущен основной цикл бота')

        try:
            for event in self.long_poll.listen():
                print('входное сообщение: ', event)
                # обработка поступившего личного сообщения
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.new_msg = self.correct_msg(event.obj['message']['text'])
                    # кто отправил сообщение
                    self.from_id = event.obj['message']['from_id']

                    if self.from_id < 0:
                        # прерываем если пришло сообщение от группы
                        continue

                    if self.new_msg == 'расписание на ...':
                        self.send_msg('за какой период хотите узнать'
                                      ' расписание?', keyboard=self.kb.get_keyboard('main'))
                    elif self.new_msg == '/пн':
                        tt = time.strftime('%A %d %B %Y', time.localtime())
                        self.send_msg('расписание на сегодня: '
                                      f'\n{tt}' + self.create_msg_table(),
                                      keyboard=self.kb.get_keyboard('main'))
                    elif self.new_msg == '/вт':
                        tt = time.strftime('%A %d %B %Y', time.localtime())
                        self.send_msg('расписание на завтра: '
                                      f'\n{tt}'
                                      '\n1 - ин-яз(анг)'
                                      '\n2 - литература', keyboard=self.kb.get_keyboard('main'))
                    else:
                        self.send_msg('Ваша команда не распознана.\nВоспользуйтесь'
                                      ' клавиатурой.', keyboard=self.kb.get_keyboard('main'))

        except requests.exceptions.ReadTimeout:
            error_msg = traceback.format_exc()
            logging.error(f'ошибка подключения: {error_msg}')
            time.sleep(10)

        except Exception:
            error_msg = traceback.format_exc()
            # print(f'Произошла ошибка в файле бота:\n    {error_msg}\nПерезапуск...')
            logging.info(f'источник краша...')
            logging.error(f'Произошла ошибка в файле бота:{error_msg}')
            logging.info('Перезапуск...')
            time.sleep(5)
