from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
from sqlalchemy.exc import SQLAlchemyError
import logging

def create_user(db: Session, user: User):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        logging.error(f'Error creating user: {e}')
        return None

def read_user(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading user: {e}')
        return None
    
def read_user_by_username(db: Session, username: str):
    try:
        return db.query(User).filter(User.username == username).first()
    except SQLAlchemyError as e:
        logging.error(f'Error reading user: {e}')
        return None

def read_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logging.error(f'Error reading users: {e}')
        return None

def update_user(db: Session, user_id: int, user: User):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        logging.error(f'Error updating user: {e}')
        db.rollback()
        return None

def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
    except SQLAlchemyError as e:
        logging.error(f'Error deleting user: {e}')
        db.rollback()
        return None

