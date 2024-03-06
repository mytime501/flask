from flask import Flask, render_template, request, redirect
app = Flask(__name__)    

@app.route("/")
def hello():
    return render_template("./hello.html")

@app.route("/login")
def login():
    return render_template("./login.html")

@app.route("/join", methods=['GET', 'POST'])
def join_in():
    if request.method == 'GET':
        return render_template("./join.html")
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
        
        if userpw != userpwc:
            return "비밀번호가 다릅니다."
        elif len(str(userid)) != 7:
            print(userid)
            return "학번을 확인하시오."
        elif len(str(usernumb)) != 11:
            return "전화번호를 확인하시오."
        else:
            return redirect('/')
    
@app.route("/attendance")
def attendance():
    return render_template("./attendance.html")

 
if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)
