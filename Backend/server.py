from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sql_connection import get_sql_connection
from auth import authenticate_user, create_access_token, get_current_user
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

class UserRegister(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: UserRegister):
    from auth import pwd_context
    from user_dao import insert_user
    hashed = pwd_context.hash(user.password)
    insert_user(connection, user.username, hashed)
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(connection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}



# ---------------- Pydantic Model ----------------
class Product(BaseModel):
    product_name: str
    uom_id: int
    price_per_unit: float


# ---------------- Protected Routes ----------------
@app.get("/getUOM")
def get_uom(current_user: str = Depends(get_current_user)):
    try:
        return uom_dao.get_uoms(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getProducts")
def get_products(current_user: str = Depends(get_current_user)):
    try:
        return product_dao.get_all_products(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insertProduct")
def insert_product(product: Product, current_user: str = Depends(get_current_user)):
    try:
        product_id = product_dao.insert_new_product(connection, product.dict())
        return {"product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getAllOrders")
def get_all_orders(current_user: str = Depends(get_current_user)):
    try:
        return order_dao.get_all_orders(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deleteProduct")
def delete_product(product_id: int = Form(...), current_user: str = Depends(get_current_user)):
    try:
        return_id = product_dao.delete_product(connection, product_id)
        return {"product_id": return_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))