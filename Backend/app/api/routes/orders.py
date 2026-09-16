from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from app.dao import order_dao
from app.core.security import get_current_user
from app.core.database import get_db

router = APIRouter()


class OrderDetail(BaseModel):
    product_id: int
    quantity: int
    total_price: float


class Order(BaseModel):
    customer_name: str
    grand_total: float
    order_details: List[OrderDetail]


@router.get("/getAllOrders")
def get_all_orders(
    current_user: str = Depends(get_current_user),
    conn = Depends(get_db)
):
    try:
        return order_dao.get_all_orders(conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insertOrder")
def insert_order(
    order: Order,
    current_user: str = Depends(get_current_user),
    conn = Depends(get_db)
):
    try:
        order_id = order_dao.insert_order(
            conn,
            order.model_dump()
        )

        return {
            "order_id": order_id,
            "message": "Order created successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))