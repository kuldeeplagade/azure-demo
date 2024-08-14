from pydantic import BaseModel, Field, validator, constr
from typing import Optional, Generic, TypeVar, Literal, List, Dict
from datetime import datetime, date

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    message: str
    status: str
    status_code: int
    data: Optional[T]

class PaginationResponse(BaseModel, Generic[T]):
    message: str
    status: str
    status_code: int
    data: Optional[T]
    current_page: Optional[int] = None
    total_count: Optional[int] = None
    total_pages: Optional[int] = None
    items_per_page: Optional[int] = None
    
class UserCreate(BaseModel):
    username : str
    email : str
    password : str = Field(min_length=6, max_length=6)
    contact_number : str = Field(min_length=10, max_length=10)
    address : str 
    
class UserResponse(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    password : Optional[str] = None
    contact_number : Optional[str] = None
    address : Optional[str] = None 