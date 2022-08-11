import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.infra.database.basemodel import Base
from app.infra.settings import settings


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
