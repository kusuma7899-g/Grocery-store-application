from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sql_connection import get_sql_connection
import product_dao
import order_dao
import uom_dao

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = get_sql_connection()

# ---------------- Pydantic Model ----------------
class Product(BaseModel):
    product_name: str
    uom_id: int
    price_per_unit: float

# ---------------- APIs ----------------

@app.get("/getUOM")
def get_uom():
    try:
        return uom_dao.get_uoms(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getProducts")
def get_products():
    try:
        return product_dao.get_all_products(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/insertProduct")
def insert_product(product: Product):
    try:
        product_id = product_dao.insert_new_product(connection, product.dict())
        return {"product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getAllOrders")
def get_all_orders():
    try:
        return order_dao.get_all_orders(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/deleteProduct")
def delete_product(product_id: int = Form(...)):
    try:
        return_id = product_dao.delete_product(connection, product_id)
        return {"product_id": return_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
