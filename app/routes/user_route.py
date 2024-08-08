from fastapi import APIRouter, HTTPException, Depends, Path, Header
from app.database.db import SessionLocal
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from app.models.models import UserModel
from app.services.user_services import UserServices
from app.database.deps import get_db
from app.utils.logger import logger
from app.models.schema import (
    UserCreate,
    ResponseModel,
    UserResponse
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