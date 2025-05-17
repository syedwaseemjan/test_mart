from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Creates a new product in the system.

    Args:
        product (schemas.ProductCreate): The product data to create.

    Returns:
        schemas.Product: The created product with its generated ID.

    Raises:
        HTTPException: 400 if the input data is invalid.
    """
    return ProductService(db).create_product(product)


@router.get("/", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves a paginated list of products.

    Args:
        skip (int): Number of records to skip (for pagination). Defaults to 0.
        limit (int): Maximum number of records to return. Defaults to 100.

    Returns:
        list[schemas.Product]: List of product objects.
    """
    return ProductService(db).get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific product by ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        schemas.Product: The requested product if found.

    Raises:
        HTTPException: 404 if the product is not found.
    """
    product = ProductService(db).get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
