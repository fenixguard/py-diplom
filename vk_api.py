import json
import time
from datetime import datetime
from tqdm import tqdm

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


def get_groups_execute(user_ids: list, target_user_groups: set):
    method_name = "execute"
    vk_url = f"{VK_URL}{method_name}"
    max_requests = 25  # Максимальное количество обращений к API внутри execute
    chop_user_ids = [user_ids[x: max_requests + x] for x in range(0, len(user_ids), max_requests)]
    json_dict = list()
    for chop_user_id in tqdm(chop_user_ids, desc="Получение списка групп всех друзей"):

        response = requests.get(vk_url, params=
        {
            "code": f"var count = {len(chop_user_id)};"
                    "var groups = [];"
                    f"var list_ids = {chop_user_id};"
                    "var list_count = 0;"
                    "while (count)"
                        "{"
                            "groups.push(API.users.getSubscriptions({\"user_id\": list_ids[list_count], \"extended\": 0}));"
                            "count = count - 1;"
                            "list_count = list_count + 1;"
                        "}"
                    "return groups;",
            "access_token": VK_TOKEN,
            "v": VK_API_VERSION
        })
        json_dict.append(response.json()['response'])

        # Таймер на случай, если быстро отработает запрос, и будет более 3 execute в секунду,
        # хотя на практике у меня не удалось такое сделать, поэтому закомментил его
        # time.sleep(0.5)

    for items in json_dict:
        for item in items:
            if item:
                target_user_groups = target_user_groups - set(item['groups']['items'])
            else:
                continue
    return target_user_groups


def get_groups(user_id) -> set:
    method_name = "users.getSubscriptions"

    payload = {
        "user_id": user_id,
        "extended": 0,
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION
    }

    vk_url = f"{VK_URL}{method_name}"
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

    target_groups = get_groups_execute(friends, target_groups)

    result = get_group_info(list(target_groups))
    with open("groups.json", "w", encoding="utf-8") as ff:
        json.dump(result, ff, ensure_ascii=False, indent=4)
    print("Данные групп сохранены в файл 'groups.json' в корне проекта.")


if __name__ == '__main__':
    main()
