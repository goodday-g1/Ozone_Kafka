
# **0. 카프카 테스트**
## 0.1 Kafka-Producer 테스트

- 필요한 라이브러리
- kafka.KafkaProducer , kafka.KafkaConsumer , json.loads, json.dumps , time  
```py
  from kafka import KafkaProducer  
  from kafka import KafkaConsumer  
  from json import loads, dumps  
  import time  
  ```

- 테스트
```python
producer = KafkaProducer(acks=0, compression_type='gzip',
                             bootstrap_servers=['{kafka_server}:{kafka_port}'],
                             api_version=(0,11,5),
                             batch_size=100000,
                             linger_ms=600000,
                             value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'))
```
<br>

# 1. 데이터 준비
## 1.1 기상청 데이터
 - 당일 날씨 데이터(today_weather)
  
### 1.1.1 사전 준비
- 필요한 라이브러리 import
  ```python
  import requests # HTTP 요청
  import json # json 파일 파싱하여 데이터 읽기
  import datetime # 날짜시간 모듈

  from urllib.request import Request, urlopen
  from urllib.parse import urlencode, quote_plus
  ```

### 1.1.2 데이터 요청하기
- 여러 가지 방안이 있어서, '가' 방안과 '나' 방안으로 나누어 정리
  
#### 가. BASE

```python
import datetime

today_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
service_key = #{SERVICE KEY}

base_date = datetime.datetime.today().strftime("%Y%m%d") # base_date =  "20211027"

# 기준 시간
# 1일 총 8번 예보 데이터 발생(0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
base_time = "1100"

#수내1동 위치 정보 좌표 값(x : 62, y: 123)
nx = "62"
ny = "123"

payload = "serviceKey=" + service_key + "&" + \
          "dataType=json" + "&" + \
          "base_date=" + base_date + "&" + \
          "base_time=" + base_time + "&" + \
          "nx=" + nx + "&" + \
          "ny=" + ny

# 값 요청
res = requests.get(today_weather_url + payload)

try:
    today_weather = res.json().get('response').get('body').get('items')

except:
    print("날씨 정보 요청 실패 : ", res.text)

```

#### 나. 데이터 값을 변수로 입력받아서 요청받은 방안
```python
# 1) 구하고자 하는 지역의 좌표값 입력 
## 나중에는 지역을 선택해서, 좌표값을 찾아주는 걸로 만들어도 좋을 듯
print("날씨를 구하고자 하는 지역의 좌표값 (x y) 입력 /ex) 경기도 분당구 수내1동 (62 123)")
print("(x y) : ", end="")
nx,ny=input().split()

# 2) 현재 시간 직전 업데이트 데이터 조회

# 현재 날짜 외의 날짜 구하기 위한 모듈
from datetime import date, datetime, timedelta 


now = datetime.now()

print("현재 시간:", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초") # 확인

# 오늘
today = datetime.today() # 현재 지역 날짜 반환
today_date = today.strftime("%Y%m%d") # 오늘의 날짜 (연도/월/일 반환)
print('오늘의 날짜는', today_date)

# # 어제
#yesterday = date.today() - timedelta(days=1)
#yesterday_date=yesterday.strftime('%Y%m%d')
#print('어제의 날짜는', yesterday_date)


# # 현재 시간의 직전에 업데이트된 데이터를 base_time, base_date로 설정
if now.hour<2 or (now.hour==2 and now.minute<=10): # 0시~2시 10분 사이
    base_date=yesterday_date # 구하고자 하는 날짜가 어제의 날짜
    base_time="2300"
elif now.hour<5 or (now.hour==5 and now.minute<=10): # 2시 11분~5시 10분 사이
    base_date=today_date
    base_time="0200"
elif now.hour<8 or (now.hour==8 and now.minute<=10): # 5시 11분~8시 10분 사이
    base_date=today_date
    base_time="0500"
elif now.hour<=11 or now.minute<=10: # 8시 11분~11시 10분 사이
    base_date=today_date
    base_time="0800"
elif now.hour<14 or (now.hour==14 and now.minute<=10): # 11시 11분~14시 10분 사이
    base_date=today_date
    base_time="1100"
elif now.hour<17 or (now.hour==17 and now.minute<=10): # 14시 11분~17시 10분 사이
    base_date=today_date
    base_time="1400"
elif now.hour<20 or (now.hour==20 and now.minute<=10): # 17시 11분~20시 10분 사이
    base_date=today_date
    base_time="1700" 
elif now.hour<23 or (now.hour==23 and now.minute<=10): # 20시 11분~23시 10분 사이
    base_date=today_date
    base_time="2000"
else: # 23시 11분~23시 59분
    base_date=today_date
    base_time="2300"
    
print(base_time)


# 입력받은 값으로 API 값 요청하기
payload = "serviceKey=" + service_key + "&" + \
          "dataType=json" + "&" + \
          "base_date=" + base_date + "&" + \
          "base_time=" + base_time + "&" + \
          "nx=" + nx + "&" + \
          "ny=" + ny

# 값 요청
res = requests.get(today_weather_url + payload)

try:
    today_weather = res.json().get('response').get('body').get('items')
    # print(today_weather)
except:
    print("날씨 정보 요청 실패 : ", res.text)
```

### 1.1.3 조회하기
- 여러 가지 방안이 있어서, '가' 방안과 '나' 방안으로 나누어 정리
  
#### 가. BASE (RAW)/ 조회 데이터 받을 수 있는 모든 정보
```python
# 값 요청
res = requests.get(today_weather_url + payload)

try:
    today_weather = res.json().get('response').get('body').get('items')
    print(today_weather)
except:
    print("날씨 정보 요청 실패 : ", res.text)
# 불필요한 내용 정제하여 중복 내용(baseDate/baseTime) 없이 정리

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
```


#### 나. 필요한 정보만 추출해서 dict 형태로 묶기
```python
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
            
#         today_weather_data['코드'] = weather_code
#         today_weather_data['상태'] = weather_state
        
        today_weather['기상코드'] = weather_code
        today_weather['상태'] = weather_state

#today_weather['날씨'] = weather_data
#today_weather['weather']

today_weather
today_weather = json.dumps(today_weather,ensure_ascii=False)
today_weather
### 1.1.4 카프카로 보내기
#### 나. Producer 생성 및 데이터 send
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

#다른 표현식
from kafka import KafkaConsumer

consumer = KafkaConsumer('weather', 
                         bootstrap_servers= '{IP}:{Port},{IP}:{Port},{IP}:{Port}',
                         bootstrap_servers= '{IP}:{Port}',
                         enable_auto_commit=True, 
                         auto_offset_reset='earliest',
                         api_version=(0, 10, 1))

for message in consumer: 
    print("Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format( message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))

```

# 1.2 인스타 크롤링 데이터
### 1.2.1 사전 준비
- 필요한 라이브러리 준비
  > selenium, selenium.webdriver, webdriver_manger

```python
# !pip install selenium
import selenium
from selenium import webdriver # as wd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# Selenium 최신 라이브러리 ChromeDriverManager
# !pip install selenium.webdriver.chrome.service 
# !pip install webdriver-manager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
```

### 1.2.2 스크래핑 환경 설정
- 필요한 정보 정의
```python
# 해시태그 검색어 및 타겟 게시글 수 선정
keyword = "점심"
cnt = 20

# 로그인 정보
username = #ID
userpw = #PW
time.sleep(3)

# 해시태그 url 값
url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

# # dataframe 만들기
#instagram_account =[]
#instagram_tags = []
#instagram_tag_dates = []

# 인스타 로그인 URL
loginUrl = 'https://www.instagram.com/accounts/login/'
### 1.2.3 인스타그램 로그인 (Chrome Driver 실행)
def insta_login(driver):
    # 로그인 정보
    username = #ID
    userpw = #PW
    time.sleep(3)


    # 인스타 로그인 URL
    loginUrl = 'https://www.instagram.com/accounts/login/'
    
    # Chrome drvier 실행
    driver.get(loginUrl)
    time.sleep(2)

    # login
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(userpw)
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR,'button.sqdOP.L3NKy.y3zKF').click()
    time.sleep(4)

    # 정보 나중에 저장하기 클릭하고 넘어가기
    driver.find_element(By.CSS_SELECTOR,'button.sqdOP.yWX7d.y3zKF').click()
    time.sleep(3)

    # 설정 나중에하기 클릭하고 넘어가기
    driver.find_element(By.CSS_SELECTOR,'button.aOOlW.HoLwm').click()
    time.sleep(3)
def get_keyword(keyword):
    # 해시태그 url 값
    url = "https://www.instagram.com/explore/tags/{}/".format(keyword)
    
    # 해시태그 검색 창에 "키워드" 검색
    driver.get(url)
    time.sleep(10)

    # 최근 게시글 첫 게시물 클릭
    driver.find_element(By.CSS_SELECTOR, '#react-root > div > div > section > main > article > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > a > div.eLAPa > div._9AhH0').click()
    
    time.sleep(2)
###### Function1. get_content() : 게시글 스크래핑
def get_content(driver):

    # 1. 현재 게시글 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')


    # 2. content : 본문 내용
    # 본문 내용이 없을 수 있으므로 예외 처리구문을 이용
    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ''

    # 3. tags : 해시태그 데이터 (정규 표현식 이용)
    tags = re.findall(r'#[^\s#,\\]+', content)  

    # 4. date : 작성 일자
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]

    # 5. like: 좋아요 수
    try:
         #like = soup.select('div.Nm9Fw > button')[0].text[4:-1]   
        like = soup.select('.Nm9Fw')[0].text[4:-1]
    except:
        like = 0
        
    # 6. place : 위치정보
    try: 
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''
        
    # 7. 저장하기
    insta_data = [content, date, like, place, tags]
    return insta_data

#get_content(driver)
###### Function2. move_next() : 다음 게시글로 이동
# 다음 게시물 클릭
def move_next(driver):
    driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div/div[2]/button').click()
    time.sleep(2)
###### Action. 코드 실행
insta= []
target = 200

# Chrome drvier 실행
# driver = wd.Chrome("C:/Users/G1/chromedriver.exe")
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
#like 컬럼 중 숫자가 아닌 경우는 0으로 변경
# errors = 'coerce' : 숫자가 아닌 경우, Nan으로 처리하란 명령어

insta_raw['like'] = pd.to_numeric(insta_raw.like, errors='coerce').fillna(0)

# 소수점 제거(float 타입을 int타입으로 변경)
insta_raw['like'] =  insta_raw['like'].astype(int)

insta_raw
## 1. text 컬럼 -> 텍스트 데이터 정제
### 1.1 한글 이외의 문자 제거

import re

def text_cleaning(text):
    #hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글의 정규표현식
    #result = re.sub('[^ A-Za-z0-9가-힣]', '', text)    
    result = re.sub('[^ A-Za-z0-9ㄱ-ㅣ가-힣]+', '',text) #한글+영어+숫자
    
    #result = result.sub('', text)
    return result

# content 피처에 적용
insta_raw['content'] = insta_raw['content'].apply(lambda x : text_cleaning(x))

insta_raw.head()
```

### 1.2.4 카프카로 보내기
```python
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
```
---
### 1.2.5 분석
```python
from konlpy.corpus import kolaw
from konlpy.tag import Okt
import nltk

okt = Okt()
ko = nltk.Text(insta_raw['content'])

stopword = ['', ' ', '      ']

ko = [i for i in ko if i not in stopword]
# nouns 는 게시글 별 단어 추출
nouns = []

for i in range(len(ko)):
    nouns.append(okt.nouns(ko[i]))
    
nouns = [i for i in nouns if i not in stopword]

# 추출한 전체 단어를 하나의 리스트로 통합
nounse = []

for i in range(len(nouns)):
    for j in range(len(nouns[i])):
        nounse.append(nouns[i][j])
from collections import Counter
count = Counter(nounse)
common_tags = count.most_common()

# nounse 데이터를 dataframe 형태로 변경
most_food = pd.DataFrame(common_tags, columns=['단어','횟수'])
#most_food
----
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

# 음식 종류 및 카테고리 분류 파일 불러오기
food_df = pd.read_csv('./Food_Dictionary_csv.csv', encoding='cp949')

food = food_df[food_df['음식명'].isin(i for i in nounse)]

# nounse 데이터프레임과 음식카테고리 merge
food_nouns = pd.merge(most_food, food, how="inner", left_on='단어', right_on='음식명')
food_nouns
food_nouns = food_nouns.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
food_nouns
#food_nouns.json.dumps(food_n, ensure_ascii=False)
food_nouns = food_nouns.to_json(orient = 'records')

```

```python
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

#Open API 검색 요청 개체 설정
request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

#검색 요청 및 처리
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
# import sys
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
# from flask import jsonify
import re

# Naver API 요청
client_id = #ID
client_secret = #SECRET

url = "https://openapi.naver.com/v1/search/local"
lm = "수내 떡볶이 맛집"
query = "?query="+urllib.parse.quote(lm)+"&sort=random&display=3&start=1"
url_query = url + query
#Open API 검색 요청 개체 설정
request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
#검색 요청 및 처리
response = urllib.request.urlopen(request)
rescode = response.getcode()
remove_tag = re.compile('<.*?>')
res = response.read().decode('utf-8')
json_response = json.loads(res)
json_response
