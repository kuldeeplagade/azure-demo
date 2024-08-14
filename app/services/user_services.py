from app.models.schema import UserCreate
from app.models.models import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, Path, Depends

from app.database.db import SessionLocal
from app.utils.logger import logger

#for password hashing and token 
import app.auth.authentication as _auth
auth_handler=_auth.AuthHandler()

class UserServices:
    @staticmethod
    def sv_create_user(db: Session, user: UserCreate):
        """
        This function is used to create new user. It takes in user data and creates a new user.
        """
        try:
            existing_user = db.query(UserModel).filter(UserModel.contact_number == user.contact_number).first()
            
            if existing_user:
                logger.info("User already exists")
                raise HTTPException(status_code=400, detail="User Already exists")
            
            new_user = UserModel(
                username=user.username,
                email=user.email,
                password=auth_handler.get_password_hash(user.password),
                contact_number=user.contact_number,
                address=user.address
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
            
        except HTTPException as he:
            logger.error(f"HTTPException: {he.detail}")
            raise he
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise HTTPException(status_code=400, detail=str(e))
            
            
    @staticmethod      
    def sv_get_all_users(db: Session, skip: int = 0, limit: int = 10) -> dict:
        total_count = db.query(UserModel).count()
        users = db.query(UserModel).offset(skip).limit(limit).all()
        return {
            "users": users,
            "total_count": total_count
    }