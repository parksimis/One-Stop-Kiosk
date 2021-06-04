import numpy as np
import cv2
import requests
from bs4 import BeautifulSoup
import joblib
import pandas as pd
import json
from datetime import datetime
from tensorflow import keras

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

gender_dic = {0: '남자', 1: '여자'}

age_dic = {0: '청소년', 1:'청년', 2:'중장년', 3:'노년'}

emo_dic = {0: '행복', 1: '중립', 2:'분노', 3:'우울' }

def gender_model(img, model_name=None):
    # 전처리
    img = cv2.resize(img, dsize=(200, 200))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.
    img = np.expand_dims(img, axis=0)
    model_path = 'models/' + model_name
    model = keras.models.load_model(model_path)
    # model = keras.models.load_model('models/gender_V19.h5')

    # 예측값 산출
    result = model.predict_classes(img)[0].tolist()[0]
    # print(f'{model_name}의 예측 결과 : {gender_dic[result]}')
    return result


def age_model(img, model_name=None):
    # 전처리
    img = cv2.resize(img, dsize=(200, 200))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.
    img = np.expand_dims(img, axis=0)
    model_path = 'models/' + model_name
    model = keras.models.load_model(model_path)


    # 예측값 산출
    label_text = [2, 3, 0, 1]
    # label_text = ['adult', 'senior', 'teen', 'young']

    result = label_text[model.predict_classes(img)[0]]

    # print(f'{model_name}의 예측 결과 : {age_dic[result]}')

    return result


# 감정 모델
def emotion_model(img, model_name=None):
    # 전처리
    img = cv2.resize(img, dsize=(48, 48))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.
    img = np.expand_dims(img, axis=0)

    # 모델 불러오기
    model_path = 'models/' + model_name
    model = keras.models.load_model(model_path)

    # 예측값 산출
    label_text = [2, 0, 1, 3]  # label_text = ['angry', 'happy', 'neutral', 'sad']
    predictions = model.predict(img)
    result = label_text[np.argmax(predictions[0])]
    # print(f'{model_name}의 예측 결과 : {emo_dic[result]}')
    return result


def get_html(url='https://www.ventusky.com/ko/37.571;126.977'):
    '''
    url 주소를 입력 받아, html 페이지를 scrapping 하는 함수

    * Parameter
    param url : 원하는 페이지 url 주소

    * Output
    return html : 해당 주소의 html 페이지
    '''

    response = requests.get(url)
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def get_cloud_amount(soup):
    '''
    서울 지역의 현재 구름량을 확인해 결과를 반환하는 함수

    * Input
    weather_url : 연결되는 url

    * Output
    return : cloud:구름량
    '''

    for row in soup.select('.info_table')[2].select('tr'):
        if row.select('td')[0].text.strip() == '구름량':
            cloud = row.select('td')[1].text.strip().split()[0]

    cloud = int(cloud) / 10

    # 구름량 분류 기준
    if 0 <= cloud <= 5:
        return '맑음'
    elif 6 <= cloud <= 8:
        return '구름많음'
    elif 9 <= cloud <= 10:
        return '흐림'


def get_rainfall_amount(soup):
    '''
    서울 지역의 현재 온도를 확인해 결과를 반환하는 함수

    * Input
    param session : 연결되는 세선

    * Output
    return : rain:강수량
    '''

    rain = soup.select('.mesto-predpoved')[0].select('td')[0].select('span')[1].text.split()[0]

    # 강수량 분류 기준
    if float(rain) > 0:
        return '비옴'
    else:
        return '비안옴'


def get_weather(url):
    '''
        함수 병합
    '''
    soup = get_html(url)
    cloudy = get_cloud_amount(soup)
    rain = get_rainfall_amount(soup)

    return [cloudy, rain]


def fill_value(total_data):
    '''
    새로운 고객 데이터를 더미화 및 표준화
    '''

    data_d = pd.DataFrame(columns=['남자', '여자', '노년', '중장년', '청년', '청소년', '분노', '우울', '중립', '행복',
                                   '구름많음', '맑음', '흐림', '주말', '평일', '아침', '저녁', '점심', '비안옴', '비옴'],
                          index=['0']).fillna(0)

    # AI모델 결과값과 날씨 API 데이터 추가

    for i in total_data:
        data_d[total_data] = 1

    # 시간

    now = datetime.now()

    if now.hour >= 16 and now.hour <= 23:
        data_d["저녁"] = 1
    elif now.hour >= 11 and now.hour < 16:
        data_d["점심"] = 1
    else:
        data_d["아침"] = 1

    # 요일
    weekday = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
    week = weekday[now.weekday()]

    if week == "일" or week == "토":
        data_d["주말"] = 1
    else:
        data_d["평일"] = 1
    #     return data_d
    # 표준화 모델 불러오기
    sd = joblib.load('models/scalemodel.pkl')

    data_sd = pd.DataFrame(sd.transform(data_d))

    # 표준화 된 데이터 프레임 컬럼 rename
    data_sd.rename(columns={0: '남자', 1: '여자', 2: '노년', 3: '중장년', 4: '청년', 5: '청소년', 6: '분노', 7: '우울', 8: '중립',
                            9: '행복', 10: '구름많음', 11: '맑음', 12: '흐림', 13: '주말', 14: '평일', 15: '아침', 16: '저녁', 17: '점심',
                            18: "비안옴", 19: "비옴"}, inplace=True)

    return data_sd.iloc[0]


def cluster_result(customer_data):
    '''
    우리가 만든 kmean 모델 불러와서 가장 가까운 군집 판별
    '''
    # 군집모델 불러오기
    model = joblib.load('models/model.pkl')
    # 군집모델로 가까운 군집 색출
    cluster_value = model.predict(customer_data.values.reshape(1, -1))[0]

    return str(cluster_value)


def recomend_Top3(total_data):
    '''
    판별된 군집의 음식 top3 추천
    '''
    # 정의된 함수 불러오기
    customer_data = fill_value(total_data)
    cluster_value = cluster_result(customer_data)

    # 군집 label과 음식데이터 확률이 들어있는 dict 불러오기
    with open("models/recommend_group.json", "r", encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # top3 음식 반환
    return sorted(json_data['word'][cluster_value], key=lambda x: json_data['word'][cluster_value][x], reverse=True)[0:3], cluster_value

