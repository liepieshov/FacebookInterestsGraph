import json, urllib.request, os, base64, requests
from pprint import pprint


def get_facebook_key():
    with open("info.json", "r", encoding="utf-8") as file_text:
        content_file = json.loads(file_text.read())
    return content_file["app_id"], content_file["app_secret"], content_file["access_token"]
new = "https://graph.facebook.com/v2.9/search?q=Ira+Kostyshyn&type=user&access_token=" + get_facebook_key()[2]
base_url = "https://graph.facebook.com/v2.1/291665527956118?access_token="
app_id, app_secret, facebook_api_key = get_facebook_key()
facebook_api_key = "EAACEdEose0cBAAGlmzWtqZCs1P35659WLx6AivMcbyZBJqV5nzPRcnwl8xMryUk3aGDWtXTVYJopzUM9VaX04ntDPZBoGDkW6393eMSn6HWtbSWwaskHBRZCrBXHEjV2BNyxen3ZB0t75qOPbXubyXDmZC0uMPHxiSXr35NTctY1HHbdRTMc3ouvu4s75fFcAZD"
url = base_url + facebook_api_key
url = "https://api.vk.com/method/users.getFollowers?user_id=14312788&fields=city&count=2&v=5.64"
# print(requests.request("GET", new).json())

response = requests.request("GET", url)
print(response.text)
if str(response) == "<Response [200]>":
    print("True")

data = response.json()
full_content = data
# full_content = data["data"]
# while "paging" in data and "next" in data["paging"]:
#     response = requests.request("GET", data["paging"]["next"])
#     data = response.json()
#     full_content += data["data"]

with open('data.json', 'w', encoding="utf-8") as outfile:
    json.dump(full_content, outfile, ensure_ascii=False)
