# -*- coding: utf-8 -*-

import openpyxl

tmp_path = 'timetable.xlsx'


def create_timetable_list(path=tmp_path):
    """
    Чтение файла xlsx
    :param path: Путь к файлу
    :return:
    """
    wb = openpyxl.load_workbook(path, data_only=True)
    # получить имена страниц с расписаниями. Название листа содержит сочетание "-параллель"
    all_name_sheet = wb.get_sheet_names()
    str_find = '-параллель'
    # максимальное кол-во уроков в день
    count_lesson_day = 15
    list_class = []
    list_lessons = [[]]
    for item in all_name_sheet:
        if item.find(str_find) > 0:
            sheet = wb.get_sheet_by_name(item)
            # sheet = wb.active
            # print(sheet[1][0].value)   A1    ABCDEFGHI  INDEX[ЦИФРА][БУКВА]
            # print(sheet[3][4].value)   E3    123456789
            # info_editor = sheet[2][1].value   Информация: Ответственный и дата
            lesson_cell_coordinate_number = 3
            date_time = sheet[2][5].value
            for columns_name_class in range(3, sheet.max_column):  # Получаю список классов при помощи прохода по 3-й строке
                if sheet[3][columns_name_class].value:
                    list_class.append(sheet[3][columns_name_class].value)
            for columns in range(3, sheet.max_column):  # переборка по координате "буква"
                for rows in range(3, (7*count_lesson_day)):  # переборка по координате "цифра"
                    # if sheet[rows][1].value == 'урок':
                    #     continue  # прерываем цикл при натыкании на столбец 'урок'

                    if sheet[rows][columns].value:  # Если выбранная ячейка содержит данные
                        if sheet[rows][columns].value in list_class:  # Значение ячейки есть в списке с классами
                            name_class = sheet[rows][columns].value

                            for i in range(count_lesson_day):  # Записываем count_lesson_day строк под ним
                                incr = len(list_lessons) - 1
                                if sheet[rows + i + 1][columns].value is None:  # Убираю значения None из списков
                                    pass
                                else:
                                    lesson_cell_coordinate_number = rows + i + 1
                                    if sheet[lesson_cell_coordinate_number][1].value == 'урок':
                                        break  # прерываем цикл при натыкании на столбец 'урок'
                                    list_lessons[incr].append(name_class)
                                    list_lessons[incr].append(str(sheet[lesson_cell_coordinate_number][1].value))
                                    list_lessons[incr].append(sheet[lesson_cell_coordinate_number][columns].value)
                                    list_lessons[incr].append(sheet[rows+1][0].value)
                                list_lessons.append([])
    return list_lessons, date_time


def create_postgres_list(list_func):
    completed_list = []
    for a in range(len(list_func)):
        if len(list_func[a]) != 0:
            completed_list.append(list_func[a])
    return completed_list

if __name__ == '__main__':
    create_timetable_list()
