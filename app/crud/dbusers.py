from email.policy import HTTP
from app.schemas import UserBase
from app.dbmodels import DbUser
from app.crud.hash import Hash

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_user(db:Session, request:UserBase):
    has_user = db.query(DbUser).filter(DbUser.username == request.username).first()

    if has_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT
        , detail = f"User with name {request.username} already exists.")

    user = DbUser(
        username = request.username, 
        password = Hash.bcrypt(request.password), 
        email = request.email)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db:Session):
    return db.query(DbUser).all()

def get_user(db:Session, id:int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} not found")
    return user

def get_user_by_username(db:Session, username:str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with username {username} not found")
    return user

def update_user(db:Session, id:int, request:UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)

    if not user.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} not found")

    user.update({ 
        DbUser.username : request.username, 
        DbUser.password : Hash.bcrypt(request.password), 
        DbUser.email : request.email}
    )
    db.commit()
    return "ok"

def delete_user(db:Session, id:int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return "ok"
