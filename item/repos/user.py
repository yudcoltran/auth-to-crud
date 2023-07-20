from fastapi import APIRouter, Request, Body, Response, status, HTTPException
from passlib.context import CryptContext
from ..schemas import User, ShowUser
from fastapi.encoders import jsonable_encoder
from typing import List

# pwd_cxt = CryptContext(schema=["bcrypt"], deprecated="auto")

def create(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.db["users"].insert_one(user)
    create_user = request.app.db["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return {'msg': '', 'code': 1, 'data': create_user}

def get(request: Request):
    users = request.app.db["users"].find()
    # if not users:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found') 
    # return {'msg':'', 'code': 1, 'data': users}
    return users

def show(id: str,request: Request):
    user = request.app.db["users"].find_one(
        {"_id": id}
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found') 
    return {'msg':'', 'code': 1, 'data': user}
