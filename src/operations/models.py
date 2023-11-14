from sqlalchemy import Table, Column, Integer, String, DateTime, TIMESTAMP, MetaData
#from src.database import metadata
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