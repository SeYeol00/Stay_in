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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)