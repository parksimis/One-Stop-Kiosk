from app.home import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from jinja2 import TemplateNotFound
import cv2
from flask import Flask, render_template, Response
import pymysql
import engine, db_engine, connection
import re
import base64
import boto3



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
            img = cv2.imread('temp/exmaple_raw.jpg')

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


                gender = engine.gender_model(cropped)
                age = engine.age_model(cropped)
                emo = engine.emotion_model(cropped)

                query = "INSERT INTO user(age_segment, emotion, sex) values (%s, %s, %s)"
                values = [age, emo, gender]

                db_engine.execute_dml(query, values)

            return redirect('recommend.html')

@blueprint.route('/user')
def user():
    return render_template('page-user.html', segment='index')


@blueprint.route('/upload_image', methods=['POST'])
def upload_image():

    json_data = request.get_data()
    decode_data = json_data.decode()
    image_data = re.sub('^data:image/.+;base64,', '', decode_data)
    imgdata = base64.b64decode(image_data)
    filename = './temp/some_image.jpg'

    with open(filename, 'wb') as f:
        f.write(imgdata)
    # s3 = connection.s3_connection()

    # bucket_name = 'yangjae-team01-s3'
    # s3.upload_file(filename, bucket_name, 'test_image.jpg')

    return jsonify(result="success")



@blueprint.route('/recommend')
def recommend():
    return render_template('recommend.html', segment='index')

@blueprint.route('/order')
def order():

    query = "SELECT cart_id, menu_name, menu_qty, menu_price FROM cart"
    rows = db_engine.select(query)

    cart_list = []
    for row in rows:
        data_dic = {
            'cart_id': row[0],
            'menu_name': row[1],
            'menu_qty': row[2],
            'menu_price': row[3]
        }
        cart_list.append(data_dic)
    return render_template('order.html', segment='index', cart_list=cart_list)

@blueprint.route('/pay')
def pay():
    return render_template('pay.html', segment='index')

@blueprint.route('/payment')
def payment():
    query = 'INSERT INTO orders(user_id, total_qty, total_price) SELECT user_id, SUM(menu_qty), SUM(menu_price) FROM cart;'
    db_engine.execute_dml(query, values=None)

    query = '''
            INSERT INTO order_details(order_id, user_id, menu_id, store_id, food_qty, food_price)\
            SELECT O.order_id, C.user_id, C.menu_id, C.store_id, C.menu_qty, C.menu_price\
            FROM orders AS O, cart AS C\
            WHERE O.user_id = C.user_id;
        '''
    db_engine.execute_dml(query, values=None)

    query = "TRUNCATE cart"
    db_engine.execute_dml(query=query, values=None)

    query = '''
        SELECT O.order_id, O.food_qty, O.food_price, M.menu_name
        FROM order_details AS O, menu AS M
        WHERE O.menu_id = M.menu_id 
        AND O.user_id = (SELECT MAX(user_id) FROM order_details)
    '''
    rows = db_engine.select(query)

    order_list = []
    for row in rows:
        data_dic = {
            'order_id': row[0],
            'food_qty': row[1],
            'food_price': row[2],
            'menu_name': row[3]
        }
        order_list.append(data_dic)

    return render_template('submit.html', segment='index', order_list=order_list)

@blueprint.route('/direct_menu')
def direct_menu():
    query = "INSERT INTO user(capture_chk) values (%s)"
    values = ['N']
    db_engine.execute_dml(query, values)

    return redirect('/menu')


@blueprint.route('/menu')
def menu():
    path = request.path
    query = "SELECT menu_name, menu_qty, menu_price FROM cart ORDER BY cart_id;"
    rows = db_engine.select(query)

    cart_list = []
    for row in rows:
        data_dic = {
            'menu_name': row[0],
            'menu_qty': row[1],
            'menu_price': row[2]
        }
        cart_list.append(data_dic)

    query = '''SELECT menu_id, store_id, menu_name, menu_price, menu_img FROM menu'''
    rows = db_engine.select(query)

    data_list = []
    for row in rows:
        data_dic = {
            'menu_id': row[0],
            'store_id': row[1],
            'menu_name': row[2],
            'menu_price': row[3],
            'menu_img': row[4]
        }
        data_list.append(data_dic)

    return render_template('menu.html', segment='index', cart_list=cart_list, data_list=data_list, path=path)

@blueprint.route('/add_cart', methods=['POST'])
def add_cart():

    if request.method == 'GET':
        return render_template('menu.html')

    elif request.method == 'POST':
        query = '''SELECT user_id FROM user ORDER BY CREATED_AT DESC LIMIT 1'''
        rows = db_engine.select(query)

        user_id = ''
        for row in rows:
            user_id = row[0]

        path = request.form['path']
        store_id = request.form['store_id']
        menu_id = int(request.form['menu_id'])
        menu_name = request.form['menu_name']
        menu_qty = int(request.form['menu_qty'])
        menu_price = int(request.form['menu_price']) * menu_qty

        query = "SELECT menu_id, menu_name, menu_qty, menu_price FROM cart"
        rows = db_engine.select(query).fetchall()

        if len(rows) == 0:
            up_query = '''
                    INSERT INTO cart (user_id, store_id, menu_id, menu_name, menu_qty, menu_price)\
                    SELECT %s, %s, %s, %s, %s, %s\
                    FROM DUAL\
                    WHERE NOT EXISTS (SELECT menu_id FROM cart WHERE menu_id = %s);
                    '''
            up_values = [user_id, store_id, menu_id, menu_name, menu_qty, menu_price, menu_id]
        else:
            for row in rows:
                if menu_id == row[0]:
                    menu_qty += int(row[2])
                    menu_price += int(row[3])

                    up_query = "UPDATE cart SET menu_qty = %s, menu_price = %s WHERE menu_id = %s"
                    up_values = [menu_qty, menu_price, row[0]]
                    db_engine.execute_dml(up_query, up_values)
                    break
                else:
                    # CART TABLE INSERT
                    up_query = '''
                            INSERT INTO cart (user_id, store_id, menu_id, menu_name, menu_qty, menu_price)\
                            SELECT %s, %s, %s, %s, %s, %s\
                            FROM DUAL\
                            WHERE NOT EXISTS (SELECT menu_id FROM cart WHERE menu_id = %s);
                    '''
                    up_values = [user_id, store_id, menu_id, menu_name, menu_qty, menu_price, menu_id]

        db_engine.execute_dml(up_query, up_values)

        return redirect(path)

@blueprint.route('/cancel')
def cancel():
    query = "TRUNCATE cart"
    db_engine.execute_dml(query=query, values=None)


    query = "DELETE FROM user WHERE user_id IN (SELECT max(user_id) FROM user);"

    db_engine.execute_ddl(query)

    return redirect('index.html')

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
