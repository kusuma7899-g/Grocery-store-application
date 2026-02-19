from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from sql_connection import get_sql_connection
import product_dao
import order_dao
import uom_dao
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = get_sql_connection()

@app.get("/getUOM")
def get_uom():
    return uom_dao.get_uoms(connection)

@app.get("/getProducts")
def get_products():
    try:
        return product_dao.get_all_products(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insertProduct")
def insert_product(data: str = Form(...)):
    request_payload = json.loads(data)
    product_id = product_dao.insert_new_product(connection, request_payload)
    return {"product_id": product_id}

@app.post("/insertOrder")
def insert_order(data: str = Form(...)):
    payload = json.loads(data)
    order_id = order_dao.insert_order(connection, payload)
    return {"order_id": order_id}

@app.get("/getAllOrders")
def get_all_orders():
    return order_dao.get_all_orders(connection)

@app.post("/deleteProduct")
def delete_product(product_id: int = Form(...)):
    return_id = product_dao.delete_product(connection, product_id)
    return {"product_id": return_id}
