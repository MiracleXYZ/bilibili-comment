import requests

data = {
    'search_type': 'video',
    'keyword': '王老菊'
}
url = 'https://search.bilibili.com/api/search'
wb_data = requests.get(url, data)

print(wb_data.text)