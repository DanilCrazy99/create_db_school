### academic-discipline / учебные предметы
* id bigserial NOT NULL PRIMARY KEY,
* name text NOT NULL,
* room_id int NOT NULL DEFAULT 0

### Таблица add_education / дополнительное образование (id, описание, цена)
* id bigserial NOT NULL,
* name_education text NOT NULL PRIMARY KEY,
* price money DEFAULT 0

### Таблица learner / учащийся (id, имя, фамилия, телефон)
* id bigserial NOT NULL PRIMARY KEY,
* name text NOT NULL,
* surname text,
* phone integer

### Таблица role / роль (id, название роли, расшифровка роли)
### UPD:по версии ВК могут быть админы/ редакторы/ рекламщики в нашей версии ещё должны добавиться классные руководители/ завучи/ по расписанию кто-то им всем придется разделять права.
* id bigserial NOT NULL PRIMARY KEY,
* role text NOT NULL,
* description text

### Таблица room_school / кабинеты (id, обозначение кабинета, id дисциплины закрепленной за кабинетом/возможно специализированный)
* id bigserial NOT NULL PRIMARY KEY,
* liter_number text NOT NULL,
* discipline_id integer DEFAULT 0

### Таблица settings(уточняется)
* id bigserial NOT NULL PRIMARY KEY,
* name text NOT NULL,
* value text,
* description text

### Таблица special_room(уточняется)
* id bigserial NOT NULL PRIMARY KEY,
* name text NOT NULL,
* class_room_id integer NOT NULL DEFAULT 0

### Таблица student_parent/родители учеников (id, id ученика, имя, фамилия, отчество, телефон, доп информация)
* id bigserial NOT NULL PRIMARY KEY,
* learner_id integer DEFAULT 0,
* name text NOT NULL,
* surname text,
* patronymic text,
* phone integer,
* description text

### Таблица teacher/учителя(id, имя, отчество, фамилия, телефон)
* id bigserial NOT NULL PRIMARY KEY,
* name text NOT NULL,
* patronymic text,
* surname text,
* phone integer

### Таблица vacation_schedule/отгулы,отпуски
* id bigserial NOT NULL,
* teacher_id integer NOT NULL PRIMARY KEY,
* start_date date,
* stop_date date,
* type_vacation_id integer

### Таблица vacation_type/тип отгулов,отпусков
* id bigserial NOT NULL PRIMARY KEY,
* description text

### Таблица timetable/расписание уроков
* id bigserial NOT NULL PRIMARY KEY,
* class text NOT NULL,
* lesson_number integer NOT NULL,
* academic_discipline text NOT NULL,
* day_of_week text NOT NULL,
* editor text DEFAULT 'admin',
* time_update timestamp without time zone DEFAULT CURRENT_TIMESTAMP

### Таблица bot_messages/сообщения от бота
* id bigserial NOT NULL PRIMARY KEY,
* msg text NOT NULL,
* time timestamp without time zone DEFAULT CURRENT_TIMESTAMP

### Таблица users
* id bigserial NOT NULL PRIMARY KEY,
* user_id_vk integer NOT NULL,
* role_id integer DEFAULT 1,
* invitation_sent boolean NOT NULL DEFAULT false,
* time_unanswered_msg integer
