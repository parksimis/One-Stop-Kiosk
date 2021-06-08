import numpy as np
from tensorflow.keras.models import model_from_json
import cv2

################
###image crop###
################

face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')

# 이미지 로드 후 전처리
img = cv2.imread('example_raw.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3,5)

# 얼굴 감지해 잘라내어 저장
imgNum = 0
for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)
    cropped = img[y - int(h/4):y + h + int(h/4), x - int(w/4):x + w + int(w/4)]
    cv2.imwrite("example" + str(imgNum) + ".jpg", cropped)
    imgNum += 1
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_casecade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh),(0,255,0),2)


###################
###input AImodel###
###################

# 성별 모델(전처리-모델 불러오기-예측값 산출)
def gender_model(img):
  img = cv2.resize(img, dsize = (200,200))
  img = img / 255.
  img = np.expand_dims(img, axis = 0)
  
  json_file = open('models/gender_R50V2.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  model = model_from_json(loaded_model_json)
  model.load_weights('models/gender_R50V2.h5')
  
  prediction = model.predict(img)[0].tolist()[0]
  if prediction <= 0.5:
    result = '남자'
  else : 
    result = '여자'

  return result

# 연령 모델(전처리-모델 불러오기-예측값 산출)
def age_model(img):
  img = cv2.resize(img, dsize = (150,150))
  img = img / 255.
  img = np.expand_dims(img, axis = 0)
  
  json_file = open('models/age_R101V2.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  model = model_from_json(loaded_model_json)
  model.load_weights('models/age_R101V2.h5')
  
  label_text = ['adult','senior','teen','young']
  predictions = model.predict(img)
  result = label_text[np.argmax(predictions[0])]
  
  return result

# 감정 모델(전처리-모델 불러오기-예측값 산출)
def emotion_model(img):
  img = cv2.resize(img, dsize = (48,48))
  img = img / 255.
  img = np.expand_dims(img, axis = 0)
  
  json_file = open('models/emotion_V16.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  model = model_from_json(loaded_model_json)
  model.load_weights('models/emotion_V16.h5')
  
  label_text = ['angry','happy','neutral','sad']
  predictions = model.predict(img)
  result = label_text[np.argmax(predictions[0])]
  
  return result