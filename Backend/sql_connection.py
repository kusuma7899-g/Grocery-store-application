import pymysql

def get_sql_connection():
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="Kusu78!!",
            database="grocerystore"
        )
        return conn
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        return None

