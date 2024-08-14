from fastapi import APIRouter, HTTPException, Depends, Path, Header
from app.database.db import SessionLocal
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated,Optional,List
from app.models.models import UserModel
from app.services.user_services import UserServices
from app.database.deps import get_db
from app.utils.logger import logger
from app.models.schema import (
    UserCreate,
    ResponseModel,
    UserResponse,
    PaginationResponse
)


router =APIRouter(prefix="/user", tags=["user"])
non_prefix_route=APIRouter(tags=["user"])

db_dependency= Annotated[Session, Depends(get_db)]

@router.post(
    "/register",
    response_model=ResponseModel[UserResponse],
    description="Register the new user in the system "
)
def register_user(user: UserCreate, db: db_dependency):
    try:
        user = UserServices.sv_create_user(db,user)
        logger.info("User registered successfully")
    
        return {
            "message": "User Registered successfully",
            "status" : "success",
            "status_code": status.HTTP_201_CREATED,
            "data": user,
        }
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/all", response_model=PaginationResponse[List[UserResponse]])
def get_all_dealers(db:db_dependency, page: Optional[int] = 1, limit: Optional[int] = 10):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page must be greater than 0")
    
    skip = (page - 1) * limit
    result = UserServices.sv_get_all_users(db, skip=skip, limit=limit)
    users = result["users"]
    total_count = result["total_count"]
    total_pages = (total_count + limit - 1) // limit  # Ceiling division

    return {
        "message": "User retrieved successfully",
        "status": "success",
        "status_code": status.HTTP_200_OK,
        "data": users,
        "current_page": page,
        "total_count": total_count,
        "total_pages": total_pages,
        "items_per_page": limit
    }