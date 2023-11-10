from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID,SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from lance import datetime
from models import metadata, role
# from models.models import role
from sqlalchemy import *
from config import *

DATABASE_URL = f"postgresql+asyncpg://%{DB_USER}s:%{DB_PASS}s@%{DB_HOST}s:%{DB_PORT}s/%{DB_NAME}s"
Base: DeclarativeMeta = declarative_base()

class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column( String, nullable=False)
    username = Column( String, nullable=False)
    password = Column(String, nullable=False)
    #utcnow хранит время по конкретному часовому поясу
    Column("registered_at", TIMESTAMP, default = datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    hashed_password: str = Column(String(length=1024),nullable=False)
    is_active: bool = Column(Boolean,default=True,nullable=True)
    is_superuser: bool = Column(Boolean,default=False,nullable=False)
    is_verified: bool = Column(Boolean,default=False, nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)