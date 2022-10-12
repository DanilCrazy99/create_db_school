# -*- coding: utf-8 -*-
# файл генерации клавиатур

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Create_Community_VK.Bot.Users.user import Community
from Create_Community_VK.Bot.Group.group import Group

gr = Group()  # экземпляр класса Group


def example_keyboard():
    """ Пример создания клавиатуры для отправки ботом """
    #
    # vk_session = vk_api.VkApi(token='bot_api_token')
    # vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Белая кнопка')  # , color=VkKeyboardColor.SECONDARY
    keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Синяя кнопка', color=VkKeyboardColor.PRIMARY)

    keyboard.add_line()  # Переход на новую строку
    keyboard.add_location_button()

    keyboard.add_line()
    keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=74030368&aid=6222115")

    keyboard.add_line()
    keyboard.add_vkapps_button(app_id=6979558,
                               owner_id=-181108510,
                               label="Отправить клавиатуру",
                               hash="sendKeyboard")

    # vk.messages.send(
    #     peer_id=123456,
    #     random_id=get_random_id(),
    #     keyboard=keyboard.get_keyboard(),
    #     message='Пример клавиатуры'
    # )


def generator_keyboard(key_set=100, one_time_method=False, flow_class=0):
    """
    Генератор клавиатуры согласно роли пользователя в группе.

    :param key_set: Номер набора клавиатуры.По умолчанию пустая клавиатура.
    :param one_time_method: Метод отправки клавиатуры Inline=True или стандартная=False
    :param flow_class: номер потока класса
    :return: keyboard формат ответа json строка
    """
    result = {}
    keyboard = VkKeyboard(one_time=one_time_method)

    if key_set == 0:  # клавиатура не участника группы
        keyboard.add_button('/Вступить в группу', color=VkKeyboardColor.POSITIVE)
        result = keyboard.get_keyboard()

    elif key_set == 1:  # клавиатура начального входа без роли
        keyboard.add_button('/начальные классы', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/старшие классы', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.PRIMARY)
        result = keyboard.get_keyboard()

    elif key_set == 2 or key_set == 21:  # клавиатура выбора потока среди классов
        # если это начальная школа, то одна строка с 4-мя клавами
        # если средняя, то две
        # генерировать клавы только для существующих потоков
        primary_school = False
        if key_set == 2:
            primary_school = True
        list_flow = gr.grouping_chats_level(primary_school=primary_school)
        list_flow_sort = sorted(list_flow)
        print('list_flow= ', list_flow_sort)
        count_flow = len(list_flow)
        if count_flow != 0:
            step = 0
            for flow in list_flow:
                step += 1
                if step > 4:
                    step = 0
                    keyboard.add_line()  # Переход на новую строку
                caption_key = '/' + flow
                keyboard.add_button(caption_key, color=VkKeyboardColor.POSITIVE)
        if step >= 4:
            keyboard.add_line()  # Переход на новую строку

        keyboard.add_button('/назад', color=VkKeyboardColor.PRIMARY)

        result = keyboard.get_keyboard()

    elif key_set == 3 and flow_class > 0:  # клавиатура внутри потока и ссылками на чаты
        list_litter_class = gr.litter_level_chat(flow_class)  # передать номер потока в int
        step = 0
        if list_litter_class:
            for item in list_litter_class:
                if step >= 2:  # максимальное число кнопок в ряду
                    step = 0
                    keyboard.add_line()  # Переход на новую строку
                caption_key = '/чат `' + item[2] + '` класса '
                link_chat = item[4]
                keyboard.add_openlink_button(label=caption_key, link=link_chat)
                step += 1

        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/назад', color=VkKeyboardColor.PRIMARY)

        result = keyboard.get_keyboard()

    elif key_set == 4:  # клавиатура выбора дня недели расписания
        keyboard.add_button('/пн', color=color_key())
        keyboard.add_button('/вт', color=color_key())
        keyboard.add_button('/ср', color=color_key())
        keyboard.add_button('/чт', color=color_key())

        keyboard.add_line()  # Переход на новую строку
        # keyboard.add_location_button()

        keyboard.add_button('/пт', color=color_key())
        keyboard.add_button('/сб', color=color_key())
        keyboard.add_button('/вс', color=color_key())

        keyboard.add_line()  # Переход на новую строку

        keyboard.add_button('/меню чатов')
        keyboard.add_button('/важные контакты')

        result = keyboard.get_keyboard()

    elif key_set == 5:  # клавиатура управления участием в чатах
        keyboard.add_button('/вступить в чат', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/я в чатах', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('/назад', color=VkKeyboardColor.PRIMARY)

        result = keyboard.get_keyboard()

    elif key_set == 6:  # клавиатура завуча
        keyboard.add_button('/загрузить расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/активировать расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('/удалить загрузку', color=VkKeyboardColor.NEGATIVE)
        result = keyboard.get_keyboard()

    elif key_set == 7:  # клавиатура с литерами потока
        count_key = 0
        # получить какой поток запрошен
        # получить какие буквы в этом потоке доступны
        designation_class = 'A'
        caption_key = '/' + designation_class
        keyboard.add_button(caption_key, color=VkKeyboardColor.POSITIVE)

    elif key_set == 10:  # клавиатура с кнопкой назад
        keyboard.add_button('/назад', color=VkKeyboardColor.POSITIVE)
        result = keyboard.get_keyboard()

    elif key_set == 100:  # очистка от всех клавиатур
        result = keyboard.get_empty_keyboard()

    else:  # очистка от всех клавиатур
        result = keyboard.get_empty_keyboard()
    return result


def color_key(id_user_vk=None):
    """
    Определение цвета кнопки
    :param id_user_vk: ID пользователя в ВК
    :return: Описатель цвета кнопки
    """
    community = Community()
    result = VkKeyboardColor.POSITIVE
    if id_user_vk:
        # проверка на новое расписание
        result = VkKeyboardColor.POSITIVE
    return result


if __name__ == '__main__':
    # для тестов
    key = generator_keyboard(4)
    print('key= ', key)
