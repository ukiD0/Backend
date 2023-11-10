from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from src.database import Base


# Base: DeclarativeMeta = declarative_base()
# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     permissions = Column(String)

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    #utcnow хранит время по конкретному часовому поясу
    Column("registered_at", TIMESTAMP, default = datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True,nullable=True),
    Column("is_superuser",Boolean,default=False,nullable=False),
    Column("is_verified",Boolean,default=False, nullable=False),
)

#так рекомендует документация fastapi
class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)