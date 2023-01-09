# -*- coding: utf-8 -*-
from Create_Community_VK.Bot.db.database import DataBase


class Discipline:
    def __init__(self):
        self.db = DataBase()

    @ staticmethod
    def transformation(description):
        """
        Приведение дисциплины к нижнему регистру и удаление пробелов.
        :param description: Описание дисциплины
        :return: str
        """
        result = ' '.join(description.split())
        result = result.lower()
        return result

    def __insert_discipline(self, description):
        """
        Добавляем дисциплину в БД
        :param description: Описание дисциплины
        :return: ID дисциплины в БД
        """
        sql = f"INSERT INTO academic_discipline(name) VALUES ('{self.transformation(description)}') RETURNING id;"
        result = self.db.change_db(sql)  # Получаем iD дисциплины
        return result

    def select_discipline_id(self, description):
        """
        Получение ID дисциплины в БД
        :return: ID дисциплины
        """
        sql = f"SELECT id, name FROM academic_discipline WHERE name='{self.transformation(description)}';"
        result = self.db.select_db(sql=sql)
        if not result:
            return 0
        return result[0][0]

    def date(self, description):
        """
        Получение данных о дисциплине.
        :param description: Название дисциплины.
        :return: ID дисциплины или 0 если нет.
        """
        description = self.transformation(description)
        result = self.select_discipline_id(description=description)
        if result:
            # если есть данные
            return result
        # Иначе. Добавляем в БД и возвращаем ID
        result = self.__insert_discipline(description=description)
        if result:
            result = self.select_discipline_id(description=description)
            return result


if __name__ == '__main__':
    discipline = Discipline()
    print(discipline.date('  Математика     и руссКий '))
