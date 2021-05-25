from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import cv2
from flask import Flask, render_template, Response
import pymysql
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


config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '0000',
    'database': 'mydb',
    'charset': 'utf8'
}

app = Flask(__name__)

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@blueprint.route('/index')
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@blueprint.route('/capture')
def capture():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:

            cv2.imwrite('temp/exmaple_raw.jpg', frame)
            camera.release()

            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

            # 이미지 로드 후 전처리
            img = cv2.imread('temp/exmaple_raw.jpg')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # 얼굴 감지해 잘라내어 저장
            imgNum = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
                cv2.imwrite('temp/exmaple_raw.jpg', cropped)

                imgNum += 1
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                gender = gender_model(cropped)
                age = age_model(cropped)
                emo = emotion_model(cropped)

                db = pymysql.connect(**config)

                cur = db.cursor()
                cur.execute("INSERT INTO user(age_segment, emotion, sex) values (%s, %s, %s)", [age, emo, gender])

                db.commit()

                cur.close()
                db.close()

            return redirect('recommend.html')

@blueprint.route('/user')
def user():
    return render_template('page-user.html', segment='index')

@blueprint.route('/recommend')
def recommend():
    return render_template('recommend.html', segment='index')

@blueprint.route('/order')
def order():
    return render_template('order.html', segment='index')

@blueprint.route('/pay')
def pay():
    return render_template('pay.html', segment='index')


@blueprint.route('/menu')
def menu():
    db = pymysql.connect(**config)

    cur = db.cursor()
    query = '''SELECT store_id, menu_name, menu_price, menu_img FROM menu'''
    cur.execute(query)
    rows = cur.fetchall()
    data_list = []
    for row in rows:
        data_dic = {
            'store_id': row[0],
            'menu_name': row[1],
            'menu_price': row[2],
            'menu_img': row[3]
        }
        data_list.append(data_dic)
    cur.close()
    db.close()

    return render_template('menu.html', segment='index', data_list=data_list)

# @blueprint.route('/add_cart', methods=['POST'])
# def add_cart():
#     print('-------------------------------------')
#     value = request.form['메뉴명']
#     print('-------------------------------------')
#     return value


@blueprint.route('/submit')
def submit():
    return render_template('submit.html', segment='index')

@blueprint.route('/<template>')
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None  
