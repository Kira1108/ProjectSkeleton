from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import UserBase, UserDisplay
from app.database import get_db
from app.crud import dbusers
from app.auth.oauth2 import get_current_user

router = APIRouter(
  prefix='/user',
  tags=['user']
)

@router.post("/", response_model = UserDisplay)
def create_user(request:UserBase, db = Depends(get_db)):
    return dbusers.create_user(db, request)

@router.get("/all",response_model = List[UserDisplay])
def get_all_users(db:Session = Depends(get_db), current_user:UserBase = Depends(get_current_user)):
    return dbusers.get_all_users(db)

@router.get("/{id}", response_model = UserDisplay)
def get_user_by_id(id:int, db:Session = Depends(get_db)):
    return dbusers.get_user(db, id)

@router.post("/{id}/update")
def update_user(id:int, request:UserBase, db:Session = Depends(get_db)):
    return dbusers.update_user(db, id, request)

@router.post("/{id}/delete")
def delete_user(id:int, db:Session = Depends(get_db)):
    return dbusers.delete_user(db, id)