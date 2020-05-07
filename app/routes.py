from flask import Flask, send_from_directory, render_template, session, redirect, url_for, request, make_response
from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")

db = client.user_database

app = Flask(__name__)
app.secret_key = b'=?????^y?+I??%/'


def check_user(nm, pwd):
    name = db.user_database.find_one({"name":nm})
    print(name)
    if name == None or name['pwd'] != pwd:
        return False
    return True


def add_user(nm, pwd):
    name = db.user_database.find_one({"name":nm})
    if name:
        return False
    db.user_database.insert({"name": nm, "pwd": pwd})
    return True


def check_extension(img):
    return '.' in img and img.rsplit ('.', 1)[1].lower() in {'jpeg','png','jpg'}


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if check_user(request.form['nm'], request.form['pwd']):
            session['username'] = request.form['nm']
            return redirect(url_for('cabinet'))
    if 'username' in session:
        return redirect(url_for('cabinet'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if add_user(request.form['nm'], request.form['pwd']):
            return redirect(url_for('cabinet'))
    if 'username' in session:
        return redirect(url_for('cabinet'))
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/cabinet')
def cabinet():
    if 'username' in session:
        return render_template('cabinet.html')
    return redirect(url_for('login'))

@app.route('/img/<path:img>')
def img(img):
    return send_from_directory('img/', img)

@app.route('/static/css/<string:css>')
def css(css):
    return send_from_directory('static/css/', css)

@app.route('/upload', methods=['POST'])
def upload():
    if 'img' not in request.files:
        return redirect(request.url)
    img = request.files['img']
    print(img)
    if img and check_extension(img.filename):
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload', img.filename))
        response = make_response(redirect(url_for('upload_img', img = img.filename)))
        return response

@app.route('/upload/<img>')
def upload_img(img):
	return send_from_directory('./upload/', img)



if __name__ == "__main__":
    app.run(threaded=True, port='5000')
