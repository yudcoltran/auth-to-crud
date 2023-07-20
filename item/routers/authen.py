from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated
from . import token

router = APIRouter(
    tags=["authentications"]
)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify(plain, hashed):
    return pwd_cxt.verify(plain, hashed)

def get_password_hash(password):
    return pwd_cxt.hash(password)

@router.post("/login")
async def login(request: Request, form: OAuth2PasswordRequestForm=Depends()):
    user = request.app.db["users"].find_one({
        'email': form.username
    })
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not exist')
    if not verify(form.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Incorrect username or password')
    access_token = token.create_access_token(
        data = {"sub": user["email"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

    