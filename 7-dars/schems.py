from pydantic import BaseModel
from typing import Optional
class CategoryCreate(BaseModel):
    name:str


class CategoryResponse(BaseModel):
    id:int
    class Config:
        from_attributes=True




class NewCreate(BaseModel):
    name:str
    title:str
    content:str
    image:Optional[str]=None
    video:Optional[str]=None
    author:str
class NewResponse(BaseModel):
    id:int
    class Config:
        from_attributes=True


