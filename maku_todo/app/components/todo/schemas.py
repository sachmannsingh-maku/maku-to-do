from .models import *

from pydantic import BaseModel

class TodoCreate(BaseModel):
    title:str
    description: str | None

class TodoUpdate(BaseModel):
    title:str
    description: str | None
    completed : bool

class TodoResponse(BaseModel):
    completed : bool
    title:str
    description: str | None
    
    class Config:
        from_attributes = True
    
    
    