import psycopg2
import Create_timetable
from Create_Database.Config.Var_database import schoolName, user, password, host, port, path_timetable


def send_timetable():
    """
    Загрузка таблицы расписания в БД
    """
    connection = psycopg2.connect(
        database=schoolName,
        user=user,
        password=password,
        host=host,
        port=port
        )

    try:
        completed_list = Create_timetable.create_postgres_list(Create_timetable.create_timetable_list(path_timetable))
        for a in range(len(completed_list)):
            without_brackets = str(completed_list[a])
            without_brackets = without_brackets[:len(without_brackets)-1]
            without_brackets = without_brackets[1:]
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO timetable (class, "
                               "lesson_number, "
                               "academic_discipline, "
                               "day_of_week, "
                               "editor) "
                               f"VALUES ({without_brackets})"
                               )
        connection.commit()
    except Exception as _ex:
        print("[INFO] Error while working with PostgresQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgresQL connection closed")


if __name__ == '__main__':
    send_timetable()
