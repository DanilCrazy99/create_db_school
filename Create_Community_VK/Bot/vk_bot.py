# -*- coding: utf-8 -*-

import vk_api.vk_api
import requests
import time
import logging
import traceback

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType  # VkBotLongPoll работа от имени группы
from Create_Community_VK.Config.token import token_group
from Create_Community_VK.Config.Var_community import group_id
from Create_Community_VK.Bot.db.database import DataBase
from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Bot.Group.group import Group
from Create_Community_VK.Config.control_word import *
from Create_Community_VK.Bot.keyboards.keyboard import controller_keyboard as control_kb


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
    """
    Класс бота
    """
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
        logging.info(f'Отправлено сообщение пользователю {self.from_id}')

    def correct_msg(self, msg):
        """
        Переводим сообщение в нижний регистр и удаляем пробелы в начале и в конце строки

        :param msg: строка
        :return: str
        """
        tmp_str = msg.lower().strip()
        return tmp_str

    def come_back(self, user_id_vk):
        """
        Отработка полученной команды назад.
        """
        # получить роль юзера
        user_role = self.community.user_role_in_group(user_id=user_id_vk)
        # получить статус состояния
        user_status = self.community.get_user_status_server(id_user_vk=user_id_vk)
        # если роль и статус не соответствуют, то выслать сообщение "начало диалога"

    def start(self):
        """
        Основной метод бота
        """
        logging.info('Запущен основной цикл бота')

        try:
            for event in self.long_poll.listen():
                print('входное сообщение: ', event)
                # кто отправил сообщение
                if 'user_id' in event.obj:
                    self.from_id = event.obj['user_id']
                elif 'from_id' in event.obj:
                    self.from_id = event.obj['from_id']

                if self.from_id < 0:
                    # прерываем если пришло сообщение от группы
                    continue

                role_user_vk = self.community.user_account_check(user_id_vk=self.from_id)

                # отработка выхода пользователя из группы
                if event.type == VkBotEventType.GROUP_LEAVE:
                    self.send_msg(message='Очень жаль что вы прощаетесь с нами.\n'
                                          'Мы уже скучаем без вас.'
                                  , keyboard=control_kb(id_user_vk=self.from_id, role_user_vk=role_user_vk))
                    # сбрасываем флаг приглашения в False
                    self.db.update_invitation_msg_user(user_id_vk=self.from_id, invitation=False)
                    self.db.update_status_user(id_user_vk=self.from_id, number_status=1)
                    continue

                # проверка на участие в группе
                if not self.group.member_group(id_user=self.from_id):
                    # проверяем флаг отправки приглашения вступить в группу
                    if not self.db.select_invitation_msg_user(user_id_vk=self.from_id):
                        msg = 'Пожалуйста вступите в нашу группу.' \
                              '\nЗарегистрируйтесь в чате своего класса.'
                        # обновляем статус отправки сообщения на True
                        self.db.update_invitation_msg_user(user_id_vk=self.from_id)
                        self.send_msg(message=msg)
                    continue  # Прерываем т.к. не член группы

                # отработка вступления пользователя в группу
                if event.type == VkBotEventType.GROUP_JOIN:
                    self.community.create_user(user_id=self.from_id)
                    # установить флаг отправки приглашения вступления в группу в True
                    self.db.update_invitation_msg_user(user_id_vk=self.from_id)
                    self.send_msg(message='Добро пожаловать в нашу группу.'
                                  , keyboard=control_kb(id_user_vk=self.from_id, role_user_vk=role_user_vk))
                    continue

                # обработка поступившего личного сообщения
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.new_msg = self.correct_msg(event.obj['text'])

                    # обработка присоединённого файла
                    if len(event.obj['attachments']) != 0:
                        ext_file = event.obj['attachments'][0]['doc']['ext']
                        if ext_file == 'xlsx':
                            print('поступил xlsx файл')
                            logging.info('поступил xlsx файл')
                            self.community.get_xl_file_from_msg()
                            self.send_msg('Файл добавлен в таблицу учета расписаний.')
                            continue

                    # проверка допустимости команды
                    if not (self.new_msg in control_word):
                        print('Прерывание выполнения.\nПоступила не распознанная команда')
                        logging.info(f'Поступила не распознанная команда={self.new_msg}. User_id_vk={self.from_id}')
                        continue

                    # отправляем на обработку команду
                    answer_msg, keyboard = control_kb(id_user_vk=self.from_id
                                                      , role_user_vk=role_user_vk
                                                      , key_command=self.new_msg)
                    self.send_msg(message=answer_msg, keyboard=keyboard)

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
