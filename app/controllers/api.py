from fastapi import APIRouter

from app.controllers import compra, revendedor

api_router = APIRouter()

api_router.include_router(revendedor.router, prefix="/revendedor", tags=["revendedor"])
api_router.include_router(compra.router, prefix="/compra", tags=["compra"])
