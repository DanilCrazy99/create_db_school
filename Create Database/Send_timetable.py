import psycopg2
from Variables.Var_database import database, user, password, host, port, schoolName, schoolPass

try:
    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    with connection.cursor() as cursor:
        cursor.execute(
                        "INSERT INTO таблица_с_расписанием (id, класс, урок(время), предмет, день недели, "
                        f"время(актуализации), ответственный) VALUES ({массив})"
                        )

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
