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
from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Bot.Group.group import Group
from Create_Community_VK.Config.control_word import list_week_day, control_word, list_week_words, list_month_words
from Create_Community_VK.Config.msg_default import hot_contact, help_user_chat_member, help_user_no_chat
from Create_Community_VK.Bot.keyboards.keyboard import generator_keyboard as gen_key


class MyLongPoll(VkBotLongPoll):
    """
    Переопределяем метод Listen родителя
    """
    def listen(self):
        """
        Отрабатываем разрывание соединения сервером
        """
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
        self.group = Group()
        self.community = Community()

    def send_msg(self, message, attachment: list = [], keyboard=None):
        """
        Отправка сообщения пользователю (+ вложение + клавиатура)

        :param message: str Сообщение пользователю.
        :param attachment: Список присоединенных файлов
        :param keyboard: Сформированная клавиатура в json
        """
        # print('отправка лс')
        parameters = {'message': message,
                      'keyboard': keyboard,
                      'attachment': attachment,
                      'random_id': 0}  # личное сообщение
        parameters.update({'user_id': self.from_id})
        self.vk.method('messages.send', parameters)

    def correct_msg(self, msg):
        # переводим сообщение в нижний регистр и удаляем пробелы в начале и в конце строки
        tmp_str = msg.lower().strip()
        return tmp_str

    # формируем шапку расписания. return = день недели для SQL запроса
    def date_words(self, input_week_day):
        today = datetime.today()
        result_word = []
        week_words = list_week_words
        control_week_day = list_week_day
        month_words = list_month_words

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
        data_timetable = self.db.select_time_table_activate(class_letter=class_letter[0], week_day=week_day[0])
        str_table = ''
        circle = 0
        for data_week in data_timetable:
            circle += 1
            str_table += '\n' + str(data_week[2])  # номер урока
            str_table += ' - ' + data_week[3]  # предмет
        if circle == 0:
            str_table = '\n*** нет занятий ***'

        return str_table

    def msg_help(self, user_id):
        """
        Обработка сообщения help
        """
        if self.community.check_is_member_chat(user_id=user_id):
            # если член чата, то help низкого уровня
            msg = help_user_chat_member
        else:
            # если не член чата, то help как вступить в чат
            msg = help_user_no_chat

        # отправить клавиатуру с кнопкой "назад"
        self.send_msg('Справка по работе с меню:'+msg, keyboard=gen_key(role_id=10))

    def start(self):
        """
        основной метод бота
        """
        logging.info('Запущен основной цикл бота')

        try:
            for event in self.long_poll.listen():
                # print('входное сообщение: ', event)
                # обработка поступившего личного сообщения
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.new_msg = self.correct_msg(event.obj['message']['text'])

                    # кто отправил сообщение
                    self.from_id = event.obj['message']['from_id']

                    if self.from_id < 0:
                        # прерываем если пришло сообщение от группы
                        continue

                    # проверка на участие в группе
                    if not self.group.member_group(id_user=self.from_id):
                        # Сохраняем в БД данные по пользователю.
                        user_id_db = self.community.create_user(user_id=self.from_id)

                        # проверяем флаг отправки приглашения вступить в группу
                        if not self.db.select_invitation_msg_user(user_id_db=user_id_db):
                            msg = 'Пожалуйста вступите в нашу группу.' \
                                  '\nЗарегистрируйтесь в чате своего класса.'
                            # обновляем статус отправки сообщения на True
                            self.db.update_invitation_msg_user(user_id_db=user_id_db)
                            self.send_msg(message=msg, keyboard=gen_key(0))

                        continue  # прерываем т.к. не член группы

                    # Проверить на участие в чатах. Если не участник. Передать клаву выбора действий.
                    if not self.community.check_is_member_chat(user_id=self.from_id):
                        self.send_msg(message='Выберите действие.'
                                      , keyboard=gen_key(1))
                        continue  # прерываем т.к. не член чата

                    # обработка присоединённого файла
                    if len(event.obj['message']['attachments']) != 0:
                        ext_file = event.obj['message']['attachments'][0]['doc']['ext']
                        if ext_file == 'xlsx':
                            print('поступил xlsx файл')
                            logging.info('поступил xlsx файл')
                            self.community.get_xl_file_from_msg()

                    # проверка на наличие обрабатываемого сообщения
                    if self.new_msg in control_word:

                        # отработка команды help
                        if self.new_msg == '/help':
                            self.msg_help(user_id=self.from_id)
                            continue

                        # отработка команды "важные контакты"
                        if self.new_msg == '/важные контакты':
                            self.send_msg(message=hot_contact
                                          , keyboard=gen_key(role_id=4))
                            continue

                        # отработка команды "назад"
                        if self.new_msg == '/важные контакты':
                            self.send_msg(message=hot_contact
                                          , keyboard=gen_key(role_id=4))
                            continue

                        list_chat_title =[]
                        self.community.get_xl_file_from_msg()  # проверка на право загрузки файла расписания

                        # Проверяем пользователя на участие в чатах.
                        # Если он не имеет роли в ВК и не участник чата, то заносим его в БД cтатус visitor

                        # получаем статус пользователя в сервере состояний
                        key_status = self.community.get_user_status_server(id_user_vk=self.from_id)

                        role_user = ''

                        if self.new_msg == 'расписание на ...':
                            self.send_msg('за какой день хотите узнать'
                                          ' расписание?', keyboard=gen_key(role_id=1))

                        elif self.new_msg in list_week_day:  # обработка по расписанию
                            list_chat_title = self.community.title_chat(user_id=self.from_id)
                            tmp_list_title = []
                            cicle = 0  # счетчик чатов в которых состоит пользователь
                            for item_chat_title in list_chat_title:
                                cicle += 1
                                tmp_list_title.append(item_chat_title)

                                self.date_words(self.new_msg)
                                msg_tmp = f'{self.header_timetable}\nкласс: {item_chat_title}' \
                                          f'{self.daily_lesson_schedule(class_letter=tmp_list_title, week_day=self.date_words(self.new_msg))}'

                                self.send_msg(message=msg_tmp, keyboard=self.kb.get_keyboard('clear'))
                                # очищаем список title чатов
                                tmp_list_title.clear()
                            if cicle == 0:  # если он ни где не состоит, то проверить сервер состояний и выдать клаву

                                self.send_msg(message='Для работы с ботом необходимо состоять в чате своего класса.'
                                              , keyboard=gen_key(role_id=3))  # очистка клавы
                                continue

                            self.send_msg(message='Выберете день недели.',
                                          keyboard=gen_key(role_id=4))

                        elif self.new_msg == '/меню выше':
                            # получить состояние юзера от сервера состояний
                            pass

                        else:
                            # подгрузить клавиатуру согласно сервера состояния
                            self.send_msg('Ваша команда не распознана.\nВоспользуйтесь клавиатурой.'
                                          , keyboard=self.kb.get_keyboard('main'))

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
