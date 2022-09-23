import openpyxl


def create_timetable_list(path):
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    # print(sheet[1][0].value)   A1    ABCDEFGHI  INDEX[ЦИФРА][БУКВА]
    # print(sheet[3][4].value)   E3    123456789
    list_class = []
    list_lessons = [[]]

    for columns_name_class in range(3, sheet.max_column):  # Получаю список классов при помощи прохода по 3-й строке
        if sheet[3][columns_name_class].value:
            list_class.append(sheet[3][columns_name_class].value)
    for columns in range(3, sheet.max_column):  # переборка по координате "буква"
        for rows in range(3, 52):  # переборка по координате "цифра"
            day_week_val = int(rows / 8)
            day_week = sheet[4 + day_week_val * 8][0].value
            if sheet[rows][columns].value:  # Если выбранная ячейка содержит данные
                if sheet[rows][columns].value in list_class:  # Значение ячейки есть в списке с классами
                    name_class = sheet[rows][columns].value

                    for i in range(7):  # Записываем 7 строк под ним
                        incr = len(list_lessons)-1
                        if sheet[rows + i + 1][columns].value is None:  # Убираю значения None из списков
                            pass
                        else:
                            lesson_cell_coordinate_number = rows + i + 1
                            list_lessons[incr].append(name_class)
                            list_lessons[incr].append(str(sheet[lesson_cell_coordinate_number][1].value)[0])
                            list_lessons[incr].append(sheet[rows + i + 1][columns].value)
                            list_lessons[incr].append(day_week)
                        list_lessons.append([])
    return list_lessons


def create_postgres_list(list_func):
    completed_list = []
    for a in range(len(list_func)):
        if len(list_func[a]) != 0:
            completed_list.append(list_func[a])
    return completed_list
