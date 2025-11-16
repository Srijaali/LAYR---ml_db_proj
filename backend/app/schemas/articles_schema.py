from pydantic import BaseModel

class ArticleBase(BaseModel):
    article_id:str
    product_code: int
    prod_name: str
    product_type_name: str
    product_group_name: str
    graphical_appearance_name: str
    colour_group_name: str
    department_no: int
    department_name: str
    index_name: str
    index_group_name: str
    section_name: str
    garment_group_name: str
    detail_desc: str
    price: float
    stock: int
    category_id: int | None = None

class ArticleCreate(ArticleBase):
    article_id: str

class ArticleResponse(ArticleBase):
    article_id: str

    class Config:
        from_attributes = True
