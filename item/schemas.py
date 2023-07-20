from pydantic import BaseModel, Field
import uuid
from typing import Union, List

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    name: str
    email: str 
    password: str
    
    class Config:
        populate_by_name = True

class Item(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    name: str
    description: str | None = Field(default= None)
    class Config:
        populate_by_name = True
        
class UpdateItem(BaseModel):
    name: str | None = None
    description: str | None = None 

class ShowUser(BaseModel):
    name: str 
    email: str 
    items: List[Item] = []
    class Config:
        from_attributes = True

class ShowItem(BaseModel):
    name: str 
    description: str | None = None
    creator: ShowUser
    class Config: 
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
