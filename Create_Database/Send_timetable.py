
import psycopg2

from datetime import datetime
from Create_Database.Config.Var_database import schoolName, user, password, host, port


def create_postgres_list(list_func):
    completed_list = []
    for a in range(len(list_func)):
        if len(list_func[a]) != 0:
            completed_list.append(list_func[a])
    return completed_list


def send_timetable(editor_id_vk, timetable_list, data_sheet=None):
    """
    Загрузка листа расписания в БД
    :param editor_id_vk: id пользователя который прислал изменения(завуч, директор, админ)
    :param timetable_list: данные листа расписания
    :param data_sheet: Дата актуализации расписания на листе
    :return id_first_timetable: id первой строки в момент заливки расписания
    """
    id_first_timetable = None  # id первой строки в момент заливки расписания
    try:
        connection = psycopg2.connect(
            database=schoolName,
            user=user,
            password=password,
            host=host,
            port=port
            )
        completed_list = timetable_list  # загружаем в переменные полученный файл Excel
        completed_list = create_postgres_list(completed_list)
        send_trigger = False
        if not completed_list:
            return False
        for a in range(len(completed_list)):
            without_brackets = str(completed_list[a])
            without_brackets = without_brackets[:len(without_brackets)-1]
            without_brackets = without_brackets[1:]
            with connection.cursor() as cursor:
                if not send_trigger:
                    send_trigger = True
                    cursor.execute("INSERT INTO timetable (class, "
                                   "lesson_number, "
                                   "academic_discipline, "
                                   "day_of_week) "
                                   f"VALUES ({without_brackets}) "
                                   "RETURNING id"
                                   )
                    id_first_timetable = str(cursor.fetchall())
                    id_first_timetable = id_first_timetable[2:-3]
                else:
                    cursor.execute("INSERT INTO timetable (class, "
                                   "lesson_number, "
                                   "academic_discipline, "
                                   "day_of_week) "
                                   f"VALUES ({without_brackets}) "
                                   )
        with connection.cursor() as cursor:
            if data_sheet is None:
                data_sheet = datetime.today()
            cursor.execute("INSERT INTO timetable_time_activate ("
                           "time_activate, "
                           "editor_user_id, "
                           "class_flow, "
                           "id_timetable) "
                           f"VALUES ('{data_sheet}', '{str(editor_id_vk)}', '{str(completed_list[0][0][:-1])}', {id_first_timetable})"
                           )
            connection.commit()
    except Exception as _ex:
        print("[INFO] Error while working with PostgresQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgresQL connection closed")
    return id_first_timetable


if __name__ == '__main__':
    send_timetable()
