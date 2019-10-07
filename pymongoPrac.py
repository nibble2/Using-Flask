import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://0.0.0.0:5001/', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
card = soup.select('#cards-box > div')

title = soup.select_one('#cards-box > div:nth-child(1) > div > a')


print(title.text)