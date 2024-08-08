from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    JSON,
    DateTime,
    ARRAY,
    Date
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base=declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username=Column(String, nullable=False)
    contact_number=Column(String,unique=True, nullable=False)
    email=Column(String,nullable=False)
    password=Column(String, nullable=False)
    address=Column(String, nullable=False)