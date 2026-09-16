from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, products, orders
from app.core.sql_connection import get_sql_connection
from app.core.init_db import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup_conn = get_sql_connection()
create_tables(startup_conn)
startup_conn.close()

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)