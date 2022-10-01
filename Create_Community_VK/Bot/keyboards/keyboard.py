# -*- coding: utf8 -*-
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


def generator_keyboard(role_id, one_time_method=False):
    """
    Генератор клавиатуры согласно роли пользователя в группе.

    :param role_id: Роль пользователя в группе
    :param one_time_method: Метод отправки клавиатуры Inline=True или стандартная=False
    :return: keyboard формат ответа json строка
    """
    result = {}
    keyboard = VkKeyboard(one_time=one_time_method)

    if role_id == 1:  # клавиатура начального входа без роли
        keyboard.add_button('/начальные классы', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/старшие классы', color=VkKeyboardColor.POSITIVE)
        result = keyboard.get_keyboard()

    elif role_id == 2:  # клавиатура выбора потока среди классов
        # если это начальная школа, то одна строка с 4-мя клавами
        # если средняя, то две
        # генерировать клавы только для существующих потоков
        primary_school = True
        list_flow = gr.grouping_chats_level(primary_school=primary_school)
        count_flow = len(list_flow)
        if count_flow != 0:
            if count_flow > 4:
                step = 0
                for flow in list_flow:
                    step += 1
                    if step == 4:
                        keyboard.add_line()  # Переход на новую строку
                    caption_key = '/' + flow
                    keyboard.add_button(caption_key, color=VkKeyboardColor.POSITIVE)

        result = keyboard.get_keyboard()

    elif role_id == 3:  # клавиатура внутри потока и ссылками на чаты
        list_litter_class = gr.litter_level_chat()
        step = 0
        if list_litter_class:
            step += 1
            if step == 4:
                keyboard.add_line()  # Переход на новую строку
            caption_key = '/' + list_litter_class[2]
            keyboard.add_button(caption_key, color=VkKeyboardColor.POSITIVE)

        result = keyboard.get_keyboard()

    elif role_id == 4:  # клавиатура выбора дня недели расписания
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

        keyboard.add_button('/меню выше')
        keyboard.add_button('/важные контакты')

        result = keyboard.get_keyboard()

    elif role_id == 5:  # клавиатура управления участием в чатах
        keyboard.add_button('/вступить в чат', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('/покинуть чат', color=VkKeyboardColor.NEGATIVE)

        result = keyboard.get_keyboard()

    elif role_id == 6:  # клавиатура завуча
        keyboard.add_button('/загрузить расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('/активировать расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()  # Переход на новую строку
        keyboard.add_button('/help', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('/удалить загрузку', color=VkKeyboardColor.NEGATIVE)
        result = keyboard.get_keyboard()

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
