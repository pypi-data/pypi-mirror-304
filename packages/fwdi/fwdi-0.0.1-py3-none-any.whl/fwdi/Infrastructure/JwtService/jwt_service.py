from datetime import datetime, timedelta, timezone
import logging
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError

from ...Abstractions.base_service import BaseService
from ...Domain.model_user import User
from ...Domain.token_data import TokenData
from ...Domain.user_in_db import UserInDB
from ...Persistence.manager_db_context import ManagerDbContext

logging.getLogger('passlib').setLevel(logging.ERROR)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JwtService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(plain_password, hashed_password):
        return JwtService.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return JwtService.pwd_context.hash(password)

    def get_user_by_username(db_context, username: str)-> UserInDB:
        user = [item for item in db_context if item['username'] == username]
        if len(user) > 0:
            user_dict = user[0]

            return UserInDB(**user_dict)

    def get_user_by_email(users_db:User, email: str)-> UserInDB:
        for user in users_db:
            if user.email == email:
                return UserInDB(**{
                        'username': user.username,
                        'hashed_password': user.hashed_password,
                        'email': user.email,
                        })

    def authenticate_user(db_context, username: str, password: str):
        user = JwtService.get_user_by_username(db_context, username)
        if not user:
            return False
        if not JwtService.verify_password(password, user.hashed_password):
            return False
        
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt

    async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            email: str = payload.get("email")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, username=username, email=email)

        except (InvalidTokenError, ValidationError):
            raise credentials_exception
        
        users_db = ManagerDbContext().get_metadata_user()
        user = JwtService.get_user_by_email(users_db, email=token_data.email)
        if user is None:
            raise credentials_exception
        
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
            
        return user
    
    async def get_current_active_user(current_user:User = Security(get_current_user),):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        return current_user