from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from src.operations.router import router as router_operation
from src.tasks.router import router as router_tasks
from pages.router import router as router_pages

app = FastAPI(
    title="Trading App"
)

app.mount("/static",StaticFiles(directory="static"), name = "static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_pages)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
     # обрабатывает запрос перед тем как придет на сервер 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # все необходимые методы прописывать
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


#startup shurdown fun при открытии и закрытии соответственно
@app.get("/")
async def redirect_from_main():
    return RedirectResponse("/docs")

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost",encoding = "utf8",decode_responses = True)
    FastAPICache.init(RedisBackend(redis),prefix = "fastapi-cache")