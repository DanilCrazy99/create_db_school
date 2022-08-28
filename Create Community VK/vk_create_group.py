import vk_api
from Variables.Var_community import vk_token, title, description, type, user_id

session = vk_api.VkApi(token=vk_token)
vk = session.get_api()


def create_group():
    vk.groups.create(title=title, description=description, type=type)


def get_list_groups(var_user_id):
    list_groups = vk.groups.get(user_id=var_user_id, filter='admin')
    print(list_groups["count"], ["items"])


get_list_groups(user_id)
