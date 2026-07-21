from fastapi import APIRouter, Depends, HTTPException

import order_dao
from auth import get_current_user
from app.core.database import connection

router = APIRouter()

@router.get("/getAllOrders")
def get_all_orders(current_user: str = Depends(get_current_user)):
    try:
        return order_dao.get_all_orders(connection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))