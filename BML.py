import json
import requests
import time
from similarity import user_similarity_analysis

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

BML_url = 'https://www.bilibili.com/activity/web/view/data/122'

BML_data = requests.get(BML_url, headers=HEADERS)
BML_json = json.loads(BML_data.text)['data']['list']

names = [user['data']['name'] for user in BML_json if len(user['data']['space']) > 0]
uids = [int(user['data']['space']) for user in BML_json if len(user['data']['space']) > 0]

print(len(names))
print(len(uids))

retry_count = 0
while retry_count <= 10:
    try:
        user_similarity_analysis(names, uids, 'BML')
        break
    except:
        retry_count += 1
        print('Waiting...')
        time.sleep(60)
        print('Retrying...')

