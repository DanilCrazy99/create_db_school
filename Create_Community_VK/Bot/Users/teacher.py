# -*- coding: utf-8 -*-
# модуль по работе с данными учителя и для учителя

from Create_Community_VK.Bot.db.database import DataBase


# ФИО учителя

# список предметов учителя
class Teacher:
    def __init__(self, id_user):
        """
        Конструктор класса Teacher
        :param id_user: ID юзера в БД бота
        """
        self.id_user = id_user
        self.db = DataBase()

    def data_teacher(self):
        sql = "SELECT id, name, patronymic, surname, phone, user_id, id_list_discipline	" \
              f"FROM teacher WHERE user_id = {self.id_user};"
        list_teacher = self.db.select_db(sql=sql)
        if not list_teacher:
            list_teacher = []

        return list_teacher





if __name__ == '__main__':
    print('test')
