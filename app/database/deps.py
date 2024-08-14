from app.database.db import SessionLocal
from fastapi import Depends, HTTPException, Header, status
from jose import JWTError
import app.auth.authentication as _auth
auth_handler = _auth.AuthHandler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
