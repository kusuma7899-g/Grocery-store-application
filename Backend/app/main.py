from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, products, orders
from app.core.database import connection
from app.core.init_db import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables(connection)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)