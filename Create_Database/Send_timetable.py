
import psycopg2

from datetime import datetime
from Create_Database.Config.Var_database import schoolName, user, password, host, port
from Create_Community_VK.Config.Var_community import user_admin
from Create_Database.Create_timetable import *


def send_timetable(editor_id_vk=user_admin):
    """
    Загрузка таблицы расписания в БД
    :param editor_id_vk: id пользователя который прислал изменения(завуч, директор, админ)
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
        completed_list, date_time = create_timetable_list()
        completed_list = create_postgres_list(completed_list)
        send_trigger = False
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
            if date_time is None:
                date_time = datetime.today()
            cursor.execute("INSERT INTO timetable_time_activate ("
                           "time_activate, "
                           "editor_user_id, "
                           "class_flow, "
                           "id_timetable) "
                           f"VALUES ('{date_time}', '{str(editor_id_vk)}', '{str(completed_list[0][0][:-1])}', {id_first_timetable})"
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
