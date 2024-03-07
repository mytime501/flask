from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import datetime
app = Flask(__name__)


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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        global useridnow
        useridnow = request.form.get("useridnow")
        userpwnow = request.form.get("userpwnow")
        result = db.whostudy.find_one({'userid':useridnow, 'userpw':userpwnow})
        if result != None:
            return redirect("attendance")
        else:
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
            return render_template("join.html")
        elif len(str(userid)) != 7:
            return render_template("join.html")
        elif userpw != userpwc:
            return render_template("join.html")
        elif len(str(usernumb)) != 11:
            return render_template("join.html")
        else:
            db.whostudy.insert_one({'userid': userid, 'userpw': userpw, 'username': username, 'usernumb': usernumb, 'playd': playd})
            return redirect('/')
    
@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    if request.method == 'GET':
        return render_template("attendance.html")
    else:
        check1 = request.form.get("check1")
        if check1 == None:
            check1 = False
        else:
            check1 = True
        print(check1)
        if check1 == True:
            now = datetime.datetime.now()
            nowtime = now.strftime("%Y{} %m{} %d{} %H{} %M{} %S{}")
            nowtime = nowtime.format('년','월','일','시','분','초')
            db.whostudycheck.insert_one({'userid': "test", 'nowtime': nowtime})
            return redirect('/')
        else:
            return render_template("attendance.html")


if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)
    
