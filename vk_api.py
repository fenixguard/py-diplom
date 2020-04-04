import requests

VK_URL = 'https://api.vk.com/method/'
VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

METHOD_NAME = "friends.get"
PARAMETERS = "user_id=25973125"
ACCESS_TOKEN = f"access_token={VK_TOKEN}"
V = f"v={5.103}"

payload = f"{PARAMETERS}&{ACCESS_TOKEN}&{V}"
VK_URL = f"{VK_URL}{METHOD_NAME}"


response = requests.get(VK_URL, params=payload)
json_dict = response.json()
print(response)
