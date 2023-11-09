from fastapi import FastAPI
from faker import Faker

fake = Faker()
app = FastAPI()



fake_users = [
    {"id":0, "role":"admin", "name":fake.name()},   
    {"id":1, "role":"admin", "name":fake.name()},
    {"id":2, "role":"admin", "name":fake.name()}
]


@app.get("/users/{user_id}")
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

@app.get("/trades")
def get_trades(limit:int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]

fake_users2 = [
    {"id":0, "role":"admin", "name":fake.name()},   
    {"id":1, "role":"admin", "name":fake.name()},
    {"id":2, "role":"admin", "name":fake.name()}
]

@app.post("/users/{user_id}")
def change_name(user_id:int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"statuts": 200,"data":current_user}