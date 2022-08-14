# Import all the models, so that Base has them before being
# imported by Alembic
from app.infra.database.basemodel import Base  # noqa F401
from app.models.api_user import APIUser  # noqa F401
from app.models.cashback import CashbackCriterio  # noqa F401
from app.models.compra import Compra  # noqa F401
from app.models.revendedor import Revendedor  # noqa F401
