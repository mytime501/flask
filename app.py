from flask import Flask, render_template, request, redirect, flash, make_response
from pymongo import MongoClient
from datetime import timedelta, datetime, timezone
import gridfs
import jwt
import hashlib
import string
import random

app = Flask(__name__)
app.secret_key="My_Key"
SECRET_KEY = 'my_key'
client = MongoClient(
            host="mongodb://svc.sel5.cloudtype.app",
            port=30997,
            # replica=replica set
            username="admin",
            password="tmdwns0504"
            # authSource=auth database
        )
db = client['who'] ## db name


@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/home", methods=['GET','POST'])
def home():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template("home.html")
    except jwt.ExpiredSignatureError:
        flash("로그인 시간이 만료되었습니다.")
        return redirect("/login")
    except jwt.exceptions.DecodeError:
        flash("로그인 정보가 존재하지 않습니다.")
        return redirect("/login")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        #global useridnow
        useridnow = request.form["useridnow"]
        userpwnow = request.form["userpwnow"]

        userpw_hide=hashlib.sha256(userpwnow.encode('utf-8')).hexdigest()

        result = db.whostudy.find_one({'userid':useridnow, 'userpw':userpw_hide})
        if result != None:
            
            payload = {
            'id': useridnow,
            'exp': datetime.now(timezone(timedelta(hours=9))) + timedelta(minutes=5)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            resp = make_response(redirect("/home"))
            resp.set_cookie('mytoken', token)

            flash("{}님 로그인 되었습니다.".format(useridnow))
            return resp
        else:
            flash("ID와 PW를 확인하세요.")
            return render_template("login.html")
            
@app.route("/join", methods=['GET', 'POST'])
def join_in():
    if request.method == 'GET':
        return render_template("join.html")
    else:
        userid = request.form.get("userid")
        userpw = request.form.get("userpw")
        userpwc = request.form.get("userpwc")
        username = request.form.get("username")
        usernumb = request.form.get("usernumb")
        playd = request.form.get("play")

        if playd == None:
            playd = False
        else:
            playd = True
        
        reid = db.whostudy.find_one({'userid': userid})
        if reid != None:
            flash("중복된 ID입니다.")
            return render_template("join.html")
        elif len(str(userid)) != 9:
            flash("학번을 확인하세요.")
            return render_template("join.html")
        elif userpw != userpwc:
            flash("비밀번호가 다릅니다.")
            return render_template("join.html")
        elif len(str(usernumb)) != 11:
            flash("전화번호를 확인하세요.")
            return render_template("join.html")
        else:
            userpw_hide=hashlib.sha256(userpw.encode('utf-8')).hexdigest()
            db.whostudy.insert_one({'userid': userid, 'userpw': userpw_hide, 'username': username, 'usernumb': usernumb, 'playd': playd})
            return redirect('/')
    
@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    token_receive = request.cookies.get('mytoken')

    _LENGTH = 10
    string_pool = string.ascii_letters + string.digits
    security = ""


    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.whostudy.find_one({"userid": payload['id']})

        if request.method == 'GET':            
            for i in range(_LENGTH):
                security += random.choice(string_pool)

            global securitycode
            securitycode = security
            return render_template("attendance.html", value = security)
        else:
            security_code = request.form.get("security_code")

            if security_code == securitycode:
                now = datetime.now(timezone(timedelta(hours=9)))

                nowtime = now.strftime("%Y{} %m{} %d{} %H{} %M{} %S{}")
                nowtime = nowtime.format('년','월','일','시','분','초')
                nowday = now.strftime("%Y{} %m{} %d{}")
                nowday = nowday.format('년','월','일')
                
                img = request.files['image']

                todayattend = db.fs.files.find_one({"filename": payload['id'], "uploadDatenow": nowday})

                if todayattend == None:
                    fs = gridfs.GridFS(db)
                    fs.put(img, filename = user_info['userid'], uploadDatenow = nowday)
                    db.whostudycheck.insert_one({'userid': user_info['userid'], 'username': user_info['username'], 'nowtime': nowtime})
                    flash("출석되었습니다.")
                    return redirect('/home')
                else:
                    flash("이미 출석되었습니다.")
                    return redirect('/home')
            else:
                flash("인증키가 틀렸습니다.")
                return render_template("attendance.html", value = securitycode)
    except jwt.ExpiredSignatureError:
        flash("로그인 시간이 만료되었습니다.")
        return redirect("/login")
    except jwt.exceptions.DecodeError:
        flash("로그인 정보가 존재하지 않습니다.")
        return redirect("/login")

if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)
    
