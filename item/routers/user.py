from fastapi import APIRouter, Body, Depends, Request
from ..repos import user
from ..schemas import User, ShowUser
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.get("/")
async def get_all(request: Request):
    return user.get(request)

@router.post("/")
async def create_user(request: Request, _user: User = Body(...)):
    return user.create(request, user=_user)

@router.get("/{id}")
async def show_user(id: str, request: Request):
    return user.show(id, request)

