from fastapi import Body, HTTPException, Request, status, Response
from ..schemas import Item, UpdateItem
from fastapi.encoders import jsonable_encoder

def get(request: Request):
    items = request.app.db["items"].find()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found')
    return list(items)

def show(id: str, request: Request):
    item = request.app.db["items"].find_one({
        "_id": id
    })
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found')
    return item

def create(request: Request, citem: Item = Body(...)):
    item = jsonable_encoder(citem)
    check_flag = request.app.db["items"].find_one({"name": item["name"]})
    if check_flag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Item is already exist')
    try:
        new_item = request.app.db["items"].insert_one(item)
        create_item = request.app.db["items"].find_one(
            {"_id": new_item.inserted_id}
        )
        return {'msg': '', 'code': 1, 'data': create_item}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Item id is already exist')

def update(id: str, request: Request, uitem: UpdateItem = Body(...)):
    item = {k:v for (k, v) in uitem.model_dump().items() if v is not None}
    if len(item) >= 1:
        update_result = request.app.db["items"].update_one(
            {"_id": id}, {"$set": item}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found')
        updated_user = request.app.db["items"].find_one(
            {"_id": id}
        )
        return {'msg': '', 'code': 1, 'data': updated_user}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found')
    
def destroy(id: str, request: Request):
    item = request.app.db["items"].find_one(
        {"_id": id}
    )
    if not item: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found')
    delete_result = request.app.db["items"].delete_one(
        {"_id": id}
    )
    if delete_result.deleted_count == 1:
        return {'msg': 'Delete success', 'code': 1, 'data': ''}
    raise {'msg': 'Delete fail', 'code': 0, 'data': ''}
        
