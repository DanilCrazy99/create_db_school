import vk_api
from Variables.Var_community import vk_token, title, description, type

session = vk_api.VkApi(token=vk_token)
vk = session.get_api()


def create_group():
    vk.groups.create(title=title, description=description, type=type)


create_group()
