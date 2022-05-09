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

@app.route('/main')
def info():
    return render_template('main.html')

@app.route('/reviews')
def review():
    return render_template('reviews.html')


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




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)