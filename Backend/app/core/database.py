from app.core.sql_connection import get_sql_connection
from fastapi import HTTPException

def get_db():
    conn = get_sql_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        yield conn
    finally:
        conn.close()