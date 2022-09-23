import psycopg2
import Create_timetable
from Create_Database.Config.Var_database import schoolName, user, password, host, port, path_timetable


def send_timetable(editor_id_vk='740705763'):
    """
    Загрузка таблицы расписания в БД
    :param editor_id_vk: id пользователя который прислал изменения(завуч, директор, админ)
    :return id_first_timetable: id первой строки в момент заливки расписания
    """

    try:
        connection = psycopg2.connect(
            database=schoolName,
            user=user,
            password=password,
            host=host,
            port=port
            )
        a = Create_timetable.create_timetable_list(path_timetable)
        completed_list, date_time = Create_timetable.create_postgres_list(a)
        send_trigger = False
        id_first_timetable = None   # id первой строки в момент заливки расписания
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
                    id_first_timetable = cursor.fetchall()
                    id_first_timetable = id_first_timetable[2:-3]
                    print(id_first_timetable)
                else:
                    cursor.execute("INSERT INTO timetable (class, "
                                   "lesson_number, "
                                   "academic_discipline, "
                                   "day_of_week) "
                                   f"VALUES ({without_brackets}) "
                                   )
        connection.commit()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO timetable_time_activate ("
                           "time_activate, "
                           "editor_user_id, "
                           "id_timetable) "
                           f"VALUES ('{date_time}', '{editor_id_vk}', {id_first_timetable})"
                           )
    except Exception as _ex:
        print("[INFO] Error while working with PostgresQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgresQL connection closed")
    return id_first_timetable


if __name__ == '__main__':
    send_timetable()
