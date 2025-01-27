from sqlalchemy.orm import Session
from src.core.database import Base
from src.core.database import engine
from src.models.category_model import Category
from src.seeders.category_seed import CATEGORIES
from src.models.user_model import User
from src.seeders.user_seed import USERS

def load_seed_data():
    with Session(engine) as session:
        existing_categories = session.query(Category).count()
        if existing_categories == 0:
            session.bulk_insert_mappings(Category, CATEGORIES)
            session.commit()
            print(f'{len(CATEGORIES)} CATEGORIES inserted correctly.')
        else:
            print('The CATEGORIES data already exists, it will not be inserted again.')  

        existing_categories = session.query(User).count()
        if existing_categories == 0:
            session.bulk_insert_mappings(User, USERS)
            session.commit()
            print(f'{len(USERS)} USERS inserted correctly.')
        else:
            print('The USERS data already exists, it will not be inserted again.')  

def create_tables():
    Base.metadata.create_all(bind=engine)
    load_seed_data()
