# -*- coding: utf-8 -*-


import vk_api.vk_api
import requests
import time
import logging
import traceback

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                # перехват ошибки сервера. без остановки бота
                continue


class VkBot:
    def __init__(self):
        pass

    def start(self):
        logging.info('Запущен основной цикл бота')
