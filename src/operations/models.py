from sqlalchemy import Table, Column, Integer, String, DateTime, TIMESTAMP, MetaData
#from src.database import metadata
from src.database import Base
metadata = MetaData()

operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP, nullable=True),
    Column("type", String),
)
class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True)
    quantity = Column( String)
    figi = Column( String)
    instrument_type = Column( String, nullable=True)
    date = Column( TIMESTAMP, nullable=True)
    type = Column( String)