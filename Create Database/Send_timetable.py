import psycopg2
import Create_timetable
from Variables.Var_database import database, user, password, host, port
try:
    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
        )

    for a in range(len(list)):
        with connection.cursor() as cursor:
            cursor.execute(
                            "INSERT INTO таблица_с_расписанием (класс, урок(время), предмет, день недели, "
                            f"ответственный) VALUES ({массив})"
                            )

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
