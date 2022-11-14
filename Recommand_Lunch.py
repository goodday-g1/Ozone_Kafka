# kafka.KafkaProducer , kafka.KafkaConsumer , json.loads, json.dumps , time  

from kafka import KafkaProducer  
from kafka import KafkaConsumer  
from json import loads, dumps  
import time  
 
producer = KafkaProducer(acks=0, compression_type='gzip',
                             bootstrap_servers=['{kafka_server}:{kafka_port}'],
                             api_version=(0,11,5),
                             batch_size=100000,
                             linger_ms=600000,
                             value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'))

# today_weather
import requests
import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus


#### A. BASE
import datetime

today_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
service_key = #SERVICE_KEY

base_date = datetime.datetime.today().strftime("%Y%m%d")


base_time = "1100"

nx = "62"
ny = "123"

payload = "serviceKey=" + service_key + "&" + \
          "dataType=json" + "&" + \
          "base_date=" + base_date + "&" + \
          "base_time=" + base_time + "&" + \
          "nx=" + nx + "&" + \
          "ny=" + ny

res = requests.get(today_weather_url + payload)

try:
    today_weather = res.json().get('response').get('body').get('items')

except:
    print("날씨 정보 요청 실패 : ", res.text)


#### B.CUSTOM

print("날씨를 구하고자 하는 지역의 좌표값 (x y) 입력 /ex) 경기도 분당구 수내1동 (62 123)")
print("(x y) : ", end="")
nx,ny=input().split()

from datetime import date, datetime, timedelta 
now = datetime.now()

today = datetime.today()
today_date = today.strftime("%Y%m%d")


if now.hour<2 or (now.hour==2 and now.minute<=10):
    base_date=yesterday_date 
    base_time="2300"
elif now.hour<5 or (now.hour==5 and now.minute<=10): 
    base_date=today_date
    base_time="0200"
elif now.hour<8 or (now.hour==8 and now.minute<=10): 
    base_date=today_date
    base_time="0500"
elif now.hour<=11 or now.minute<=10: 
    base_date=today_date
    base_time="0800"
elif now.hour<14 or (now.hour==14 and now.minute<=10):
    base_date=today_date
    base_time="1100"
elif now.hour<17 or (now.hour==17 and now.minute<=10): 
    base_date=today_date
    base_time="1400"
elif now.hour<20 or (now.hour==20 and now.minute<=10): 
    base_date=today_date
    base_time="1700" 
elif now.hour<23 or (now.hour==23 and now.minute<=10): 
    base_date=today_date
    base_time="2000"
else: 
    base_date=today_date
    base_time="2300"
    
print(base_time)


payload = "serviceKey=" + service_key + "&" + \
          "dataType=json" + "&" + \
          "base_date=" + base_date + "&" + \
          "base_time=" + base_time + "&" + \
          "nx=" + nx + "&" + \
          "ny=" + ny

res = requests.get(today_weather_url + payload)

try:
    today_weather = res.json().get('response').get('body').get('items')
    # print(today_weather)
except:
    print("날씨 정보 요청 실패 : ", res.text)


res = requests.get(today_weather_url + payload)

try:
    today_weather = res.json().get('response').get('body').get('items')
    print(today_weather)
except:
    print("날씨 정보 요청 실패 : ", res.text)

td_wt = dict()
td_wt['baseDate'] = base_date
td_wt['baseTime'] = base_time

# for item in today_weahter['item']:
#     td_wt['category'] = item['category']

for i in range(len(today_weather['item'])):
    td_wt[today_weather['item'][i]['category']] = today_weather['item'][i]['fcstValue']

# json 형태로 변환
td_wt = json.dumps(td_wt, ensure_ascii=False)
td_wt


today_weather = dict()

today_weather['날짜'] = base_date

#today_weather_data = dict()
for item in td_wt['item']:
    # 기온
    if item['category'] == 'TMP':
        today_weather['기온'] = item['fcstValue']
    
    # 기상상태
    if item['category'] == 'PTY':
        weather_code = item['fcstValue']
        
        if weather_code == '1':
            weather_state = '비'
        elif weather_code == '2':
            weather_state = '비/눈'
        elif weather_code == '3':
            weather_state = '눈'
        elif weather_code == '4':
            weather_state = '소나기'
        else:
            weather_state = '맑음'
        
        today_weather['기상코드'] = weather_code
        today_weather['상태'] = weather_state

#today_weather['날씨'] = weather_data
#today_weather['weather']

today_weather
today_weather = json.dumps(today_weather,ensure_ascii=False)
today_weather

producer = KafkaProducer(acks=0, compression_type='gzip',
                             bootstrap_servers=['{IP}:{Port}'],
                             api_version=(0,11,5),
                             batch_size=100000,
                             linger_ms=600000,
                             value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'))

start = time.time()
producer.send('weather', value=td_wt)
producer.flush()
print("소요시간 :", time.time() - start)


from kafka import KafkaConsumer

consumer = KafkaConsumer('weather', 
                         bootstrap_servers= '{IP}:{Port},{IP}:{Port},{IP}:{Port}',
                         bootstrap_servers= '{IP}:{Port}',
                         enable_auto_commit=True, 
                         auto_offset_reset='earliest',
                         api_version=(0, 10, 1))

for message in consumer: 
    print("Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format( message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))


import selenium
from selenium import webdriver # as wd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer


keyword = "점심"
cnt = 20

#username = #INSTA_ID
#userpw = #INSTA_PW
time.sleep(3)

url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

# # dataframe 만들기
#instagram_account =[]
#instagram_tags = []
#instagram_tag_dates = []

loginUrl = 'https://www.instagram.com/accounts/login/'

def insta_login(driver):
    username = #ID
    userpw = #PW
    time.sleep(3)

    loginUrl = 'https://www.instagram.com/accounts/login/'
    
    driver.get(loginUrl)
    time.sleep(2)
 
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(userpw)
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR,'button.sqdOP.L3NKy.y3zKF').click()
    time.sleep(4)

    driver.find_element(By.CSS_SELECTOR,'button.sqdOP.yWX7d.y3zKF').click()
    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR,'button.aOOlW.HoLwm').click()
    time.sleep(3)

def get_keyword(keyword):
    url = "https://www.instagram.com/explore/tags/{}/".format(keyword)
    
    driver.get(url)
    time.sleep(10)

    driver.find_element(By.CSS_SELECTOR, '#react-root > div > div > section > main > article > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > a > div.eLAPa > div._9AhH0').click()
    
    time.sleep(2)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ''

    tags = re.findall(r'#[^\s#,\\]+', content)  
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    try:
         #like = soup.select('div.Nm9Fw > button')[0].text[4:-1]   
        like = soup.select('.Nm9Fw')[0].text[4:-1]
    except:
        like = 0
    try: 
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''
        
    insta_data = [content, date, like, place, tags]
    return insta_data

#get_content(driver)
def move_next(driver):
    driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div/div[2]/button').click()
    time.sleep(2)
insta= []
target = 200
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
time.sleep(2)


insta_login(driver)

get_keyword("점심")

for i in range(target):
    try:
        insta_data = get_content(driver)
        insta.append(insta_data)
        move_next(driver)
        
        if (i+1) % 50 == 0:
            print( str(i) +1 +"번째까지 게시물 정보 수집 완료")

    except:
        time.sleep(2)

driver.close()

insta_raw = pd.DataFrame(insta)
insta_raw.columns = ['content', 'date', 'like', 'place', 'tags']


insta_raw['like'] = pd.to_numeric(insta_raw.like, errors='coerce').fillna(0)


insta_raw['like'] =  insta_raw['like'].astype(int)

insta_raw
import re

def text_cleaning(text):
    #hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글의 정규표현식
    #result = re.sub('[^ A-Za-z0-9가-힣]', '', text)    
    result = re.sub('[^ A-Za-z0-9ㄱ-ㅣ가-힣]+', '',text) #한글+영어+숫자
    
    #result = result.sub('', text)
    return result

insta_raw['content'] = insta_raw['content'].apply(lambda x : text_cleaning(x))

insta_raw.head()

import json
insta = insta_raw.to_json(orient = 'records')
insta = json.loads(insta)

insta
producer = KafkaProducer(acks=0, compression_type='gzip',
                             bootstrap_servers=['{IP}:{Port}'],
                             api_version=(0,11,5),
                             batch_size=100000,
                             linger_ms=600000,
                             value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'))

start = time.time()
producer.send('insta', value=insta)
producer.flush()
print("소요시간 :", time.time() - start)


from konlpy.corpus import kolaw
from konlpy.tag import Okt
import nltk

okt = Okt()
ko = nltk.Text(insta_raw['content'])

stopword = ['', ' ', '      ']

ko = [i for i in ko if i not in stopword]
nouns = []

for i in range(len(ko)):
    nouns.append(okt.nouns(ko[i]))
    
nouns = [i for i in nouns if i not in stopword]

nounse = []

for i in range(len(nouns)):
    for j in range(len(nouns[i])):
        nounse.append(nouns[i][j])
from collections import Counter
count = Counter(nounse)
common_tags = count.most_common()


most_food = pd.DataFrame(common_tags, columns=['단어','횟수'])
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

food_df = pd.read_csv('./Food_Dictionary_csv.csv', encoding='cp949')

food = food_df[food_df['음식명'].isin(i for i in nounse)]


food_nouns = pd.merge(most_food, food, how="inner", left_on='단어', right_on='음식명')
food_nouns
food_nouns = food_nouns.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
food_nouns

food_nouns = food_nouns.to_json(orient = 'records')
producer = KafkaProducer(acks=0, compression_type='gzip', \
                         bootstrap_servers=['{IP}:{Port}','{IP}:{Port}','{IP}:{Port}'], \
                         value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'), \
                         api_version=(0, 10, 1))

start = time.time()
producer.send('insta', value=insta)
producer.flush()
print("소요시간 :", time.time() - start)
food_json = df.to_json(food_nouns, ascii=False)
#food_json = json.dumps(food_nouns, ensure_ascii=False)
#food_json = food_nouns.to_json(orient = 'records')
food_json = food_nouns.to_json(orient = 'columns', ensure_ascii=False)
#food_json = food_json.loads(food_json, ensure_ascii=False)
food_nouns


#rstr_dfs = pd.DataFrame(columns=['title','link',' category','description','telephone','roadAddress'])
rstr_dfs = pd.DataFrame(columns=['추천음식','추천식당','분류','도로명 주소'])

url = "https://openapi.naver.com/v1/search/local"
lm = "수내 " + rc_food_name[i] + " 맛집"
query = "?query="+urllib.parse.quote(lm)+"&sort=random&display=3&start=1"
url_query = url + query

request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)


response = urllib.request.urlopen(request)
rescode = response.getcode()
remove_tag = re.compile('<.*?>')

        if(rescode == 200):
            res = response.read().decode('utf-8')
            res = re.sub(remove_tag,'',res)
            res = re.sub('경기도 성남시 분당구 ','',res)
            res = re.sub('&amp;','',res)
            if(res == None):
                print("검색 실패!!!")
                exit()
            else:
                #검색 결과를 json개체로 로딩
                json_response = json.loads(res)
                if(json_response == None):
                    print("json.loads 실패!!!")
                    exit()
                else:
                    rstr_json = json_response['items']
                    rstr_df = pd.DataFrame(rstr_json, columns=['title','category','roadAddress'])
                    rstr_df.columns=['추천식당','분류','도로명 주소']
                    #rstr_df = pd.DataFrame(rstr_json, columns=['title','link','category','description','telephone','roadAddress'])
                    rstr_df['추천음식'] = rc_food_name[i]

import logging
import pandas as pd
import os

import time
from datetime import datetime
from made import interactWithOzone
from made import instaCrawling
from made import instaNLTK
from made import toKafka
import json
from made import sshSendCommand
from made import awsMysql
from datetime import datetime
from made import awsMysql
import os
import pandas as pd
import urllib
import random
import requests
import json
import re

client_id = #ID
client_secret = #SECRET

url = "https://openapi.naver.com/v1/search/local"
lm = "수내 떡볶이 맛집"
query = "?query="+urllib.parse.quote(lm)+"&sort=random&display=3&start=1"
url_query = url + query

request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()
remove_tag = re.compile('<.*?>')
res = response.read().decode('utf-8')
json_response = json.loads(res)
json_response
