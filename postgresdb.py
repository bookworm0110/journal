import psycopg2
# DB_URL = 'postgres://postgres:Go761204@localhost:5432/postgres'

DB_URL = 'postgres://uguqaccpkekgpf:2aa052969770a6158d1c58873f0ec9f8853901e3a1ce6947d24cfb4ce55e838a@ec2-54-158-232-223.compute-1.amazonaws.com:5432/d5m6oa5s29nsp5'
def pgconn():
    conn = None
    try:
        conn = psycopg2.connect(DB_URL,sslmode='require')
    except Exception as e:
        print(e)
    return conn