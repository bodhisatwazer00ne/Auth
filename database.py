import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

load_dotenv()
#Gets your PostgreSQL connection URL from .env.
DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(DATABASE_URL)
#engine is basically the connection mechanism between Python/SQLAlchemy and PostgreSQL.

#This creates a database session factory.
SessionLocal=sessionmaker(bind =engine, autocommit=False, autoflush=False)

#This is the base class from which your database models inherit.
class Base(DeclarativeBase):
    pass

#This creates a DB session for a request.
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()        
        
        
        
