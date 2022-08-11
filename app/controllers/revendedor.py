from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_db
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.services.revendedor import RevendedorService

router = APIRouter()


@router.post("/", response_model=RevendedorOut)
def create_revendedor(revendedor_in: RevendedorIn, db: Session = Depends(get_db)):
    service = RevendedorService(db)

    return service.create(revendedor_in)
