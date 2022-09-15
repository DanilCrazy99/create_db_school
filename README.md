# create_db_school
Для работы с файлом Create Database/Create_database.py необходимо установить библиотеку psycopg2

    pip install psycopg2-binary

и ввести все переменные в файле Variables/Var_database:
	
* database = "postgres" 
* user = "" #имя пользователя кто будет создавать базу данных, пользователя, таблицы
* password = "" #пароль пользователя-создателя таблицы
* host = "" #local_host если запускать из директории сервера
* port = 5432
* schoolName = "" #это будет имя пользователя и базы данных
* schoolPass = "" #пароль созданного пользователя 

Этот скрипт создаёт базу данных, пользователя(вместе с паролем), и таблицы с содержимым описанным в файле tables_school.md

Для работы с файлом vk_create_group.py необходима установка библиотеки vk-api:
	
	python3 -m pip install vk_api

После установки нужно ввести все переменные в файле Variables/Var_community.py

* vk_token  #токен пользователя от чьего имени будет создаваться сообщество

Для работы с файлом Send_timetable нужна библиотека openpylx

	pip install openpyxl
	
