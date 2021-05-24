from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import cv2
from flask import Flask, render_template, Response
import pymysql

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
            cv2.imwrite('temp/test.jpg', frame)
            camera.release()
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
