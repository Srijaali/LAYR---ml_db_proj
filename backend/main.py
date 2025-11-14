from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import database_models
from . import models
from fastapi import Query
app = FastAPI()

# Allow React frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create tables
database_models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def greet():
    return "Welcome to ML-DB FastAPI backend!"


# ======================================================
# --------------------- ARTICLES -----------------------
# ======================================================
# ======================================================
# --------------------- ARTICLES -----------------------
# ======================================================
@app.get("/articles")
def get_all_articles(skip: int=Query(0,ge=0), limit: int=Query(100,le=1000),db: Session = Depends(get_db)):
    articles = db.query(database_models.Articles).offset(skip).limit(limit).all()
    return [
        {
            "article_id": a.article_id,
            "product_code": a.product_code,
            "prod_name": a.prod_name,
            "product_type_name": a.product_type_name,
            "product_group_name": a.product_group_name,
            "graphical_appearance_name": a.graphical_appearance_name,
            "colour_group_name": a.colour_group_name,
            "department_no": a.department_no,
            "department_name": a.department_name,
            "index_name": a.index_name,
            "index_group_name": a.index_group_name,
            "section_name": a.section_name,
            "garment_group_name": a.garment_group_name,
            "detail_desc": a.detail_desc,
            "price": a.price,
            "stock": a.stock,
            "category_id": a.category_id
        } for a in articles
    ]


@app.get("/articles/{id}")
def get_article(id: str, db: Session = Depends(get_db)):
    a = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if a:
        return {
            "article_id": a.article_id,
            "product_code": a.product_code,
            "prod_name": a.prod_name,
            "product_type_name": a.product_type_name,
            "product_group_name": a.product_group_name,
            "graphical_appearance_name": a.graphical_appearance_name,
            "colour_group_name": a.colour_group_name,
            "department_no": a.department_no,
            "department_name": a.department_name,
            "index_name": a.index_name,
            "index_group_name": a.index_group_name,
            "section_name": a.section_name,
            "garment_group_name": a.garment_group_name,
            "detail_desc": a.detail_desc,
            "price": a.price,
            "stock": a.stock,
            "category_id": a.category_id
        }
    return {"error": "Article not found."}



@app.post("/articles")
def add_article(article: models.Articles, db: Session = Depends(get_db)):
    db.add(database_models.Articles(**article.model_dump()))
    db.commit()
    return "Article added successfully."


@app.put("/articles/{id}")
def update_article(id: str, article: models.Articles, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if db_article:
        for key, value in article.model_dump().items():
            setattr(db_article, key, value)
        db.commit()
        return "Article updated successfully."
    return "Article not found."


@app.delete("/articles/{id}")
def delete_article(id: str, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
        return "Article deleted successfully."
    return "Article not found."


# ======================================================
# -------------------- CATEGORIES ----------------------
# ======================================================
@app.get("/categories")
def get_all_categories(skip: int=0 , limit: int=100 ,db: Session = Depends(get_db)):
    return db.query(database_models.Categories).offset(skip).limit(limit).all()


@app.post("/categories")
def add_category(category: models.Categories, db: Session = Depends(get_db)):
    db.add(database_models.Categories(**category.model_dump()))
    db.commit()
    return "Category added successfully."


@app.put("/categories/{id}")
def update_category(id: int, category: models.Categories, db: Session = Depends(get_db)):
    db_category = db.query(database_models.Categories).filter(database_models.Categories.category_id == id).first()
    if db_category:
        for key, value in category.model_dump().items():
            setattr(db_category, key, value)
        db.commit()
        return "Category updated successfully."
    return "Category not found."


@app.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = db.query(database_models.Categories).filter(database_models.Categories.category_id == id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return "Category deleted successfully."
    return "Category not found."


# ======================================================
# -------------------- CUSTOMERS -----------------------
# ======================================================
@app.get("/customers")
def get_all_customers(skip: int=0 , limit: int=100 ,db: Session = Depends(get_db)):
    return db.query(database_models.Customers).offset(skip).limit(limit).all()


@app.get("/customers/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if db_customer:
        return db_customer
    return "Customer not found."


@app.post("/customers")
def add_customer(customer: models.Customers, db: Session = Depends(get_db)):
    db.add(database_models.Customers(**customer.model_dump()))
    db.commit()
    return "Customer added successfully."


@app.put("/customers/{id}")
def update_customer(id: str, customer: models.Customers, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if db_customer:
        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        return "Customer updated successfully."
    return "Customer not found."


@app.delete("/customers/{id}")
def delete_customer(id: str, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return "Customer deleted successfully."
    return "Customer not found."


# ======================================================
# ---------------------- EVENTS ------------------------
# ======================================================
@app.get("/events")
def get_all_events(skip: int=0 , limit: int=100 ,db: Session = Depends(get_db)):
    return db.query(database_models.Events).offset(skip).limit(limit).all()


@app.post("/events")
def add_event(event: models.Events, db: Session = Depends(get_db)):
    db.add(database_models.Events(**event.model_dump()))
    db.commit()
    return "Event added successfully."


@app.put("/events/{id}")
def update_event(id: int, event: models.Events, db: Session = Depends(get_db)):
    db_event = db.query(database_models.Events).filter(database_models.Events.event_id == id).first()
    if db_event:
        for key, value in event.model_dump().items():
            setattr(db_event, key, value)
        db.commit()
        return "Event updated successfully."
    return "Event not found."


@app.delete("/events/{id}")
def delete_event(id: int, db: Session = Depends(get_db)):
    db_event = db.query(database_models.Events).filter(database_models.Events.event_id == id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return "Event deleted successfully."
    return "Event not found."


# ======================================================
# ---------------------- ORDERS ------------------------
# ======================================================
@app.get("/orders")
def get_all_orders(skip: int=0, limit: int=100,db: Session = Depends(get_db)):
    return db.query(database_models.Orders).offset(skip).limit(limit).all()


@app.post("/orders")
def add_order(order: models.Orders, db: Session = Depends(get_db)):
    db.add(database_models.Orders(**order.model_dump()))
    db.commit()
    return "Order added successfully."


@app.put("/orders/{id}")
def update_order(id: int, order: models.Orders, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Orders).filter(database_models.Orders.order_id == id).first()
    if db_order:
        for key, value in order.model_dump().items():
            setattr(db_order, key, value)
        db.commit()
        return "Order updated successfully."
    return "Order not found."


@app.delete("/orders/{id}")
def delete_order(id: int, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Orders).filter(database_models.Orders.order_id == id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return "Order deleted successfully."
    return "Order not found."


# ======================================================
# ------------------- ORDER ITEMS ----------------------
# ======================================================
@app.get("/order_items")
def get_all_order_items(skip: int=0, limit: int=100,db: Session = Depends(get_db)):
    return db.query(database_models.OrderItems).offset(skip).limit(limit).all()


@app.post("/order_items")
def add_order_item(order_item: models.OrderItems, db: Session = Depends(get_db)):
    db.add(database_models.OrderItems(**order_item.model_dump()))
    db.commit()
    return "Order item added successfully."


@app.put("/order_items/{id}")
def update_order_item(id: int, order_item: models.OrderItems, db: Session = Depends(get_db)):
    db_item = db.query(database_models.OrderItems).filter(database_models.OrderItems.order_item_id == id).first()
    if db_item:
        for key, value in order_item.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        return "Order item updated successfully."
    return "Order item not found."


@app.delete("/order_items/{id}")
def delete_order_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(database_models.OrderItems).filter(database_models.OrderItems.order_item_id == id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return "Order item deleted successfully."
    return "Order item not found."


# ======================================================
# ---------------------- REVIEWS -----------------------
# ======================================================
@app.get("/reviews")
def get_all_reviews(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return db.query(database_models.Reviews).offset(skip).limit(limit).all()


@app.post("/reviews")
def add_review(review: models.Reviews, db: Session = Depends(get_db)):
    db.add(database_models.Reviews(**review.model_dump()))
    db.commit()
    return "Review added successfully."


@app.put("/reviews/{id}")
def update_review(id: int, review: models.Reviews, db: Session = Depends(get_db)):
    db_review = db.query(database_models.Reviews).filter(database_models.Reviews.review_id == id).first()
    if db_review:
        for key, value in review.model_dump().items():
            setattr(db_review, key, value)
        db.commit()
        return "Review updated successfully."
    return "Review not found."


@app.delete("/reviews/{id}")
def delete_review(id: int, db: Session = Depends(get_db)):
    db_review = db.query(database_models.Reviews).filter(database_models.Reviews.review_id == id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return "Review deleted successfully."
    return "Review not found."


# ======================================================
# ------------------- TRANSACTIONS ---------------------
# ======================================================
@app.get("/transactions")
def get_all_transactions(skip: int=0, limit: int=100,db: Session = Depends(get_db)):
    return db.query(database_models.Transactions).offset(skip).limit(limit).all()


@app.post("/transactions")
def add_transaction(transaction: models.Transactions, db: Session = Depends(get_db)):
    db.add(database_models.Transactions(**transaction.model_dump()))
    db.commit()
    return "Transaction added successfully."


@app.put("/transactions/{id}")
def update_transaction(id: int, transaction: models.Transactions, db: Session = Depends(get_db)):
    db_transaction = db.query(database_models.Transactions).filter(database_models.Transactions.transaction_id == id).first()
    if db_transaction:
        for key, value in transaction.model_dump().items():
            setattr(db_transaction, key, value)
        db.commit()
        return "Transaction updated successfully."
    return "Transaction not found."


@app.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(database_models.Transactions).filter(database_models.Transactions.transaction_id == id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return "Transaction deleted successfully."
    return "Transaction not found."