from fastapi import FastAPI, Request, status
from faker import Faker
from pydantic import BaseModel, Field

from datetime import datetime
from enum import Enum
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse


fake = Faker()

app = FastAPI(
    title="Trading App"
)

#показывает пользователю ошибки которые происходят на сервере
@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


fake_users = [
    {"id":0, "role":"admin", "name":fake.name()},   
    {"id":1, "role":"admin", "name":fake.name()},
    {"id":2, "role":"admin", "name":fake.name()},
    {"id":2, "created_at":"2020", "type_degree":"expert"},  
]

class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    create_at: datetime
    type_degree: str


class User(BaseModel):
    id:int
    role:int
    name:str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}",response_model=List[User])
def get_user(user_id:int):
#     for user in fake_users:
#         print(user)
#         if user.get("id") == user_id:
#             return user
    return [user for user in fake_users if user.get("id") == user_id]

fake_trades = [
    {"id":0, "user_id":0,"currency":"BTC", "side":"buy", "price":123,"amount":2.12},
    {"id":0, "user_id":0,"currency":"BTC", "side":"buy", "price":123,"amount":2.12},
]

class Trade(BaseModel):
    id:int
    user_id:int
    currency:str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float

@app.post("/trades")
def add_trades(trades:List[Trade]):
    fake_trades.extend(trades)
    return{"status":200, "data": fake_trades}