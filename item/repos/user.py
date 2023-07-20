from fastapi import Request, Body, Response, status, HTTPException
from ..schemas import User, ShowUser
from fastapi.encoders import jsonable_encoder
from typing import List
from passlib.context import CryptContext
from .. routers import authen

def create(request: Request, cuser: User = Body(...)):
    
    cuser.password = authen.get_password_hash(cuser.password)
    user = jsonable_encoder(cuser)
    check_flag = request.app.db["users"].find_one({"email": user["email"]})
    if check_flag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User email is already exist')
    try:
        new_user = request.app.db["users"].insert_one(user)
        create_user = request.app.db["users"].find_one(
            {"_id": new_user.inserted_id}
        )
        return {'msg': '', 'code': 1, 'data': create_user}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User id is already exist')

def get(request: Request):
    users = request.app.db["users"].find()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found') 
    # return {'msg':'', 'code': 1, 'data': list(users)}
    return list(users)

def show(id: str,request: Request):
    user = request.app.db["users"].find_one(
        {"_id": id}
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found') 
    # return {'msg':'', 'code': 1, 'data': user}
    return user
