from app.home import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from jinja2 import TemplateNotFound
import cv2
from flask import Flask, render_template, Response
import engine, db_engine
import re
import base64
import boto3

gender_dic = {0: '남자', 1: '여자'}

age_dic = {0: '청소년', 1:'청년', 2:'중장년', 3:'노년'}

emo_dic = {0: '행복', 1: '중립', 2:'분노', 3:'우울' }

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '0000',
    'database': 'mydb',
    'charset': 'utf8'
}


app = Flask(__name__)



@blueprint.route('/index')
def index():
    return render_template('index.html', segment='index')

@blueprint.route('/user')
def user():
    return render_template('page-user.html', segment='index')


@blueprint.route('/upload_image', methods=['POST'])
def upload_image():

    json_data = request.get_data()
    decode_data = json_data.decode()
    image_data = re.sub('^data:image/.+;base64,', '', decode_data)
    imgdata = base64.b64decode(image_data)
    filename = './temp/example.jpg'

    with open(filename, 'wb') as f:
        f.write(imgdata)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    # 이미지 로드 후 전처리
    img = cv2.imread('./temp/example.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # 얼굴 감지해 잘라내어 저장
    imgNum = 0

    data = None
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]

        imgNum += 1
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        gender = engine.gender_model(cropped)
        age = engine.age_model(cropped)
        emo = engine.emotion_model(cropped)

        query = "INSERT INTO user(age_segment, emotion, sex, capture_chk) values (%s, %s, %s, 'Y')"
        values = [age, emo, gender]

        db_engine.execute_dml(query, values)

        weather = engine.get_weather('https://www.ventusky.com/ko/37.571;126.977')

        gender = gender_dic[gender]
        age = age_dic[age]
        emo = emo_dic[emo]

        test_data = [gender, age] + weather + [emo]

        result = engine.recomend_Top3(test_data)

        data = {'one': result[0],
                'two': result[1],
                'three': result[2]
                }

    return jsonify(result='success', result2=data)



@blueprint.route('/recommend')
def recommend():
    return render_template('recommend.html', segment='index')

@blueprint.route('/order')
def order():
    path = request.path
    query = '''
        SELECT C.cart_id, C.menu_name, M.menu_img, C.menu_qty, C.menu_price\
        FROM cart AS C JOIN menu AS M\
        ON C.menu_id = M.menu_id\
    '''
    rows = db_engine.select(query)

    cart_list = []
    for row in rows:
        data_dic = {
            'cart_id': row[0],
            'menu_name': row[1],
            'menu_img': row[2],
            'menu_qty': row[3],
            'menu_price': row[4]
        }
        cart_list.append(data_dic)
    return render_template('order.html', segment='index', cart_list=cart_list, path=path)

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


@blueprint.route('/menu', methods=['GET', 'POST'])
def menu():
    path = request.path
    cap_chk = 'false'
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

    if request.full_path.find('=') != -1:
        cap_chk = 'true'
        values = list(request.args.to_dict().values())
        query = '''
        SELECT menu_name, menu_price, menu_img FROM menu WHERE menu_name IN (%s, %s, %s)
        '''

        rows = db_engine.select(query, values)

        recom_list = []
        for row in rows:
            data_dic = {
                'menu_name': row[0],
                'menu_price': row[1],
                'menu_img': row[2],
            }
            recom_list.append(data_dic)

        return render_template('menu.html', segment='index', cart_list=cart_list, data_list=data_list, recom_list=recom_list, path=path, cap_chk=cap_chk)

    else:
        return render_template('menu.html', segment='index', cart_list=cart_list, data_list=data_list, path=path, cap_chk=cap_chk)

@blueprint.route('/reco_add_cart', methods=['POST'])
def reco_add_cart():
    if request.method == 'GET':
        return render_template('menu.html')

    elif request.method == 'POST':
        query = '''SELECT user_id FROM user WHERE capture_chk ="Y" ORDER BY CREATED_AT DESC LIMIT 1'''
        rows = db_engine.select(query)

        user_id = ''
        for row in rows:
            user_id = row[0]

        top_menu_list = request.form['top_slt_menu']

        query = '''
            SELECT store_id, menu_id, menu_name, menu_price 
            FROM menu
            WHERE menu_name = %s
        '''
        values = top_menu_list.split(',')

        input_query = '''
            INSERT INTO cart (store_id, menu_id, menu_name, menu_price, menu_qty, user_id)\
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        for value in values:
            rows = db_engine.select(query, value)
            for row in rows:
                input_values = list(row) + [1, user_id]
                db_engine.execute_dml(input_query, input_values)


        return redirect('/menu')

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
        menu_price = request.form['menu_price']
        menu_price = int(re.sub(r'[^0-9]+', '', menu_price)) * menu_qty

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

@blueprint.route('/delete', methods=['POST'])
def delete():

    if request.method == 'GET':
        return render_template('/menu')

    elif request.method == 'POST':
        path = request.form['path']
        cart_menu = request.form['cart_menu']
        query = 'DELETE FROM cart WHERE menu_name = %s'
        db_engine.execute_dml(query=query, values=[cart_menu])


        return redirect(path)


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
