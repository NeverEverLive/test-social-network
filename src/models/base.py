from contextlib import asynccontextmanager
from contextlib import contextmanager
from typing import AsyncContextManager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin

from src.settings import async_postgres_settings
from src.settings import postgres_settings


Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin):
    """Postgres base model"""

    __abstract__ = True
    pass


@asynccontextmanager
async def get_async_session() -> AsyncContextManager[AsyncSession]:
    engine = create_async_engine(async_postgres_settings.get_url())
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


@contextmanager
def get_session() -> ContextManager[Session]:
    engine = create_engine(postgres_settings.get_url())
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def set_session():
    """Создать сессию"""
    engine = create_engine(postgres_settings.get_url())
    db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
    BaseModel.set_session(db_session)
    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)
