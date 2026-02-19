import os
from dotenv import load_dotenv
import pymysql

# Load environment variables
load_dotenv()

def get_sql_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        return None

