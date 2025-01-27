from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.product_model import Product
from src.schemas.product_schema import ProductCreate, ProductUpdate
import logging

def create_product(db: Session, product: ProductCreate):
    try:
        product_dict = product.dict()
        product_dict['initial_stock'] = product_dict.get('initial_stock', None)
        product_dict['current_stock'] = product_dict.get('current_stock', None)
        db_product = Product(**product_dict)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        logging.error(f'Error creating product: {e}')
        db.rollback()
        raise None

def read_product(db: Session, product_id: int):
    try:
        return db.query(Product).filter(Product.id == product_id).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading product: {e}')
        return None
    
def read_product_by_sku(db: Session, sku: str):
    try:
        return db.query(Product).filter(Product.sku == sku).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading product: {e}')
        return None

def read_products(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Product).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logging.error(f'Error reading products: {e}')
        return None

def update_product(db: Session, product_id: int, product: ProductUpdate):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise ValueError(f'Product with id {product_id} does not exist.')

        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        logging.error(f'Error updating product: {e}')
        db.rollback()
        return None
    
def update_product_stock(db: Session, product_id: int, quantity: int):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            if db_product.current_stock is None:
                db_product.current_stock = 0
            if db_product.current_stock + quantity < 0:
                raise ValueError('Insufficient stock')
            db_product.current_stock += quantity
            db.commit()
            db.refresh(db_product)
            return db_product
        return None
    except SQLAlchemyError as e:
        logging.error(f'Error updating product stock: {e}')
        db.rollback()
        return None

def delete_product(db: Session, product_id: int):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise ValueError(f'Product with id {product_id} does not exist.')

        db.delete(db_product)
        db.commit()
        return db_product
    except SQLAlchemyError as e:
        logging.error(f'Error deleting product: {e}')
        db.rollback()
        return None
