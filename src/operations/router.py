import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache
from src.database import get_async_session
from .models import operation
from .schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

#redis
@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"

@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
#endpoint всегда должен иметь try except,также стоит обрабатывать отдельные ошибки(частный случай)
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        # x = 1/0
        #лучше писать "шаблон" как минимум из-за suc чтобы на фронте было чтот обрабатывать
        return {
            "status": "success",
            "data": result.scalars(),
            "details": None,
            }
    # except ZeroDivisionError:
    #     raise HTTPException(status_code = 500, detail ={
    #         "status":"error",
    #         "data": None,
    #         "details":"Не дели на 0"
    #     })
    except Exception:
        #Передать ошибку разработчикам
        raise HTTPException(status_code = 500, detail ={
            "status":"error",
            "data": None,
            "details": None
        })


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**dict(new_operation))
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}