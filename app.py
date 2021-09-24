from jrnl import Journals
import psycopg2
from postgresdb import pgconn
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
dbf = r"/Users/plasma/Documents/Code/docs/journal.db"


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
    return render_template("create.html")

@app.route("/make",methods=["POST"])
def make():
    _id = request.form.get("id")
    author =request.form.get("author")
    emotion = request.form.get("emotion")
    weather=request.form.get("weather")
    content = request.form.get("content")
    date=request.form.get("date")
    conn = pgconn()
    cur = conn.cursor()
    cur.execute('INSERT INTO entrys (author,emotion,weather,content,date)VALUES(%s,%s,%s,%s,%s)',(author,emotion,weather,content,date))
    # Problem: Author is seperate table
    connection.commit()
    return redirect("view.html")


@app.route("/view")
def view():
    conn = pgconn()
    cur = conn.cursor()
    cur.execute(
        "select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id"

    )
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
    cur.execute("DELETE from journals WHERE id=?", (str(id),))
    connection.commit()
    return redirect("/list")
