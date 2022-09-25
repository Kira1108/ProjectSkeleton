from http.client import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException,status

from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError

from typing import Optional
from datetime import datetime, timedelta

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY
from app.database import get_db
from app.crud import dbusers
 
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = 'HS256'
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = f"Cound not validate credentials.",
        headers = {"www-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = dbusers.get_user_by_username(db, username = username)

    if user is None:
        raise credential_exception

    return user