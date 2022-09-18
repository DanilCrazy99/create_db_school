# -*- coding: utf-8 -*-


import vk_api.vk_api
import requests
import time
import logging
import traceback

from datetime import datetime, timedelta
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
                # print(e)
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
        self.header_timetable = ''
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

    # формируем шапку расписания. return = день недели для SQL запроса
    def date_words(self, input_week_day):
        today = datetime.today()
        result_word = []
        week_words = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        control_week_day = ['/пн', '/вт', '/ср', '/чт', '/пт', '/сб', '/вс']
        month_words = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                       'октября', 'ноября', 'декабря']

        number_week_day = datetime.weekday(today)
        index_input_week_day = control_week_day.index(input_week_day)
        index_week_today = datetime.weekday(today)
        len_list_week = len(control_week_day)

        # вычисляем дельту между сегодня и запрашиваемым днём
        if index_input_week_day != index_week_today:
            if index_week_today < index_input_week_day:
                delta_day = index_input_week_day - index_week_today
            else:
                delta_day = len_list_week - index_week_today + index_input_week_day
        else:
            delta_day = 0

        tomorrow = today + timedelta(days=delta_day)
        tomorrow_week_day = datetime.weekday(tomorrow)

        # склонение дня недели
        if index_input_week_day in [2, 4, 5]:
            day_week = week_words[tomorrow_week_day][:-1] + 'у'
        else:
            day_week = week_words[tomorrow_week_day]
        number_month = int(tomorrow.strftime('%m'))

       # формируем шапку расписания на день
        self.header_timetable = f'на {day_week}, {tomorrow.strftime("%d")} ' \
                                f'{month_words[number_month]} ' \
                                f'{tomorrow.strftime("%Y")}г'
        # print('header_timetable= ', self.header_timetable)

        result_word.append(week_words[tomorrow_week_day].capitalize())
        return result_word

    # получение расписания на один день
    def daily_lesson_schedule(self, class_letter=['5Б'], week_day=['Вторник']):
        data_timetable = self.db.select_timetable_class(class_letter=class_letter, week_day=week_day)
        str_table = ''
        circle = 0
        for data_week in data_timetable:
            circle += 1
            str_table += '\n' + str(data_week[2])  # номер урока
            str_table += ' - ' + data_week[3]  # предмет
        if circle == 0:
            str_table = '\n*** нет занятий ***'

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
                        self.send_msg('за какой день хотите узнать'
                                      ' расписание?', keyboard=self.kb.get_keyboard('main'))
                    elif self.new_msg in ['/пн', '/вт', '/ср', '/чт', '/пт', '/сб', '/вс']:
                        self.date_words(self.new_msg)
                        msg_tmp = f'{self.header_timetable} ' \
                                  f'{self.daily_lesson_schedule(class_letter=["5А"], week_day=self.date_words(self.new_msg))}'

                        self.send_msg(message=msg_tmp, keyboard=self.kb.get_keyboard('main'))
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
