from fastapi import APIRouter

from app.controllers import revendedor

api_router = APIRouter()

api_router.include_router(revendedor.router, prefix="/revendedor", tags=["revendedor"])
