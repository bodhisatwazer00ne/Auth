from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class User(Base):
    __tablename__="users"
    #Create/use a PostgreSQL table called users.
    
    
    id:Mapped[int]=mapped_column(
        primary_key=True,   
    )
    username:Mapped[str]=mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    password_hash:Mapped[str]=mapped_column(
        String(255),
    )