from datetime import date

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: date
    type: str