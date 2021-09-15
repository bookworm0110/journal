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
    nameform = request.form.get('name')
    emailform = request.form.get('email')
    phoneform = request.form.get('phone')
    fbform = request.form.get('fb')
    instform = request.form.get('inst')
    twform = request.form.get('tw')
    dcform = request.form.get('dc')
    print(nameform+' '+emailform+' '+phoneform+' ' +
          fbform+' '+instform+' '+twform+' '+dcform)
    # person=People("",nameform,emailform,phoneform,fbform,instform,twform,dcform)
    person = People(_id, nameform, emailform, phoneform,
                    fbform, instform, twform, dcform)

    connection = create(dbf)
    cur = connection.cursor()
    cur.execute('UPDATE people SET name=?,email = ?,phone = ?,facebook=?,twitter=?,instagram=?,discord=? WHERE id=?',
                (person.name, person.email, person.phone, person.facebook, person.instagram, person.twitter, person.discord, person.id))
    connection.commit()
    return redirect("/view")


@app.route('/edit/<int:id>')
def edit():
    connection = create(dbf)
    cur = connection.cursor()
    cur.execute('select e.id,u.name as author,e.emotion,e.weather,e.content,e.date from entrys as e, users as u where e.authorid=u.id', (str(id),))
    row = cur.fetchone()
    print(row)
    jnl = Journals(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    print(jnl)
    return render_template("edit.html", jnl=jnl)


@app.route("/delete/<int:id>")
def delete(id):
    conn = pgconn()
    cur = conn.cursor()
    cur.execute("DELETE from journals WHERE id=?", (str(id),))
    connection.commit()
    return redirect("/list")
