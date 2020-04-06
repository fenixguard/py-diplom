import json
import time
from datetime import datetime

import requests

VK_URL = 'https://api.vk.com/method/'
VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
VK_API_VERSION = 5.103


def get_user_id(user_id) -> int:
    method_name = "users.get"

    payload = {
        "user_ids": user_id,
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION
    }
    vk_url = f"{VK_URL}{method_name}"
    time.sleep(0.5)
    print(f"{datetime.now()} - Получение числового идентификатора пользователя {user_id}")
    response = requests.get(vk_url, params=payload)
    json_dict = response.json()
    return json_dict['response'][0]['id']


def get_friends(user_id) -> list:
    method_name = "friends.get"

    payload = {
        "user_id": user_id,
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION
    }

    vk_url = f"{VK_URL}{method_name}"
    time.sleep(0.5)
    print(f"{datetime.now()} - Получение списка друзей пользователя {user_id}")
    response = requests.get(vk_url, params=payload)
    json_dict = response.json()
    try:
        if json_dict['error'] == 18 or json_dict['error'] == 30:
            return []
    except KeyError:
        return json_dict['response']['items']


def get_groups(user_id) -> set:
    method_name = "users.getSubscriptions"

    payload = {
        "user_id": user_id,
        "extended": 0,
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION
    }

    vk_url = f"{VK_URL}{method_name}"
    time.sleep(0.5)
    print(f"{datetime.now()} - Получение списка групп пользователя {user_id}")
    response = requests.get(vk_url, params=payload)
    json_dict = response.json()
    try:
        if json_dict['error'] == 18 or json_dict['error'] == 30:
            return set([])
    except KeyError:
        return set(json_dict['response']['groups']['items'])


def get_group_info(groups) -> list:
    groups_info = list()
    method_name = "groups.getById"
    # parameter = "group_ids="
    # for group_id in groups:
    #     parameter += f"{group_id},"
    # parameters = f"{parameter[:-1]}&fields=id,name,members_count"
    #
    # payload = f"{parameters}&{VK_TOKEN}&{VK_API_VERSION}"
    groups_id = ','.join(str(group_id) for group_id in groups)
    payload = {
        "group_ids": groups_id,
        "fields": "id,name,members_count",
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION
    }

    vk_url = f"{VK_URL}{method_name}"
    time.sleep(0.5)
    print(f"{datetime.now()} - Получение информации о группах")
    response = requests.get(vk_url, params=payload)
    json_dict = response.json()
    for item in json_dict['response']:
        temp_dict = dict()
        temp_dict['id'] = f"{item['id']}"
        temp_dict['name'] = item['name']
        temp_dict['members_count'] = item['members_count']
        groups_info.append(temp_dict)
    return groups_info


def main():
    user_id = input("Введите ID пользователя (числовой либо буквенный): ")
    if user_id.isalpha():
        user_id = get_user_id(user_id)
    friends = get_friends(user_id)
    target_groups = get_groups(user_id)

    for friend in friends:
        user_group = get_groups(friend)
        if user_group is not None:
            target_groups = target_groups - user_group
    result = get_group_info(list(target_groups))
    with open("groups.json", "w", encoding="utf-8") as ff:
        json.dump(result, ff, ensure_ascii=False, indent=4)
    print("Данные групп сохранены в файл 'groups.json' в корне проекта.")


if __name__ == '__main__':
    main()
