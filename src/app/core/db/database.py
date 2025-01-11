from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

from src.app.core.config import settings

DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_SYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

local_session = sessionmaker(bind=engine, expire_on_commit=False)

def get_db():
    session = local_session()
    try:
        yield session
    finally:
        session.close()