from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_db
from app.repository.revendedor import DuplicateRevendedorException
from app.schemas.revendedor import RevendedorIn, RevendedorOut
from app.services.revendedor import RevendedorService

router = APIRouter()


@router.post("/", response_model=RevendedorOut, status_code=201)
def create_revendedor(revendedor_in: RevendedorIn, db: Session = Depends(get_db)):
    service = RevendedorService(db)

    try:
        return service.create(revendedor_in)
    except DuplicateRevendedorException:
        raise HTTPException(status_code=422, detail="Revendedor já cadastrado")
