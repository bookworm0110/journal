from jrnl import Journals
import psycopg2
from postgresdb import pgconn
from flask import Flask, render_template, redirect, request
import requests
import json
import time
app = Flask(__name__)
dbf = r"/Users/plasma/Documents/Code/docs/journal.db"
from user import User
# @app.route("/test")
def findUserByEmail():
    try:
        email="people@email.net"
        conn = pgconn()
        cur = conn.cursor()
        cur.execute("select * from users where email=%s",(email,))
        row=cur.fetchone()
        print(row)
        if row is None:
            return None
        else:
            usr=User(row[0], row[1], row[2], row[3])
            print(usr)
            return usr
    except Exception as e:
        print(e)

@app.route("/signup")
def signupview():
    return render_template("signup.html")
@app.route("/logout")
def logout():
    return redirect("/")


@app.route("/signup",methods=["POST"])
def signup():
    return redirect("/login")

@app.route("/login")
def loginview():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    return redirect("/")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/")
def home():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute(
        "select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id"
    )
    rows = cur.fetchall()
    print(rows)
    return render_template("home.html")


@app.route("/create")
def create():
    day=time.strftime("%Y-%m-%d")
    key="06e3e0e2fe69d7f0caecadafc58c1a86"
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Coquitlam' + '&units=metric' + '&appid=' + key
    response=requests.get(url)
    data=json.loads(response.text)
    print(data)
    return render_template("create.html",day=day,weather=data["weather"][0]["main"], temperature=data["main"]["temp"])

@app.route("/make",methods=["POST"])
def make():
    emotion = request.form.get("emotion")
    author=1
    weather=request.form.get("weather")
    content = request.form.get("content")
    date=request.form.get("date")
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('INSERT INTO entrys (authorid,emotion,weather,content,date)VALUES(%s,%s,%s,%s,%s)',(author,emotion,weather,content,date))
    # Problem: Author is seperate table
    conn.commit()
    return redirect("/view")


@app.route("/view")
def view():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute("select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id")
    rows = cur.fetchall()
    print(rows)
    jnllist = []
    for row in rows:
        # jnl = Journals(row['id'], row['author'], row['emotion'],
        #    row['weather'], row['content'], row['date'])
        jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5])
        jnllist.append(jnl)
    return render_template("view.html", jnllist=jnllist)


@app.route('/update', methods=['POST'])
def update():
    _id = request.form.get("id")
    emotion = request.form.get("emotion")
    content = request.form.get("content")
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('UPDATE entrys SET emotion=%s, content=%s WHERE id=%s',(emotion, content, _id))
    conn.commit()
    return redirect("/view")


@app.route('/edit/<int:id>')
def edit(id):
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id', (str(id),))
    row = cur.fetchone()
    print(row)
    jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5])
    print(jnl)
    return render_template("edit.html", jnl=jnl)


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
    cur.execute('select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id', (str(id),))
    row = cur.fetchone()
    print(row)
    jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5])
    print(jnl)
    return render_template("details.html", jnl=jnl)
@app.route("/weather")
def weatherapi():
    key="06e3e0e2fe69d7f0caecadafc58c1a86"
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Coquitlam' + '&units=metric' + '&appid=' + key
    response=requests.get(url)
    print(response.text)
    data=json.loads(response.text)
    print(data)
    return data["weather"][0]["description"]