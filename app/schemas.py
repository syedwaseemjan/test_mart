from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: Annotated[str, Field(...)]
    category: Annotated[str, Field(...)]
    price: Annotated[Decimal, Field(...)]


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: Annotated[int, Field(...)]

    model_config = {"from_attributes": True}


class InventoryBase(BaseModel):
    stock: Annotated[int, Field(...)]


class InventoryCreate(InventoryBase):
    product_id: Annotated[int, Field(...)]


class Inventory(InventoryBase):
    id: Annotated[int, Field(...)]
    product_id: Annotated[int, Field(...)]
    last_updated: Annotated[datetime, Field(...)]

    model_config = {"from_attributes": True}


class InventoryUpdate(BaseModel):
    stock: int


class SaleBase(BaseModel):
    product_id: Annotated[int, Field(...)]
    quantity: Annotated[int, Field(...)]
    sale_date: Annotated[date, Field(...)]


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: Annotated[int, Field(...)]
    total_amount: Annotated[Decimal, Field(...)]

    model_config = {"from_attributes": True}
