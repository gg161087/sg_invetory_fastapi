from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.warehouse_schema import WarehouseCreate
from app.models.warehouse_model import Warehouse
import logging


def create_warehouse(db: Session, warehouse_data: WarehouseCreate):
    try:
        warehouse = Warehouse(**warehouse_data.dict())
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse
    except SQLAlchemyError as e:
        logging.error(f'Error creating warehouse: {e}')
        db.rollback()
        return None
