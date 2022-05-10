from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import jwt
import datetime
import hashlib

import requests
from bs4 import BeautifulSoup

from datetime import datetime, timedelta

from pymongo import MongoClient
client = MongoClient('mongodb+srv://project:sparta@cluster1.mjh3x.mongodb.net/Cluster1?retryWrites=true&w=majority')
db = client.hotel

SECRET_KEY = 'sparta'

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
        print(token)
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

@app.route('/main')
def info():
    return render_template('main.html')

@app.route("/info", methods=["POST"])
def hotel_post():
    hotel_list = list(db.hotel.find({}, {'_id': False}))
    count = len(hotel_list) + 1
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    title_receive = request.form['title_give']
    hotel_address_receive = request.form['hotel_address_give']

    doc = {
        'url':url_receive,
        'star':star_receive,
        'title':title_receive,
        'hotel_address':hotel_address_receive,
        'num': count
    }
    db.hotel.insert_one(doc)

    return jsonify({'msg':'등록 완료'})

@app.route("/info", methods=["GET"])
def hotel_get():
    hotel_list = list(db.hotel.find({}, {'_id': False}))
    return jsonify({'hotels': hotel_list})

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)