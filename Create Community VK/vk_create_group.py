import vk_api
import logging
from Variables.Var_community import vk_token, title, description, type, user_id

logging.basicConfig(filename='log.log', level='DEBUG', encoding='utf-8',
                    format='%(asctime)s::%(levelname)s:%(message)s')
session = vk_api.VkApi(token=vk_token)
vk = session.get_api()


def create_group():
    try:
        vk.groups.create(title=title, description=description, type=type)
    except Exception:
        logging.error('Введены не те данные для создания группы:%s', Exception)


def get_list_groups(var_user_id):
    logging.debug('Проверка листа групп администратора, переменные\n'
                  '1)ID пользователя:%s', var_user_id)
    list_groups = vk.groups.get(user_id=var_user_id, extended=1, filter='admin', fields='name')
    count_groups = list_groups['count']
    # print(count_groups)
    """
    items_first_group = list_groups['items'][0]
    name_first_group = items_first_group['name']
    print(name_first_group)
    print(items_first_group)
    items_second_group = list_groups['items'][1]
    print(items_second_group)
    """
    items_all_groups = list_groups['items']
    # print(items_all_groups[1])
    return count_groups, items_all_groups


def check_duplicate_group():
    for i in range(len(items_groups)):
        items_current_group = items_groups[i]
        if title == items_current_group['name']:
            print('Капец. Группа с таким названием уже существует')
            return 0
    else:
        return 1


values_groups = get_list_groups(user_id)  # запрос листа групп от API
counts_groups = values_groups[0]  # [0] = count groups
items_groups = values_groups[1]  # [1] = items groups
items_first_group = items_groups[1]  # items_groups[1] значения первой группы
check_group = check_duplicate_group()
print('Функция check_duplicate_group вернула:', check_group)
if check_group == 1:
    print('Я выполнил основной блок')
    create_group()
else:
    print('Что-то пошло не так. Скорее всего это название\n'
          'уже есть и его нужно поменять на другое')
