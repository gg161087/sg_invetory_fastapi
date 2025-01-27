from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from src.core.dependency import db_dependency, user_dependency
from src.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from src.services import product_service
from src.core.security import check_user
import logging

router = APIRouter(
    prefix='/products',
    tags=['Products']    
)

@router.get('/{product_id}', summary='GET Product by ID', response_model=ProductResponse)
def get_product(product_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_product = product_service.read_product(db, product_id)
        if db_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
        return db_product
    except Exception as e:
        logging.error(f'Error reading product: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
@router.get('/', summary='GET ALL Products', response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def get_products(user: user_dependency, db: db_dependency):
    skip: int = 0
    limit: int = 100
    check_user(user)
    try:
        products = product_service.read_products(db, skip=skip, limit=limit)
        return products
    except Exception as e:
        logging.error(f'Error reading products: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
@router.post('/', summary='CREATE new Product', status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: db_dependency, user: user_dependency):
    check_user(user)
    if product_service.read_product_by_sku(db, product.sku):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Product with SKU {product.sku} already exists')
    new_product = product_service.create_product(db, product)
    if not new_product:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to create product')
    return new_product

@router.put('/{product_id}', summary='UPDATE Product by ID', response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_product = product_service.update_product(db, product_id, product_data)
        if db_product is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error updating product')
        return db_product
    except Exception as e:
        logging.error(f'Error updating product: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
@router.put('/stock/{product_id}', summary='UPDATE Product Stock', status_code=status.HTTP_200_OK)
def update_product_stock(product_id: int, quantity: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        updated_product = product_service.update_product_stock(db, product_id, quantity)
        if not updated_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Product not found')
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

@router.delete('/{product_id}', summary='DELETE Product by ID', response_model=ProductResponse)
def delete_product(product_id: int, db: db_dependency, user: user_dependency):
    check_user(user)
    try:
        db_product = product_service.delete_product(db, product_id)
        if db_product is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error deleting product')
        return db_product
    except Exception as e:
        logging.error(f'Error deleting product: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')