import vk_api
import logging
from Create_Community_VK.Config.Var_community import vk_token, title, description, type_community, user_admin, path_logFile

logging.basicConfig(filename=path_logFile, level='DEBUG', encoding='utf-8',
                    format='%(asctime)s:%(levelname)s:Строка-'
                           '%(lineno)d:%(message)s')
logging.info('\nНачало работы программы')

try:
    session = vk_api.VkApi(token=vk_token)
    vk = session.get_api()
except Exception:
    logging.error('Ошибка присваивания Token')


def create_group():
    try:
        vk.groups.create(title=title, description=description, type=type_community)
        print('Новая группа создана')
        logging.info('Новая группа создана')
    except Exception:
        print('Ошибка при создании группы')
        logging.error('Введены не те данные для создания группы:%s', Exception)


def get_list_groups(var_user_id):
    logging.debug('Проверка листа групп администратора, переменные\n'
                  'ID пользователя:%s', var_user_id)
    list_groups = vk.groups.get(user_id=var_user_id, extended=1, filter='admin', fields='name')
    count_groups = list_groups['count']
    items_all_groups = list_groups['items']
    return count_groups, items_all_groups


def check_duplicate_group():
    for i in range(len(items_groups)):
        items_current_group = items_groups[i]
        if title == items_current_group['name']:
            print('Группа с таким названием уже существует')
            return 0
    else:
        return 1


try:
    values_groups = get_list_groups(user_admin)  # запрос листа групп от API
except Exception as Er:
    logging.error('Произошла ошибка во время считывания листа групп администратора: %s', Er)
counts_groups = values_groups[0]  # [0] = count groups
items_groups = values_groups[1]  # [1] = items groups
items_first_group = items_groups[1]  # items_groups[1] значения первой группы
check_group = check_duplicate_group()
logging.debug('Функция check_duplicate_group вернула: %d', check_group)
if check_group == 1:
    create_group()
else:
    pass

logging.info('\nПрограмма закончила свою работу')
