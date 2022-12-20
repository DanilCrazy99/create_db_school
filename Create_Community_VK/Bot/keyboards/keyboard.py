# -*- coding: utf-8 -*-
# файл генерации клавиатур
import time

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Bot.Group.group import Group
from Create_Community_VK.Bot.db.database import DataBase
from Create_Community_VK.Bot.Chat.chat import Chat
from Create_Community_VK.Config.msg_default import hot_contact, help_user_no_chat, help_user_chat_member
from Create_Community_VK.Config.control_word import list_class, list_week_day, list_week_words, list_month_words
from datetime import datetime, timedelta, date

gr = Group()  # экземпляр класса Group
db = DataBase()
user = Community()
chat = Chat()


def controller_keyboard(id_user_vk, role_user_vk, key_command=None):
    """
    Контроллер клавиатуры
    :param id_user_vk: ID пользователя в ВК
    :param role_user_vk: str Роль пользователя в ВК
    :param key_command: полученная команда из сообщения
    :return:
    """

    # получаем данные с сервера состояний юзера
    if db.select_user_status_server(id_user_vk=id_user_vk):
        key_set = db.select_user_status_server(id_user_vk=id_user_vk)[2]
    else:
        key_set = 1
        status_id = db.select_status(key_stat=key_set)
        db.insert_user_status_server(user_id_vk=id_user_vk, status_id=status_id)

    result_msg = ''
    inline_keyboard = False
    flow_class = 0
    if role_user_vk == 'visitor':
        result_keyboard = generator_keyboard(set_keyboard=0)
        result_msg = 'Вступите в нашу группу.'
    else:
        # Проверяем доступ юзера к полученной команде.
        if user.control_access_command(user_id_vk=id_user_vk):
            if key_command == '/help':
                if key_set < 2:
                    result_msg = help_user_no_chat
                else:
                    result_msg = help_user_chat_member

            elif key_command == '/начальные классы':
                result_msg = 'Выберите поток в начальных классах:'
                key_set = 2  # номер клавиатуры для команды "Начальные классы"
                # Обновляем в БД статус на выбор потока
                user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=2))

            elif key_command == '/старшие классы':
                result_msg = 'Выберите поток в старших классах:'
                key_set = 21  # номер клавиатуры для команды "Старшие классы"
                # Обновляем в БД статус на выбор потока
                user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=21))

            elif key_command in list_class:
                flow_class = int(key_command[1:])
                # формируем клавиатуру ссылок внутри параллели
                result_msg = 'Выберите чат своего класса.'
                key_set = 3
                # Обновляем в БД статус на выбор потока
                user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=3))

            elif key_command == '/важные контакты':
                result_msg = hot_contact
                # key_set в этом случае не меняется

            elif key_command == '/назад':
                # проверяем из какой клавиатуры вызвана команда "/назад"
                if key_set == 2 or key_set == 21:
                    # Обновляем в БД статус на выбор потока
                    key_set = 1
                    user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=key_set))
                    result_msg = 'Выберите интересующий вас уровень образования.'
                elif key_set == 3:
                    # Обновляем в БД статус на выбор потока
                    key_set = 1
                    user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=key_set))
                    result_msg = 'Выберите чат своего класса.'
            elif key_command == '/к расписанию':
                key_set = 4
                user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=key_set))
                result_msg = 'Выберите день, для запроса расписания.'
            elif (key_command == '/меню') or (key_command == 'начать'):
                key_set = 1
                user.set_user_status_server(id_user_vk=id_user_vk, id_status=db.select_status(key_stat=key_set))
                result_msg = 'Основное меню.'

            elif key_command in list_week_day:  # обработка по расписанию дней недели
                list_chat_title = chat.title_chat(user_id_vk=id_user_vk)
                tmp_list_title = []
                result_msg = ''
                cycle = 0

                # для обычной клавиатуры
                for item_chat_title in list_chat_title:
                    cycle += 1
                    tmp_list_title.append(item_chat_title)
                    week_letter, header_timetable, selected_day = date_words(key_command)
                    result_msg += f'{header_timetable}\nкласс: {item_chat_title}' \
                                  f'{daily_lesson_schedule(class_letter=tmp_list_title, week_day=week_letter, selected_day=selected_day)}'
                    tmp_list_title.clear()
                    if len(list_chat_title) > cycle:
                        result_msg += '\n\n'
                key_set = 4

                if cycle == 0:
                    result_msg = 'Для запроса расписания необходимо вступить в чат своего класса.'
                    key_set = 1
                db.update_user(user_id_vk=id_user_vk, schedule_date=datetime.today())

            result_keyboard = generator_keyboard(set_keyboard=key_set,
                                                 id_user_vk=id_user_vk,
                                                 flow_class=flow_class, inline=inline_keyboard)
        else:
            result_keyboard = generator_keyboard(set_keyboard=1)
            result_msg = 'Повторите попытку'

    return result_msg, result_keyboard


def daily_lesson_schedule(class_letter=['5Б'], week_day=['Вторник'], selected_day=''):
    """
    Получение расписания на один день
    :param class_letter: list Название классов школы в str
    :param week_day: str день недели(вида "Вторник")
    :param selected_day: str дата выбранного дня(вида "10/24/2022")
    :return:
    """
    data_timetable = db.select_time_table_activate(class_letter=class_letter[0], week_day=week_day[0], selected_day=selected_day)
    str_table = ''
    circle = 0
    for data_week in data_timetable:
        circle += 1
        str_table += '\n' + str(data_week[1])  # номер урока
        str_table += ' - ' + data_week[2]  # предмет
    if circle == 0:
        str_table = '\n*** нет расписания ***'

    return str_table


def date_words(input_week_day):
    """
    Формируем шапку расписания.

    :param input_week_day: День недели (вида "/вт")
    :return: день недели для SQL запроса (вида "Вторник")
    """
    today = datetime.today()
    result_word = []
    week_words = list_week_words
    control_week_day = list_week_day
    month_words = list_month_words

    number_week_day = datetime.weekday(today)
    index_input_week_day = control_week_day.index(input_week_day)
    index_week_today = datetime.weekday(today)
    len_list_week = len(control_week_day)

    # вычисляем дельту между сегодня и запрашиваемым днём
    if index_input_week_day != index_week_today:
        if index_week_today < index_input_week_day:
            delta_day = index_input_week_day - index_week_today
        else:
            delta_day = len_list_week - index_week_today + index_input_week_day
    else:
        delta_day = 0

    tomorrow = today + timedelta(days=delta_day)
    tomorrow_week_day = datetime.weekday(tomorrow)

    # склонение дня недели
    if index_input_week_day in [2, 4, 5]:
        day_week = week_words[tomorrow_week_day][:-1] + 'у'
    else:
        day_week = week_words[tomorrow_week_day]
    number_month = int(tomorrow.strftime('%m'))
    if number_month == 12:
        number_month = 0

    # формируем шапку расписания на день
    header_timetable = f'на {day_week}, {tomorrow.strftime("%d")} ' \
                       f'{month_words[number_month]} ' \
                       f'{tomorrow.strftime("%Y")}г'

    result_word.append(week_words[tomorrow_week_day].capitalize())
    selected_day = tomorrow.strftime("%Y-%m-%d")
    return result_word, header_timetable, selected_day


def generator_keyboard(set_keyboard, id_user_vk=0, inline=False, flow_class=0):
    """
    Генератор клавиатуры согласно роли пользователя в группе.

    :param set_keyboard: номер набора клавиатур
    :param id_user_vk: ID пользователя в ВК
    :param inline: Метод отправки клавиатуры Inline=True или стандартная=False
    :param flow_class: номер потока класса
    :return: keyboard формат ответа json строка
    """
    result = {}
    keyboard = VkKeyboard(inline=inline)

    if set_keyboard == 0:  # клавиатура не участника группы
        result = keyboard.get_empty_keyboard()

    elif set_keyboard == 1:  # клавиатура начального входа без роли
        keyboard.add_button('/начальные классы', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/старшие классы', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        if chat.list_chat_user(user_id_vk=id_user_vk):
            keyboard.add_button('/к расписанию', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        result = keyboard.get_keyboard()

    elif set_keyboard == 2 or set_keyboard == 21:  # клавиатура выбора потока среди классов
        # если это начальная школа, то одна строка с 4-мя клавишами
        # если средняя, то две
        # генерировать клавишу только для существующих потоков
        primary_school = False
        if set_keyboard == 2:
            primary_school = True
        list_flow = chat.grouping_chats_number(primary_school=primary_school)
        count_flow = len(list_flow)
        count_key_row = 0  # счетчик кол-ва клавиш в ряду
        if count_flow != 0:
            count_key_row = 0
            for flow in list_flow:
                count_key_row += 1
                if count_key_row > 4:
                    count_key_row = 0
                    keyboard.add_line()  # Переход на новую строку
                caption_key = '/' + str(flow)
                keyboard.add_button(caption_key, color=VkKeyboardColor.POSITIVE)
        if count_key_row >= 4:
            keyboard.add_line()  # Переход на новую строку

        keyboard.add_button('/назад', color=VkKeyboardColor.PRIMARY)

        result = keyboard.get_keyboard()

    elif set_keyboard == 3 and flow_class > 0:  # клавиатура внутри потока и ссылками на чаты
        list_litter_class = chat.litter_level_chat(flow_class)  # передать номер потока в int
        count_key_row = 0
        if list_litter_class:
            for item in list_litter_class:
                if count_key_row >= 2:  # максимальное число кнопок в ряду
                    count_key_row = 0
                    keyboard.add_line()  # Переход на новую строку
                caption_key = '/чат `' + item[2] + '` класса '
                link_chat = item[3]
                keyboard.add_openlink_button(label=caption_key, link=link_chat)
                count_key_row += 1

        keyboard.add_line()  # Переход на новую строку
        # если юзер участник чата, то добавить кнопку "/к расписанию"
        if chat.title_chat(user_id_vk=id_user_vk):
            keyboard.add_button('/к расписанию', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/назад', color=VkKeyboardColor.PRIMARY)

        result = keyboard.get_keyboard()

    elif set_keyboard == 4:  # клавиатура выбора дня недели расписания
        step = 0
        key_week = week_dict(user_id_vk=id_user_vk)
        for item in list_week_day:
            flag = key_week[item[1:]]
            if flag == 1:
                color_key = VkKeyboardColor.NEGATIVE
            elif flag == 2:
                color_key = VkKeyboardColor.PRIMARY
            elif flag == 3:
                color_key = VkKeyboardColor.SECONDARY
            else:
                color_key = VkKeyboardColor.POSITIVE
            keyboard.add_button(item, color=color_key)
            step += 1
            if step >= 4:
                step = 0
                keyboard.add_line()  # Переход на новую строку

        keyboard.add_line()  # Переход на новую строку

        keyboard.add_button('/меню')
        keyboard.add_button('/важные контакты')

        result = keyboard.get_keyboard()

    elif set_keyboard == 5:  # клавиатура управления участием в чатах
        keyboard.add_button('/вступить в чат', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/я в чатах', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('/назад', color=VkKeyboardColor.PRIMARY)

        result = keyboard.get_keyboard()

    elif set_keyboard == 6:  # клавиатура завуча
        keyboard.add_button('/загрузить расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/активировать расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('/удалить загрузку', color=VkKeyboardColor.NEGATIVE)
        result = keyboard.get_keyboard()

    elif set_keyboard == 7:  # клавиатура с литерами потока
        # получить какой поток запрошен
        # получить какие буквы в этом потоке доступны
        designation_class = 'A'
        caption_key = '/' + designation_class
        keyboard.add_button(caption_key, color=VkKeyboardColor.POSITIVE)

    elif set_keyboard == 10:  # клавиатура с кнопкой назад
        keyboard.add_button('/назад', color=VkKeyboardColor.POSITIVE)
        result = keyboard.get_keyboard()

    elif set_keyboard == 100:  # очистка от всех клавиатур
        result = keyboard.get_empty_keyboard()

    else:  # очистка от всех клавиатур
        result = keyboard.get_empty_keyboard()
    return result


def week_dict(user_id_vk):
    """
    Формируем словарь дат.
    :return: dict Словарь с данными на неделю
    """
    week_control = []
    week_current = []
    name_class = []
    flag_day = []
    holiday = ['каникул']
    bad_day = ['карантин', 'нет уроков']
    w_key = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    # временная заглушка
    flag_day = [0, 0, 0, 0, 0, 0, 0]

    # **************************************************
    today = date.today()  # Получаем текущую дату
    week_day_now = datetime.weekday(today)  # Получаем текущий день недели

    all_chat = chat.list_chat_user(user_id_vk=user_id_vk)  # Получаем чаты пользователя
    for item in all_chat:
        name_class.append(item[1])

    # цикл формирования текущей календарной недели
    for y in range(0, 7):
        tt = y - week_day_now

        # формируем список дней контрольной недели
        if tt < 0:
            delta_day = timedelta(days=tt)
            today_1 = today + delta_day
        else:
            tmp = -7 + tt
            delta_day = timedelta(days=tmp)
            today_1 = today + delta_day
        week_control.append(today_1.strftime("%Y-%m-%d"))

        # формируем список дней клавиатуры текущей недели
        if tt < 0:
            tt += 7
        delta_day = timedelta(days=tt)
        today_1 = today + delta_day
        week_current.append(today_1)

    for current_class in name_class:
        for item in range(7):
            act_day = week_current[item]
            control_day = week_control[item]  #.strftime("%Y-%m-%d")

            wd = list_week_words[item]
            wdc = wd.capitalize()

            action_response = db.select_time_table_activate(class_letter=current_class,
                                                            week_day=wdc, selected_day=act_day)
            control_response = db.select_time_table_activate(class_letter=current_class,
                                                             week_day=wdc, selected_day=control_day)

            if len(action_response) > 0:  # список дня активной даты
                # вытаскиваем урок из активного дня
                action_step = 0
                for action_lesson in action_response:
                    # проверяем на наличие в активном дне слово "каникулы"
                    for special_day in holiday:
                        test_holiday = str(action_lesson[2]).lower()
                        if test_holiday.find(special_day) > 0:
                            flag_day[item] = 2
                            break

                    # проверяем на наличие в активном дне слово "карантин"
                    for special_day in bad_day:
                        test_holiday = str(action_lesson[2]).lower()
                        if test_holiday.find(special_day) >= 0:
                            flag_day[item] = 3
                            break

                    if len(control_response) > 0:  # список дня контрольной даты
                        if (len(action_response) != len(control_response)) \
                                and (flag_day[item] != 2) \
                                and (flag_day[item] != 3):
                            flag_day[item] = 1
                            break
                        else:
                            if (action_lesson[2] != control_response[action_step][2]) \
                                    and (flag_day[item] != 2) \
                                    and (flag_day[item] != 3):
                                flag_day[item] = 1
                                break
                    else:
                        # проверить урок активной недели на текст каникулы
                        flag_day[item] = 1  # красный
                        break  # прерываем цикл

                    action_step += 1
            else:
                flag_day[item] = change_color_flag(flag_day=flag_day, index_control=item)
    # ************************************

    week_key = dict(zip(w_key, flag_day))
    # print('week_key= ', week_key)
    return week_key


def change_color_flag(flag_day, index_control):
    """
    Выставление приоритетов цвета кнопок при изменении на входе
    :param flag_day: список флагов цветов
    :param index_control: проверяемая позиция
    :return: приоритетный цвет
    """
    if flag_day[index_control] != 1:  # приоритет если день уже красный
        if flag_day[index_control] != 2:  # приоритет если день синий
            if flag_day[index_control] == 0:  # если необходимо заменить с зеленого на серый
                return 3  # Если активный день пустой. То красим кнопку в серый цвет

    return flag_day[index_control]


if __name__ == '__main__':
    # для тестов
    key = generator_keyboard(4)
    print('key= ', key)
