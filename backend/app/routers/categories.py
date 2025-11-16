from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models.categories import Category
from app.schemas.categories_schema import CategoryCreate, CategoryOut

router = APIRouter()

@router.get("/", response_model=List[CategoryOut])
def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Category).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.category_id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/", response_model=CategoryOut)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if category.parent_category_id:
        parent = db.query(Category).filter(Category.category_id == category.parent_category_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category does not exist")

    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{id}", response_model=CategoryOut)
def update_category(id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.category_id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.parent_category_id:
        parent = db.query(Category).filter(Category.category_id == category.parent_category_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category does not exist")

    data = category.dict()
    if data.get("parent_category_id") == 0:
        data["parent_category_id"] = None  # avoid FK violation

    for key, value in data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.category_id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted successfully"}
