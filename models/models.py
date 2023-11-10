from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer,Boolean, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()

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