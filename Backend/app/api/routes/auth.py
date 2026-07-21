from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.security import authenticate_user, create_access_token, pwd_context
from app.core.database import connection

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    from user_dao import insert_user
    hashed = pwd_context.hash(user.password)
    insert_user(connection, user.username, hashed)
    return {"message": "User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(connection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}