from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.category_model import Category
from src.schemas.category_schema import CategoryCreate, CategoryUpdate
import logging

def create_category(db: Session, category:CategoryCreate):
    try:
        db_category = Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except SQLAlchemyError as e:
        logging.error(f'Error creating category: {e}')
        db.rollback()
        return None

def read_category(db: Session, category_id: int):
    try:
        return db.query(Category).filter(Category.id == category_id).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading category: {e}')
        return None

def read_categories(db: Session):
    try:
        return db.query(Category).all()
    except SQLAlchemyError as e:
        logging.error(f'Error reading categories: {e}')
        return None

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if db_category:
            for key, value in category.dict(exclude_unset=True).items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)
        return db_category
    except SQLAlchemyError as e:
        logging.error(f'Error updating category: {e}')
        db.rollback()
        return None    

def delete_category(db: Session, category_id: int):
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
        return db_category
    except SQLAlchemyError as e:
        logging.error(f'Error deleting category: {e}')
        db.rollback()
        return None    