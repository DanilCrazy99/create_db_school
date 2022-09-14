import openpyxl
from Variables.Var_database import path_timetable

wb = openpyxl.load_workbook(path_timetable)
sheet = wb.active
# print(sheet[1][0].value)   A1    ABCDEFGHI  INDEX[ЦИФРА][БУКВА]
# print(sheet[3][4].value)   E3    123456789
list_class = []
list_lessons = []

for columns_name_class in range(3, sheet.max_column):  # Получаю список классов при помощи прохода по 3-й строке
    if sheet[3][columns_name_class].value:
        list_class.append(sheet[3][columns_name_class].value)

for columns in range(3, sheet.max_column):  # переборка по координате "буква"
    for rows in range(3, 52):  # переборка по координате "цифра"
        if sheet[rows][columns].value:  # Если выбранная ячейка содержит данные
            for a in list_class:  # Переборка классов из листа list_class
                if a in sheet[rows][columns].value:  # Если класс встретился при переборе таблицы
                    name_class = a
                    for i in range(7):  # Записываем 7 строк под ним
                        if sheet[rows + i + 1][columns].value is None:  # Убираю значения None из списков
                            list_lessons.append(f'{name_class}._')
                        else:
                            list_lessons.append(name_class + '.' + str(sheet[rows + i + 1][1].value)[0] + '.' + sheet[rows + i + 1][columns].value)
                        if i == 6:
                            list_lessons.append(f'{name_class}._')

print(list_class)
print(list_lessons)


def create_postgres_list():
    completed_list = [
        [1, 2, 3, 4, 5, 6]]  # класс, урок(время), предмет, день недели, время(актуализации), ответственный
    return completed_list  # Должно вернуть список который можно будет вставить в функцию INSERT

# for i in list_class['class']:
#     if i == '5Б':
#         print(list_class['class'].index(i))
