# -*- coding: utf-8 -*-

control_word = []
list_week_day = ['/пн', '/вт', '/ср', '/чт', '/пт', '/сб', '/вс']
list_word = ['расписание', 'список уроков', 'занятия сегодня', 'какие уроки', 'расписание на ...']
list_week_words = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
list_month_words = ['декабря', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                    'октября', 'ноября']
list_command = ['/начальные классы', '/старшие классы', '/важные контакты', '/меню выше', '/help', '/назад',
                '/вступить в группу', '/меню', '/вступить в чат', '/к расписанию']
list_class = ['/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', '/10', '/11', '/12']

# формируем общий список слов
control_word.extend(list_week_day)
control_word.extend(list_word)
control_word.extend(list_command)
control_word.extend(list_class)
