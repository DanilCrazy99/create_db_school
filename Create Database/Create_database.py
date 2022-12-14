import psycopg2
from Variables.Var_database import database, user, password, host, port, schoolName, schoolPass
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_school():
    try:
        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        with connection.cursor() as cursor:
            # Смотрим список баз данных
            cursor.execute(
                "SELECT datname FROM pg_database;"
            )
            # Записываем список баз данных в переменную list_database
            list_database = str(
                cursor.fetchall()
            )
            # Записываем список ролей в переменную list_roles
            cursor.execute(
                "SELECT rolname FROM pg_roles;"
            )
            list_roles = str(
                cursor.fetchall()
            )
            if schoolName in list_database:
                # Создание пользователя школы
                if schoolName not in list_roles:
                    cursor.execute(
                        "CREATE USER " + schoolName + " WITH PASSWORD '" + schoolPass + "';"
                    )
                    connection.commit()
            else:
                # Создание пользователя школы
                if schoolName not in list_roles:
                    cursor.execute(
                        "CREATE USER " + schoolName + " WITH PASSWORD '" + schoolPass + "';"
                    )
                    connection.commit()
                # Узнаю уровень изоляции и присваиваю переменной
                isolation_value = connection.isolation_level
                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                # Создание базы данных
                cursor.execute(
                    "CREATE DATABASE " + schoolName + " OWNER " + schoolName + ";"
                )
                connection.set_isolation_level(isolation_value)

            print("Создана роль и база данных школы " + schoolName)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def create_tables_in_new_db(case):
    try:
        connection = psycopg2.connect(
            database=schoolName,
            user=user,
            password=password,
            host=host,
            port=port
        )
        with connection.cursor() as cursor:
            if case == 1:
                db_main_tables(cursor)
                connection.commit()
            elif case == 2:
                db_main_tables(cursor)
                db_not_main_tables(cursor)
                connection.commit()
    except Exception as _ex:
        print("[INFO] Error while working with second stream PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO]Second Stream PostgreSQL: Tables created")


def input_case_var():
    case_var = int(input("Введите номер кейса, где\n"
                         "0 - Ничего не делать\n"
                         "1 - Создать базу данных, пользователя, и основную группу таблиц\n"
                         "2 - Создать базу данных, пользователя, и все таблицы\n"))
    info_var = program_case(case_var)
    if info_var == 0:
        return 0


def program_case(case_value):
    if case_value == 0:
        print("Не выполнять")
    elif case_value == 1:
        print("Выполняется первый кейс")
        create_database_school()
        create_tables_in_new_db(1)
    elif case_value == 2:
        print("Выполняется второй кейс")
        create_database_school()
        create_tables_in_new_db(2)
    else:
        print("Введи другое число")
        return 0


def db_main_tables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS academic_discipline(\
        id integer NOT NULL PRIMARY KEY,\
        name text NOT NULL,\
        room_id int NOT NULL DEFAULT 0\
        );"
                   )

    cursor.execute("CREATE TABLE IF NOT EXISTS add_education(\
        id integer NOT NULL,\
        name_education text NOT NULL PRIMARY KEY,\
        price money DEFAULT 0\
        );"
                   )

    cursor.execute("CREATE TABLE IF NOT EXISTS learner(\
        id integer NOT NULL PRIMARY KEY,\
        name text NOT NULL,\
        surname text,\
        phone integer\
        );"
                   )

    cursor.execute("CREATE TABLE IF NOT EXISTS role(\
        id integer NOT NULL PRIMARY KEY,\
        role text NOT NULL,\
        description text\
        );"
                   )

    cursor.execute("CREATE TABLE IF NOT EXISTS room_school(\
        id integer NOT NULL PRIMARY KEY,\
        liter_number text NOT NULL,\
        discipline_id integer DEFAULT 0\
        );"
                   )

    # Таблица student_parent/родители учеников (id, id ученика, имя, фамилия, отчество, телефон, доп информация)
    cursor.execute("CREATE TABLE IF NOT EXISTS student_parent(\
        id integer NOT NULL PRIMARY KEY, \
        learner_id integer DEFAULT 0,\
        name text NOT NULL, \
        surname text, \
        patronymic text, \
        phone integer, \
        description text\
    );"
                   )

    # Таблица teacher/учителя(id, имя, отчество, фамилия, телефон)
    cursor.execute("CREATE TABLE IF NOT EXISTS teacher(\
         id integer NOT NULL PRIMARY KEY,\
         name text NOT NULL,\
         patronymic text,\
         surname text,\
         phone integer\
         );"
                   )

    # Таблица vacation_schedule/отгулы,отпуски
    cursor.execute("CREATE TABLE IF NOT EXISTS vacation_schedule(\
        id integer NOT NULL,\
        teacher_id integer NOT NULL PRIMARY KEY,\
        start_date date,\
        stop_date date,\
        type_vacation_id integer\
        );"
                   )

    # Таблица vacation_type/тип отгулов,отпусков
    cursor.execute("CREATE TABLE IF NOT EXISTS vacation_type(\
        id integer NOT NULL PRIMARY KEY,\
        description text\
        );"
                   )


def db_not_main_tables(cursor):
    # Таблица settings(уточняется)
    cursor.execute("CREATE TABLE IF NOT EXISTS settings(\
        id integer NOT NULL PRIMARY KEY,\
        name text NOT NULL,\
        value text,\
        description text\
    );"
                   )
    # Таблица special_room(уточняется)
    cursor.execute("CREATE TABLE IF NOT EXISTS special_room(\
        id integer NOT NULL PRIMARY KEY,\
        name text NOT NULL,\
        class_room_id integer NOT NULL DEFAULT 0\
        );"
                   )
    # Таблица users
    cursor.execute("CREATE TABLE IF NOT EXISTS users(\
        id integer NOT NULL PRIMARY KEY,\
        user_id_vk integer NOT NULL,\
        role_id integer DEFAULT 1,\
        invitation_sent boolean NOT NULL DEFAULT false,\
        time_unanswered_msg integer\
        );"
                   )


while input_case_var() == 0:
    pass
