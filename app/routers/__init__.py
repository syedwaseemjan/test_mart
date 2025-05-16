from fastapi import APIRouter

from .inventory import router as inventory_router
from .products import router as product_router

api_router = APIRouter()
api_router.include_router(product_router)
api_router.include_router(inventory_router)
