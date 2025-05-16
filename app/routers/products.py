from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return ProductService(db).create_product(product)


@router.get("/", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProductService(db).get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService(db).get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
