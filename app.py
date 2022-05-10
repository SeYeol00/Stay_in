from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

import jwt
import datetime
import hashlib

from datetime import datetime, timedelta

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.qrhfi.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


SECRET_KEY = 'sparta'

# @app.route('/')
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#
#         return render_template('login.html')
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/')
def home():
        return render_template('login.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    user_id_receive = request.form['user_id_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': user_id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'user_id': user_id_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # .decode('utf-8')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    user_id_receive = request.form['user_id_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    print(user_id_receive,password_receive,nickname_receive)
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "user_id": user_id_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "nickname": nickname_receive                                # 닉네임
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_id_dup', methods=['POST'])
def check_id_dup():
    user_id_receive = request.form['user_id_give']
    print(user_id_receive)
    exists = bool(db.users.find_one({"user_id": user_id_receive}))
    print(exists)
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/check_nickname_dup', methods=['POST'])
def check_nickname_dup():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)