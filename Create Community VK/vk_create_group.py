import vk_api
from Variables.Var_community import vk_token
from Variables.Var_community import title, description, type
token = vk_token
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

def main():



    # vk_create_group = vk_session.method()
    """
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """


if __name__ == '__main__':
    main()
