from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.config.dependency import db_dependency, user_dependency
from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.controllers import user_controller

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/{user_id}', summary='GET User by ID', response_model=UserResponse)
def get_user(user_id: int, db: db_dependency, user: user_dependency):
    return user_controller.get_user(user_id, db, user)

@router.get('/', summary='GET ALL Users', response_model=List[UserResponse])
def get_users(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 100):
    return user_controller.get_users(db, user, skip, limit)

@router.post('/', summary='CREATE New User', response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(user_data, db)

@router.put('/{user_id}', summary='UPDATE User by ID', response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: db_dependency, user: user_dependency):
    return user_controller.update_user(user_id, user_data, db, user)

@router.delete('/{user_id}', summary='DELETE user by ID', response_model=UserResponse)
def delete_user(user_id: int, db: db_dependency, user: user_dependency):
    return user_controller.delete_user(user_id, db, user)