# -*- coding: utf8 -*-

control_word = []
list_week_day = ['/пн', '/вт', '/ср', '/чт', '/пт', '/сб', '/вс']
list_word = ['расписание', 'список уроков', 'занятия сегодня', 'какие уроки', 'расписание на ...']
list_week_words = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
list_month_words = ['декабря', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                    'октября', 'ноября']
list_command = ['/начальные классы', '/старшие классы', '/exit', '/важные контакты', '/меню выше']

# формируем общий список слов
control_word.extend(list_week_day)
control_word.extend(list_word)
control_word.extend(list_command)
