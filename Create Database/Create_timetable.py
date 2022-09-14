import openpyxl
from Variables.Var_database import path_timetable
wb = openpyxl.load_workbook(path_timetable)
sheet = wb.active
# print(sheet[1][0].value)  # A1      ABCDEFGHI  INDEX[ЦИФРА][БУКВА]
# print(sheet[3][4].value)  # E3      123456789
list_class = {'class': [], 'lessons': []}
list_lessons = []

for columns1 in range(3, sheet.max_column):
    if sheet[3][columns1].value:
        list_class['class'].append(sheet[3][columns1].value)

for columns in range(3, sheet.max_column):
    for rows in range(3, 52):
        # print(sheet[rows][columns].value)
        if sheet[rows][columns].value:
            for a in (list_class['class']):
                if a in sheet[rows][columns].value:
                    for i in range(7):
                        if sheet[rows + i + 1][columns].value is None:
                            list_lessons.append('_')
                        else:
                            list_lessons.append(sheet[rows + i + 1][columns].value)
                        if i == 6:
                            list_lessons.append('_')

                    list_class['lessons'].append(list_lessons)
                    list_lessons = []
for i in range(6):
    print(list_class['lessons'][i])


def create_postgres_list():

    completed_list = [
        [1, 2, 3, 4, 5, 6]]  # класс, урок(время), предмет, день недели, время(актуализации), ответственный
    return completed_list


print(create_postgres_list())
print(list_class)
# for i in list_class['class']:
#     if i == '5Б':
#         print(list_class['class'].index(i))
