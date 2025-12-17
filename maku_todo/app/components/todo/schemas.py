from .models import *

from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    title:str
    description: str | None

class TodoUpdate(BaseModel):
    title:Optional[str] = None
    description: Optional[str] = None
    completed : Optional[str] = None

class TodoResponse(BaseModel):
    id:int
    completed : bool
    title:str
    description: str | None
    
    class Config:
        from_attributes = True
    
    
    