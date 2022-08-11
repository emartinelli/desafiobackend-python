from sqlalchemy.orm import Session

from app.models.revendedor import Revendedor as RevendedorModel
from app.schemas.revendedor import RevendedorIn, RevendedorOut


class RevendedorService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, revendedor: RevendedorIn) -> RevendedorOut:
        revendedor_model = RevendedorModel(
            cpf=revendedor.cpf,
            email=revendedor.email,
            nome_completo=revendedor.nome_completo,
            senha_com_hash=revendedor.senha,
        )

        self.db.add(revendedor_model)
        self.db.commit()
        self.db.refresh(revendedor_model)

        return RevendedorOut(
            nome_completo=revendedor_model.nome_completo,
            cpf=revendedor_model.cpf,
            email=revendedor_model.email,
        )
