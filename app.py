from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.qrhfi.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')


@app.route('/main')
def info():
    hotel_list = list(db.hotel.find({}, {'_id': False}))
    return render_template('main.html', rows=hotel_list)

@app.route("/info", methods=["POST"])
def hotel_post():
    hotel_list = list(db.hotel.find({}, {'_id': False}))
    count = len(hotel_list) + 1
    hotel_image_receive = request.form['url_give']
    hotel_rate_receive = request.form['star_give']
    name_receive = request.form['title_give']
    address_receive = request.form['hotel_address_give']

    doc = {
        'hotel_image':hotel_image_receive,
        'hotel_rate':hotel_rate_receive,
        'name':name_receive,
        'address':address_receive,
        'hotel_id': count
    }
    db.hotel.insert_one(doc)

    return jsonify({'msg':'등록 완료'})

@app.route("/info", methods=["GET"])
def hotel_get():
    hotel_list = list(db.hotel.find({}, {'_id': False}))
    return jsonify({'hotels': hotel_list})



#reviews
@app.route('/posting', methods=['POST'])
def posting():
    hotel_id = request.args.get("num")
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"user_id": payload["id"]})
        comment_receive = request.form["comment_give"]
        comment_rate = request.form["comment_rate"]
        doc = {
            "nickname": user_info["nickname"],
            "hotel_id": hotel_id,
            "comment": comment_receive,
            "comment_rate": comment_rate
        }
        db.comment.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/reviews"))


@app.route("/get_posts", methods=['GET'])
def get_posts():
    hotel_id = request.args.get("num")
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        posts = list(db.comment.find({'hotel_id': hotel_id}).limit(20))#내림차순 20개 가져오기
        for post in posts:
            post["_id"] = str(post["_id"])#고유값 이것을 항상 스트링으로 변경하기
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.","posts":posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/reviews"))




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)