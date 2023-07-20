from fastapi import APIRouter, Body, Depends, Request
from ..repos import user
from ..schemas import User, ShowUser
from typing import List
from .import oauth2


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.get("/", response_model=List[ShowUser])
async def get_all(request: Request):
    return user.get(request)

@router.post("/")
async def create_user(request: Request, cuser: User = Body(...), current_user: User = Depends(oauth2.get_current_user)):
    return user.create(request, cuser)

@router.get("/{id}", response_model=ShowUser)
async def show_user(id: str, request: Request):
    return user.show(id, request)

