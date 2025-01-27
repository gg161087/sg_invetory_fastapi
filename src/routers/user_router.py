from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.dependency import db_dependency, user_dependency
from src.core.database import get_db
from src.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from src.models.user_model import User
from src.services import user_service
from src.core.security import check_user, bcrypt_context
import logging

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/{user_id}', summary='GET User by ID', response_model=UserResponse)
def get_user(user_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_user = user_service.read_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return db_user
    except Exception as e:
        logging.error(f'Error reading user: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.get('/', summary='GET ALL Users', response_model=List[UserResponse])
def get_users(db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 100):
    check_user(user)
    try:
        users = user_service.read_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        logging.error(f'Error reading users: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.post('/', summary='CREATE New User', response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user_data = User(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        password=bcrypt_context.hash(user_data.password),
        is_active=True
    )    
        db_user = user_service.create_user(db, user_data)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error creating user')
        return db_user
    except Exception as e:
        logging.error(f'Error creating user: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.put('/{user_id}', summary='UPDATE User by ID', response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_user = user_service.update_user(db, user_id, user_data)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating user')
        return db_user
    except Exception as e:
        logging.error(f'Error updating user: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.delete('/{user_id}', summary='DELETE user by ID', response_model=UserResponse)
def delete_user(user_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_user = user_service.delete_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error deleting user')
        return db_user
    except Exception as e:
        logging.error(f'Error deleting user: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')