from fastapi import APIRouter, HTTPException, status
from typing import List
from src.core.dependency import db_dependency, user_dependency
from src.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from src.services import category_service
from src.core.security import check_user
import logging

router = APIRouter(
    prefix='/categories',
    tags=['Categories']    
)

@router.get('/{category_id}', summary='GET Category by ID', response_model=CategoryResponse)
def get_category(category_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_category = category_service.read_category(db, category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
        return db_category
    except Exception as e:
        logging.error(f'Error reading category: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.get('/', summary='GET ALL Categories', response_model=List[CategoryResponse])
def get_categories(db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        categories = category_service.read_categories(db)
        return categories
    except Exception as e:
        logging.error(f'Error reading categories: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.post('/', summary='CREATE new Category', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_category = category_service.create_category(db, category)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error creating category')
        return db_category
    except Exception as e:
        logging.error(f'Error creating category: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.put('/{category_id}', summary='UPDATE Category by ID', response_model=CategoryResponse)
def update_category(category_id: int, category_data: CategoryUpdate, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_category = category_service.update_category(db, category_id, category_data)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating category')
        return db_category
    except Exception as e:
        logging.error(f'Error updating category: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.delete('/{category_id}', summary='DELETE Category by ID', response_model=CategoryResponse)
def delete_category(category_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_category = category_service.delete_category(db, category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error deleting category')
        return db_category
    except Exception as e:
        logging.error(f'Error deleting category: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
