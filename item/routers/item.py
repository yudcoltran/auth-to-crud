from fastapi import APIRouter, Body, Depends, HTTPException, Response, status, Request
from ..repos import item
from .import oauth2
from ..schemas import Item, ShowItem, UpdateItem, User
from typing import List

router = APIRouter (
    prefix="/item",
    tags=["Items"]
)

@router.get('/')
async def get_items(request: Request):
    return item.get(request)

@router.get('/{id}')
async def show_item(id: str, request: Request):
    return item.show(id, request)

@router.post('/')
async def create_item(request: Request, citem: Item = Body(...), current_user: User = Depends(oauth2.get_current_user)):
    return item.create(request, citem)

@router.put("/{id}")
async def update_item(id: str, request: Request, uitem: UpdateItem = Body(...), current_user: User = Depends(oauth2.get_current_user)):
    return item.update(id, request, uitem)

@router.delete("/{id}")
async def destroy_item(id: str, request: Request, current_user: User = Depends(oauth2.get_current_user)):
    return item.destroy(id, request)