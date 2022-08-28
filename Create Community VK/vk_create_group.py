import vk_api
from Variables.Var_community import vk_token, title, description, type, user_id

session = vk_api.VkApi(token=vk_token)
vk = session.get_api()


def create_group():
    vk.groups.create(title=title, description=description, type=type)


def get_list_groups(var_user_id):
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
    for i in range(len((values_groups[1]))):
        items_first_group = values_groups['items'][1]
        print(i, items_first_group['name'])
    else:
        return 1


values_groups = get_list_groups(user_id)
# [0] = count groups
# [1] = items groups
counts_groups = values_groups[0]
items_groups = values_groups[1]
# items_groups[1] значения первой группы
items_first_group = items_groups[1]
print(items_first_group['name'])

