import requests
from mysql import connector

proxy = {
    'HTTP': 'http://171.39.41.203:8123'
}
try:
    response = requests.get('http://music.163.com/#/song?id=442314991', proxies=proxy, timeout=10)
except Exception as e:
    print('ConnectionRefusedError, ', e)
else:
    print(response.status_code)
