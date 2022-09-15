import psycopg2
import Create_timetable
from Variables.Var_database import schoolName, user, password, host, port, path_timetable
try:
    connection = psycopg2.connect(
        database=schoolName,
        user=user,
        password=password,
        host=host,
        port=port
        )
    completed_list = Create_timetable.create_postgres_list(Create_timetable.create_timetable_list(path_timetable))
    for a in range(len(completed_list)):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO timetable (class, "
                           "lesson_number, "
                           "academic_discipline, "
                           "day_of_week, "
                           "editor) "
                          f"VALUES ({completed_list[a]})"
                            )

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
