from faker import Faker
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

fake = Faker()

app = FastAPI(
    title="Trading App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello,{user.username}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello,anonym"

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