## Stay: in
좋은 숙박 시설을 찾아보자!
좋은 여행 숙박 시설을 찾고 싶을 때 사용해봐요!

항해 99 1주차 프로젝트 


![title copy](https://user-images.githubusercontent.com/79959576/167782935-2f9cdb42-6cc0-4571-b9dd-4bc8716e70e2.png)


## 제작기간 
22.05.09(월) ~ 22.05.12(목)

## 팀원 및 역할 분담
```
조장 이은총
Role
```
```
조원 박민수
Role 호텔등록 메인페이지 UI 및 서버api 제작
```
```
조원 박세열
Role 세부 리뷰 페이지 총괄 및 데이터 베이스 관리
```
## 프로젝트 소개


<hr>

## 1. 개발 환경

* 운영체제 : Windows, mac
* 개발 도구 : pycharm, visual studio code
* 개발 언어 : html, python
* 데이터베이스 : MongoDB

## 2. 기능 요약 설명
* 회원가입/로그인을 통한 계정 정보 저장 및 관리
* 회원가입 후 로그인으로 메인페이지에서 호텔 설명 카드 열람
* 상세 리뷰 버튼으로 상세 리뷰 페이지 이동하여 호텔에 대한 여러 코멘트들 열람 가능
* 마음에 드는 코멘트에 좋아요를 표시하여 좋아요 집계 가능
* 로그인으로 받은 토큰이 없다면 로그인 페이지 이외의 타 페이지 강제 이동 불가능

## 3. 데이터베이스 구조
![image](https://user-images.githubusercontent.com/79959576/167780696-03502869-1c8d-48b4-870a-65438e718e2a.png)


### hotel 데이터베이스
호텔의 전체적인 데이터들을 저장하는 데이터베이스
* __hotel_id__\
호텔이 생성될 때 할당 받는 아이디
* __name__\
호텔 이름
* __hotel rate__\
호텔이 몇성급인지 보여주는 인스턴스
* __hotel address__\
호텔 주소

<hr>

### user 데이터베이스
회원가입한 사용자의 데이터들을 저장하는 데이터베이스
* __user id__\
사용자의 아이디
* __password__\
사용자의 패스워드
* __nickname__\
사용자의 닉네임

<hr>

### comment 데이터베이스
호텔의 id와 유저의 id를 이용해 누가 어느 호텔에 코멘트를 달았는지 볼 수 있는 데이터베이스
* __comment id__\
코멘트가 생성될 때 자체적으로 생기는 아이디
* __comment rate__\
사용자가 코멘트를 작성할 때 매기는 별점
* __nickname__\
사용자의 닉네임
* __hotel_id__\
호텔이 생성될 때 할당 받는 아이디


<hr>

### Likes 데이터베이스
누가 무슨 코멘트를 좋아요를 했는지 알 수 있는 데이터베이스
* __likes id__\
좋아요가 생성될 때 자체적으로 생기는 아이디
* __comment id__\
코멘트가 생성될 때 자체적으로 생기는 아이디
* __nickname__\
사용자의 닉네임

## 4. 기능 구현

### 이은총
### login.html 및 해당 서버 기능 app.py




### 박민수
### main.html 및 해당 서버 기능 app.py
<img width="1921" alt="image" src="https://user-images.githubusercontent.com/95006095/167842528-f9d03306-80f6-42c5-9d84-3bfb92083c6d.png">

서버측 코드
```
@app.route('/main')
def info():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        hotel_list = list(db.hotel.find({}, {'_id': False}))
        reviewer = payload["user_id"]
        return render_template('main.html', rows=hotel_list, user_id=reviewer)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))
```
* 페이지로 들어 올 때 로그인유효성 검사를 위해 쿠키에서 토큰정보를 확인 후 통과시 등록되어있는 호텔데이터와 본인의 아이디정보를 가지고 메인페이지로보내주고 토큰정보가 없거나 유효하지않다면 로그인페이지로 돌아간다.
* 데이터베이스에 등록되어 있는 호텔정보를 Jinja2언어로 클라이언트에서 받기 위해 이동시에 파라메터로 보내준다.
* 클라이언트 측에서 작성자 본인이 아니면 삭제버튼이 안보이게 하기위해 본인의 아이디 정보를 파라메터로 보내준다.
```
@app.route("/info", methods=["POST"])
def hotel_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        hotel_list = list(db.hotel.find({}))
        try:
            if hotel_list[-1]["hotel_id"] is None:
                count = 0
            else:
                count = hotel_list[-1]["hotel_id"] + 1
        except(IndexError):
            print("에러")
            count = 0
        reviewer = payload["user_id"]
        hotel_image_receive = request.form['url_give']
        hotel_rate_receive = request.form['star_give']
        name_receive = request.form['title_give']
        address_receive = request.form['hotel_address_give']

        doc = {
            'hotel_image':hotel_image_receive,
            'hotel_rate':hotel_rate_receive,
            'name':name_receive,
            'address':address_receive,
            'hotel_id': count,
            'reviewer' : reviewer
        }
        db.hotel.insert_one(doc)
        return jsonify({'msg':'등록 완료'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))

```
* 호텔등록코드부분, 이전코드와 마찬가지로 토큰으로 유효성검사를하고 데이터베이스의 호텔id와 중복되지 않게 id를 할당하고 클라이언트 측에서 보내준 입력데이터를 포스팅한다.
```
@app.route("/info/delete", methods=["POST"])
def hotel_delete():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        reviewer = payload["user_id"]
        hotel_id_receive = request.form['hotel_id_give']
        card_info = db.hotel.find_one({'hotel_id':int(hotel_id_receive)})
        card_reviewer = card_info['reviewer']
        if reviewer == card_reviewer:
            db.hotel.delete_one({'hotel_id':int(hotel_id_receive)})
            return jsonify({'msg':'삭제 완료'})
        else:
            return jsonify({'msg':'작성자만 삭제가능합니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))
```
* 포스팅 삭제를 위한 서버코드, 마찬가지로 로그인이 되어있는지 검사하고 본인이 등록한 호텔데이터인지 확인후 삭제한다.


```
function to_review(hotel_id) {
        let hotel_num = hotel_id;
        window.location.href = "/reviews?num=" + hotel_num;
      }
```
* 호텔카드마다 붙어있는 버튼을 누를 시 호텔아이디를 가지고 리뷰페이지로 넘어가기 위한 클라이언트 코드.
```
 function posting() {
        let url = $("#url").val();
        let star = $("#star").val();
        let title = $("#title").val();
        let hotel_address = $("#address").val();

        $.ajax({
          type: "POST",
          url: "/info",
          data: {
            url_give: url,
            star_give: star,
            title_give: title,
            hotel_address_give: hotel_address,
          },
          success: function (response) {
            alert(response["msg"]);
            window.location.reload();
          },
        });
      }
```
*호텔 등록창에 입력한 데이터를 포스트 요청ajax코드를 사용하여 서버측으로 넘겨준다.
```
function delete_review(hotel_id) {
        $.ajax({
          type: "POST",
          url: "/info/delete",
          data: {
            hotel_id_give: hotel_id,
          },
          success: function (response) {
            alert(response["msg"]);
            window.location.reload();
          },
        });
      }
```
* 삭제할 호텔아이디를 서버측으로 넘겨주는 포스트요청ajax코드이다.

```
{% for row in rows %} {% set hotel_image = row['hotel_image'] %}
              {% set name = row['name'] %} {% set address = row['address'] %}
              {% set hotel_rate = row['hotel_rate'] %}
              {% set hotel_id = row['hotel_id'] %}
              {% set reviewer = row['reviewer'] %}
          {% set hotel_rate_image ="" %} 
              {% if hotel_rate == "1" %} 
                  {% set hotel_rate_image = "⭐" %} 
              {% elif hotel_rate == "2" %} 
                  {% set hotel_rate_image = "⭐⭐" %} 
              {% elif hotel_rate == "3" %} 
                  {% set hotel_rate_image = "⭐⭐⭐" %} 
              {% elif hotel_rate == "4" %} 
                  {% set hotel_rate_image = "⭐⭐⭐⭐" %} 
              {% elif hotel_rate == "5" %} 
                  {% set hotel_rate_image = "⭐⭐⭐⭐⭐" %} 
              {% endif %}
          <div class="col">
            <div class="card h-100">
              <img src="{{hotel_image}}" class="card-img-top" />
              <div class="card-body">
                <h5 class="card-title">{{name}}</h5>
                <p class="card-text">{{address}}</p>
                <p>{{hotel_rate_image}}</p>
                <p class="comment">
                  <button onclick="to_review({{hotel_id}})">상세리뷰</button>
                  {% if reviewer == user_id %}
                    <button onclick="delete_review({{ hotel_id }})">삭제</button>
                  {% endif %}
                </p>
              </div>
            </div>
          </div>
          {% endfor %}
```
* 서버측에서 넘겨준 파라메터 데이터를 Jinja2방식을 사용하여 포스팅카드로 나타내는 부분의 코드이다.


### 박세열
### reviews.html 및 해당 서버 기능 app.py
![image](https://user-images.githubusercontent.com/79959576/167813673-9f50021b-1ea5-43fe-bfaf-977c42bb7819.png)

코드의 길이 관계로 백엔드 서버 쪽과 자바스크립트 함수 부분만 설명하겠다.

```
@app.route('/reviews')
def reviews():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('reviews.html')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))
    except KeyError:
        return redirect(url_for("login"))
    except UnboundLocalError:
        return redirect(url_for("login"))
```
* 메인페이지에서 사용자가 토큰을 가지고 넘어오면 그것을 기반으로 "reviews.html"을 렌더해서 클라이언트한테 보내준다.

```
$(document).ready(function () {
        let getLink = window.location.search;
        let num = getLink.split("=")[1];
        get_posts();
      });
```
* 사용자는 토큰과 함께 메인페이지에서 num이라는 변수로 hotel_id를 가져온다. 이 hotel_id는 상세 리뷰에서 해당 호텔에 관련된 
  코멘트들만 불러모으기 위한 키 값으로 작용한다.
* 페이지 렌더시 기본적으로 작동이 되는 함수를 모아서 작동시킨다. 여기에 자바스크립트로 이루어진 get_posts함수를 담아 코멘트를 가지고 온다.

```
## get_posts.js 함수의 실행 전반부
function get_posts() {
        let getLink = window.location.search;
        let num = getLink.split("=")[1];
        $.ajax({
          type: "POST",
          url: "/get_posts",
          data: { hotel_id_give: num },//여기까지
```
* get_posts()함수에서 타입을 post로 data에 hotel_id를 담아 app.py 백엔드 서버에 보내준다. 이를 통해 벡엔드에서 해당 hotel_id와 
 연관이 있는 코멘트를 데이터베이스에서 서치한다.

```
@app.route("/get_posts", methods=['POST'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        hotel_id = request.form["hotel_id_give"]
        hotel_id_int = int(hotel_id)
        posts = list(db.comment.find({'hotel_id': hotel_id}).limit(20))#내림차순 20개 가져오기
        hotel = list(db.hotel.find({'hotel_id': hotel_id_int}))
        hotel_parse = [hotel[0]['name'],hotel[0]['hotel_image']]
        print("hotel:",hotel)
        for post in posts:
            post["_id"] = str(post["_id"])#고유값 이것을 항상 스트링으로 변경하기
            post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            post["heart_by_me"] = bool(db.likes.find_one({"post_id": post["_id"], "type": "heart", "username": payload['user_id']}))
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.","posts":posts,"hotel":hotel_parse})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))
    except KeyError:
        return redirect(url_for("login"))
    except UnboundLocalError:
        return redirect(url_for("login"))
```
* request.form으로 hotel_id를 받은 get_posts.py함수는 토큰 확인 후 hotel_id에 매치되는 코멘트를 posts에 담고 매치되는 
 호텔 이름과 이미지를 hotel에 담아 클라이언트로 보내준다. 이 때 likes 데이터 베이스와 연동하여 해당 코멘트가 가진 likes의 정보도 
 가져온다.
 
 ```
 ## get_posts.js 함수의 실행 후반부
 success: function (response) {
            if (response["result"] == "success") {
              let posts = response["posts"];
              let hotel = response["hotel"];
              let hotel_name = hotel[0];
              let hotel_image = hotel[1];
              let hotel_name_attach_temp = `...(코드 길이 관계상 생략)`;
              $("#hotel_nameCard").append(hotel_name_attach);
              for (let i = 0; i < posts.length; i++) {
                let post = posts[i];
                let star = posts[i]["comment_rate"];
                let star_image = "⭐".repeat(star);
                let class_heart = post["heart_by_me"] //삼항연산자
                  ? "fa-heart" //트루면
                  : "fa-heart-o"; //폴스면
                let count_heart = post["count_heart"];
                let html_temp = `...(코드 길이 관계상 생략)`
                $("#post-box").append(html_temp);}
 ```
 * 이후 response의 딕셔너리가 포함된 리스트 형태로 데이터를 가져오고 이 데이터들을 호텔 정보를 보여주는 템플릿과 코멘트들을 보여주는 
   템플릿들에 붙여 코멘트들은 for문을 돌리고 각각 append로 붙여서 클라이언트에게 보여준다. 또한 get_posts().py에서 계산된 좋아요 
   갯수를 코멘트 하단에 붙여서 보여준다.
   
```
function toggle_like(post_id, type) {
        console.log(post_id, type);
        let $a_like = $(`#${post_id} a[aria-label='heart']`);
        let $i_like = $a_like.find("i");
        if ($i_like.hasClass("fa-heart")) {
          $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
              post_id_give: post_id,
              type_give: type,
              action_give: "unlike",
            },
            success: function (response) {
              console.log("unlike");
              $i_like.addClass("fa-heart-o").removeClass("fa-heart");
              $a_like.find("span.like-num").text(num2str(response["count"]));
            },
          });
        } else {
          $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
              post_id_give: post_id,
              type_give: type,
              action_give: "like",
            },
            success: function (response) {
              console.log("like");
              $i_like.addClass("fa-heart").removeClass("fa-heart-o");
              $a_like.find("span.like-num").text(num2str(response["count"]));
            },
          });
        }
      }
```
* 사용자는 좋아요를 눌러 toggle_like.js 함수를 통해 서버 쪽에 눌렀다는 데이터를 보내는데 이 때 두 가지 경우가 생긴다. 사용자가 처음   좋아요를 눌러 코멘트에 긍정적인 표현을 하였을 때 addClass를 통해 긍정의 하트라는 클래스를 보여주고 한 번 더 눌러 사용자가 좋아요를   취소했을 때 취소당한 하트라고 표현하기 위해 addclass로 취소된 하트임을 보여주고 이 클릭에 대한 데이터를 서버에 보내준다.

```
@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            "nickname": user_info["nickname"],
            "type": type_receive
        }
        if action_receive =="like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))
    except KeyError:
        return redirect(url_for("login"))
    except UnboundLocalError:
        return redirect(url_for("login"))
```
* 좋아요를 눌렀다면 좋아요를 누른 사용자이므로 이에 대한 정보를 post로 서버에서 받아 likes 데이터베이스로 정보를 넘겨준다. 이 때 
  긍정의 좋아요 수를 카운팅하여 현재 코멘트가 얼마나 많은 좋아요를 받았는지 클라이언트에게 보여준다.
  
```
function post() {
        let getLink = window.location.search;
        let num = getLink.split("=")[1];
        let comment = $("#textarea-post").val();
        let comment_rate = $("#star").val();
        $.ajax({
          type: "POST",
          url: "/posting",
          data: {
            comment_give: comment,
            comment_rate_give: comment_rate,
            hotel_id_give: num,
          },
          success: function (response) {
            $("#modal-post").removeClass("is-active"); //모달을 닫는다.
            window.location.reload();
          },
        });
      }
```

* 사용자가 코멘트를 만들고 생성하기 버튼을 눌렀을 때 실행되며 post.js 함수로 코멘트의 내용과 평점, hotel_id를 서버로 넘겨준다.

```
@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        hotel_id = request.form["hotel_id_give"]
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        comment_receive = request.form["comment_give"]
        comment_rate = request.form["comment_rate_give"]
        hotel_id = request.form["hotel_id_give"]
        doc = {
            "nickname": user_info["nickname"],
            "hotel_id": hotel_id,
            "comment": comment_receive,
            "comment_rate": comment_rate
        }
        db.comment.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))
    except KeyError:
        return redirect(url_for("login"))
    except UnboundLocalError:
        return redirect(url_for("login"))
```
* 클라이언트에서 받은 데이터들을 comment 데이터 베이스로 저장하여 코멘트가 저장된다.
