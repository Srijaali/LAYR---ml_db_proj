from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Optional

# ----- Base schema for API response -----
class CustomerBase(BaseModel):
    customer_id: str
    age: int
    postal_code: str
    club_member_status: Optional[str]
    fashion_news_frequency: str
    active: bool
    first_name: str
    last_name: str
    email: str
    signup_date: datetime
    gender: str
    loyalty_score: Optional[Decimal]

    class Config:
        orm_mode = True

# ----- Schema for creating a customer -----
class CustomerCreate(BaseModel):
    customer_id: str
    age: int
    postal_code: str
    club_member_status: str
    fashion_news_frequency: str
    active: bool
    first_name: str
    last_name: str
    email: EmailStr

# ----- Schema for sending customer data in responses -----
class CustomerOut(CustomerBase):
    pass
