import numpy as np
from tensorflow.keras.models import model_from_json
import cv2

def gender_model(img):
    # 전처리
    img = cv2.resize(img, dsize=(200, 200))
    img = img / 255.
    img = np.expand_dims(img, axis=0)

    # 모델 불러오기
    json_file = open('models/gender_R50V2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights('models/gender_R50V2.h5')

    # 예측값 산출
    prediction = model.predict(img)[0].tolist()[0]
    if prediction <= 0.5:
        result = 0
    else:
        result = 1

    return result


def age_model(img):
    # 전처리
    img = cv2.resize(img, dsize=(150, 150))
    img = img / 255.
    img = np.expand_dims(img, axis=0)

    # 모델 불러오기
    json_file = open('models/age_R101V2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights('models/age_R101V2.h5')

    # 예측값 산출
    label_text = [2, 3, 0, 1]
    # label_text = ['adult', 'senior', 'teen', 'young']
    predictions = model.predict(img)
    result = label_text[np.argmax(predictions[0])]

    return result

# 감정 모델
def emotion_model(img):
    # 전처리
    img = cv2.resize(img, dsize=(48, 48))
    img = img / 255.
    img = np.expand_dims(img, axis=0)

    # 모델 불러오기
    json_file = open('models/emotion_V16.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights('models/emotion_V16.h5')

    # 예측값 산출
    label_text = [2, 0, 1, 3]
    # label_text = ['angry', 'happy', 'neutral', 'sad']
    predictions = model.predict(img)
    result = label_text[np.argmax(predictions[0])]

    return result






