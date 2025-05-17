from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", response_model=schemas.Inventory)
def add_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    """Adds new inventory record for a product.

    Args:
        inventory (schemas.InventoryCreate): Inventory data to create.

    Returns:
        schemas.Inventory: Created inventory record.

    Raises:
        HTTPException: 400 if product doesn't exist or invalid data.
    """
    return InventoryService(db).create_inventory(inventory)


@router.get("/", response_model=list[schemas.Inventory])
def list_inventory(db: Session = Depends(get_db)):
    """Retrieves complete inventory list.

    Returns:
        list[schemas.Inventory]: All inventory records.
    """
    return InventoryService(db).get_all_inventory()


@router.get("/low-stock", response_model=list[schemas.Inventory])
def get_low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    """Lists inventory items below stock threshold.

    Args:
        threshold (int): Minimum stock level threshold. Defaults to 10.
        db (Session): Database session dependency.

    Returns:
        list[schemas.Inventory]: Inventory items below threshold.
    """
    return InventoryService(db).get_low_stock(threshold)


@router.put("/{product_id}", response_model=schemas.Inventory)
def update_stock(product_id: int, data: schemas.InventoryBase, db: Session = Depends(get_db)):
    """Updates stock level for specific product.

    Args:
        product_id (int): ID of product to update.
        data (schemas.InventoryBase): New stock data.

    Returns:
        schemas.Inventory: Updated inventory record.

    Raises:
        HTTPException: 404 if inventory not found.
    """
    inventory = InventoryService(db).update_inventory_stock(product_id, data.stock)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory
