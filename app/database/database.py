import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_models():
    try:
        from app.models.base_model import BaseModel
        from app.models.category_model import Category
        from app.models.inventory_item_model import InventoryItem
        from app.models.warehouse_model import Warehouse
        from app.models.stock_location_model import StockLocation
        from app.models.stock_movement_model import StockMovement
        from app.models.user_model import User
    except ImportError as e:
        print(f'Error al cargar los modelos: {e}')
        raise

def wait_for_db():
    load_models()
    while True:
        try:
            connection = engine.connect()
            connection.close()
            print('Conexión a la base de datos exitosa.')
            break
        except OperationalError:
            print('Esperando que la base de datos esté disponible...')
            time.sleep(5)
    Base.metadata.create_all(bind=engine)