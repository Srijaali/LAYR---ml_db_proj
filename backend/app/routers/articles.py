from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.articles import Article
from app.schemas.articles_schema import ArticleCreate, ArticleResponse
from typing import List
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import BIGINT

router = APIRouter()
@router.get("/", response_model=List[ArticleResponse])
def get_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Article)\
             .order_by(cast(Article.article_id, BIGINT).asc())\
             .offset(skip)\
             .limit(limit)\
             .all()

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: str, db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.article_id == article_id).first()

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(article_id: str, article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.article_id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="article not found")
    for key, value in article.dict().items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.post("/", response_model=str)
def add_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    return "Article added"

@router.delete("/{article_id}")
def delete_article(article_id: str, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.article_id == article_id).first()
    if not db_article:
        return {"error": "Article not found"}
    db.delete(db_article)
    db.commit()
    return "Deleted successfully"
