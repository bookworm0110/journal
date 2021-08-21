import psycopg2
DB_URL = 'postgres://postgres:Go761204@localhost:5432/postgres'


def pgconn():
    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
    except Exception as e:
        print(e)
    return conn
