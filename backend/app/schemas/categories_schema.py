from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    parent_category_id: Optional[int] = None  # top-level categories have no parent

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True  # Pydantic v2
