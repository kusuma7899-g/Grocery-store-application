from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel

import product_dao
import uom_dao
from app.core.security import get_current_user
from app.core.database import connection

router = APIRouter()

class Product(BaseModel):
    product_name: str
    uom_id: int
    price_per_unit: float

@router.get("/getUOM")
def get_uom(current_user: str = Depends(get_current_user)):
    try:
        return uom_dao.get_uoms(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getProducts")
def get_products(current_user: str = Depends(get_current_user)):
    try:
        return product_dao.get_all_products(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insertProduct")
def insert_product(product: Product, current_user: str = Depends(get_current_user)):
    try:
        product_id = product_dao.insert_new_product(connection, product.dict())
        return {"product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deleteProduct")
def delete_product(product_id: int = Form(...), current_user: str = Depends(get_current_user)):
    try:
        return_id = product_dao.delete_product(connection, product_id)
        return {"product_id": return_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))