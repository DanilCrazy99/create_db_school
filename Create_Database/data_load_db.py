# -*- coding utf-8 -*-

import psycopg2
from Config.Var_database import main_database, user, password, host, port

list_data = (["начало диалога", 1], ["потоки младших классов", 2], ["выбор ссылки на чат класса", 3],
             ["получение расписания", 4], ["потоки старших классов", 21])


def load_data():
    try:
        connection = psycopg2.connect(
            database=main_database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        with connection.cursor() as cursor:
            for item in list_data:
                cursor.execute("INSERT INTO "
                               "status(status_member, key_stats_1) "
                               f"VALUES ({item[0]}, {item[1]});")
                connection.commit()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def test():
    for item in list_data:
        print(f'data1= {item[0]}, data2= {item[1]}')


if __name__ == '__main__':
    load_data()
