import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from src.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db():
    Base.metadata.create_all(bind=engine)
    while True:
        try:
            connection = engine.connect()
            connection.close()
            print('Conexión a la base de datos exitosa.')
            break
        except OperationalError:
            print('Esperando que la base de datos esté disponible...')
            time.sleep(5)