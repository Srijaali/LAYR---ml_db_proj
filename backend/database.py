from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Example: update with your own credentials
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rija123@localhost:5432/fashion_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)