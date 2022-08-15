from decimal import Decimal

import pytest
from psycopg2.extras import NumericRange
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.infra.settings import settings
from app.models.cashback import CashbackCriterio


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

    yield engine

    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def cashback_criterios(db_session: Session) -> None:
    db_session.add_all(
        [
            CashbackCriterio(
                intervalo=NumericRange(Decimal("0"), Decimal("1000")),
                porcentagem_de_cashback=Decimal("0.10"),
            ),
            CashbackCriterio(
                intervalo=NumericRange(Decimal("1000"), Decimal("1500")),
                porcentagem_de_cashback=Decimal("0.10"),
            ),
            CashbackCriterio(
                intervalo=NumericRange(
                    Decimal("1500"),
                ),
                porcentagem_de_cashback=Decimal("0.10"),
            ),
        ]
    )
    db_session.commit()
