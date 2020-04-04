import requests

VK_URL = 'https://api.vk.com/method/'
VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


def get_friends() -> list:
    method_name = "friends.get"
    parameters = "user_id=171691064"
    access_token = f"access_token={VK_TOKEN}"
    version_api = f"v={5.103}"

    payload = f"{parameters}&{access_token}&{version_api}"
    vk_url = f"{VK_URL}{method_name}"

    response = requests.get(vk_url, params=payload)
    json_dict = response.json()
    return json_dict['response']['items']


def get_groups(friend) -> list:
    


    return []


if __name__ == '__main__':
    friends = get_friends()
    for friend in friends:
        get_groups(friend)
    print(friends)
