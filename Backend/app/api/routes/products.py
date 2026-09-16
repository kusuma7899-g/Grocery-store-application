from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel

from app.dao import product_dao
from app.dao import uom_dao
from app.core.security import get_current_user
from app.core.database import get_db

router = APIRouter()

class Product(BaseModel):
    product_name: str
    uom_id: int
    price_per_unit: float

@router.get("/getUOM")
def get_uom(current_user: str = Depends(get_current_user), conn = Depends(get_db)):
    try:
        return uom_dao.get_uoms(conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getProducts")
def get_products(current_user: str = Depends(get_current_user), conn = Depends(get_db)):
    try:
        return product_dao.get_all_products(conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insertProduct")
def insert_product(
    product: Product,
    current_user: str = Depends(get_current_user),
    conn = Depends(get_db)
):
    try:
        product_id = product_dao.insert_new_product(conn, product.dict())
        return {"product_id": product_id}
    except Exception as e:
        raise