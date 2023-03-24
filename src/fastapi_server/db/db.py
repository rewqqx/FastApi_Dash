from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.fastapi_server.core.settings import settings

engine = create_engine(
    settings.connection_string
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
