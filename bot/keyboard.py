# -*- coding: utf-8 -*-
#файл клавиатур

class Keyboards:
    def __init__(self):
        self.default_path = 'main'

    def get_keyboard(self, path):
        with open(f'keyboards/{path}.json', 'r', encoding="UTF-8") as kb:
            return kb.read()
