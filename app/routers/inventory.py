from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", response_model=schemas.Inventory)
def add_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return InventoryService(db).create_inventory(inventory)


@router.get("/", response_model=list[schemas.Inventory])
def list_inventory(db: Session = Depends(get_db)):
    return InventoryService(db).get_all_inventory()


@router.get("/low-stock", response_model=list[schemas.Inventory])
def get_low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    return InventoryService(db).get_low_stock(threshold)


@router.put("/{product_id}", response_model=schemas.Inventory)
def update_stock(
    product_id: int, data: schemas.InventoryBase, db: Session = Depends(get_db)
):
    inventory = InventoryService(db).update_inventory_stock(product_id, data.stock)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory
