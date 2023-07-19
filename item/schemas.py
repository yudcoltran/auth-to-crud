from pydantic import BaseModel, Field
import uuid
from typing import Union, List

class User(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    name: str
    email: str 
    passoword: str

class Item(BaseModel):
    name: str = Field(...)
    description: str | None = Field(default= None)
    
class ShowUser(BaseModel):
    name: str 
    email: str 
    items: List[Item] = []
    class Config:
        from_attributes = True

class ShowItem(BaseModel):
    name: str 
    description: str
    creator: ShowUser
    class Config: 
        from_attributes = True