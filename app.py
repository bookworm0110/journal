import email
from gettext import find
from jrnl import Journals
from comment import Comments
import psycopg2
from postgresdb import pgconn
from flask import Flask, render_template, redirect, request, flash
import requests
import json
import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config["SECRET_KEY"]="top-secret"    

login_manager=LoginManager()
login_manager.init_app(app)

dbf = r"/Users/plasma/Documents/Code/docs/journal.db"
from user import User
# @app.route("/test")
def findUserByEmail(email):
    try:
        conn = pgconn()
        cur = conn.cursor()
        cur.execute("select * from users where email=%s",(email,))
        row=cur.fetchone()
        print(row)
        if row is None:
            return None
        else:
            usr=User(row[0], row[2], row[1], row[3], row[4])
            print('finduserbyemail',usr)
            return usr
    except Exception as e:
        print(e)

@app.route("/signup")
def signupview():
    return render_template("signup.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/signup",methods=["POST"])
def signup():

    name = request.form.get("name")
    email=request.form.get("email")
    pw=request.form.get("password")
    print(name+email+pw)

    user= findUserByEmail(email)
    if user is not None:
        flash("email is already registered! Meant to login? Go here: ")

        return redirect("/signup")
    else: 
        conn = pgconn()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name,email,password,role)VALUES(%s,%s,%s,%s)',(name, email, generate_password_hash(pw,method="sha256"),"member"))
        conn.commit()
        # Directions:
        # parse form element-DONE
        # check if email does not already exist in data
        # if true:
        # redirect back to signup page with alert
        # else:
        # add data to table
        # redirect to login
        return redirect("/login")

@app.route("/login")
def loginview():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    
    email=request.form.get("email")
    pw=request.form.get("password")
    user=findUserByEmail(email)
    if not user or check_password_hash(user.password, pw) == False:
        flash("Unable to login. Please check information and try again.")
        return redirect("/login")
    else:
        login_user(user, remember=False)
        print("loginfunction", user)

    #find user with said email
    #if password is wrong:
    #redirect to login with another alert
    #else:
    #set local/session variable to user
        return redirect("/profile")
@login_manager.user_loader
def load_user(user_id):
    
    user=findUserByEmail(user_id)

    print('loginuser',user)
    return user

@app.route("/admin")
@login_required
def admin():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute("select e.id,u.name as author,e.emotion,e.weather,e.content,e.date,e.private,u.id as authid from entrys as e, users as u where e.authorid=u.id")
    rows = cur.fetchall()
    print(rows)
    jnllist = []
    for row in rows:
        # jnl = Journals(row['id'], row['author'], row['emotion'],
        #    row['weather'], row['content'], row['date'])
        jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        jnllist.append(jnl)
    return render_template("adminpanel.html", jnllist=jnllist, user=current_user)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/")
def home():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute(
        "select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id"
    )
    rows = cur.fetchall()
    print(rows)
    return render_template("home.html", user=current_user)

@app.route("/create")
def create():
    day=time.strftime("%Y-%m-%d")
    key="06e3e0e2fe69d7f0caecadafc58c1a86"
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Coquitlam' + '&units=metric' + '&appid=' + key
    response=requests.get(url)
    data=json.loads(response.text)
    print(data)
    return render_template("create.html",day=day,weather=data["weather"][0]["main"], temperature=data["main"]["temp"], user=current_user)

@app.route("/make",methods=["POST"])
def make():
    emotion = request.form.get("emotion")
    author=current_user.id
    weather=request.form.get("weather")
    content = request.form.get("content")
    date=request.form.get("date")
    private=request.form.get("private")
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('INSERT INTO entrys (authorid,emotion,weather,content,date,private)VALUES(%s,%s,%s,%s,%s,%s)',(author,emotion,weather,content,date,private))
    conn.commit()
    return redirect("/view")

@app.route("/view")
def view():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute("select e.id,u.name as author,e.emotion,e.weather,e.content,e.date,e.private from entrys as e, users as u where e.authorid=u.id and e.private=false")
    rows = cur.fetchall()
    print(rows)
    jnllist = []
    for row in rows:
        jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        jnllist.append(jnl)
    return render_template("view.html", jnllist=jnllist, user=current_user)

@app.route('/myjournals')
def myjournals():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute("select e.id,u.name as author,e.emotion,e.weather,e.content,e.date,e.private,u.id from entrys as e, users as u where e.authorid=u.id and e.authorid=%s",(str(current_user.id),))
    rows = cur.fetchall()
    print(rows)
    jnllist = []
    for row in rows:
        jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        jnllist.append(jnl)
    return render_template("privateview.html", jnllist=jnllist, user=current_user)

@app.route('/update', methods=['POST'])
def update():
    _id = request.form.get("id")
    emotion = request.form.get("emotion")
    content = request.form.get("content")
    private = request.form.get("private")
    if private is None:
        private=False
    else:
        private=True
    conn = pgconn()
    print("private variable  ",private)
    cur = conn.cursor()
    cur.execute('UPDATE entrys SET emotion=%s, content=%s, private=%s WHERE id=%s',(emotion, content, private, _id))
    conn.commit()
    return redirect("/view")


@app.route('/edit/<int:id>')
def edit(id):
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('select e.id,u.name as author,e.emotion,e.weather,e.content,e.date,e.private from entrys as e, users as u where e.authorid=u.id', (str(id),))
    row = cur.fetchone()
    print(row)
    jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    print(jnl)
    return render_template("edit.html", jnl=jnl, user=current_user)


@app.route("/delete/<int:id>")
def delete(id):
    conn = pgconn()
    cur = conn.cursor()
    cur.execute("DELETE from entrys WHERE id=%s", (str(id),))
    conn.commit()
    return redirect("/view")
    
@app.route("/details/<int:id>")
def details(id):
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('select e.id,u.name as author,e.emotion,e.weather,e.content,e.date,e.private from entrys as e, users as u where e.authorid=u.id', (str(id),))
    row = cur.fetchone()
    print(row)
    jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    cur.execute('select c.id,c.date,c.entryid,c.content,c.author from comments as c where c.entryid=%s',(str(id),))
    rows = cur.fetchall()
    ctlist=[]
    for comment in rows:
        ct = Comments(comment[0], comment[1], comment[2], comment[3], comment[4])
        ctlist.append(ct)
        print(ct)
    return render_template("details.html", jnl=jnl, user=current_user)
@app.route("/weather")
def weatherapi():
    key="06e3e0e2fe69d7f0caecadafc58c1a86"
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Coquitlam' + '&units=metric' + '&appid=' + key
    response=requests.get(url)
    print(response.text)
    data=json.loads(response.text)
    print(data)
    return data["weather"][0]["description"]
@app.route("/addcomment", methods=["POST"])
def addcomment():
    date=datetime.now()
    entryid=request.form.get("journalid")
    content=request.form.get("content")
    author=current_user.name
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('INSERT INTO comments (date,entryid,content,author)VALUES(%s,%s,%s,%s)',(date, entryid, content, author))
    conn.commit()
    return redirect("/details/"+str(entryid))