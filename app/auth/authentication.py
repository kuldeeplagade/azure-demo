from argon2 import PasswordHasher
from jose import JWTError, jwt,ExpiredSignatureError, JWTError
from datetime import datetime, timedelta
import os
from fastapi import HTTPException, Depends, status, Header,Request
from functools import wraps
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.logger import logger

class AuthHandler:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SEC_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.user_access_token_ttl = 43200  # 30 days
        self.admin_access_token_ttl = 43200 # 30 days
        self.ph = PasswordHasher()  # Using argon2's PasswordHasher

    def get_password_hash(self, password: str) -> str:
        """
        Hash an MPIN using Argon2.
        Args:
            mpin (str): The MPIN to hash.
        Returns:
            str: The hashed MPIN.
        """
        return self.ph.hash(password)

    def verify_password(self, hashed_password: str, plain_password: str) -> bool:
        """
        Verify an MPIN against a hashed MPIN.
        Args:
            hashed_password (str): The hashed MPIN.
            plain_password (str): The plain MPIN.
        Returns:
            bool: True if the MPINs match, otherwise False.
        """
        try:
            return self.ph.verify(hashed_password, plain_password)
        except:
            return False