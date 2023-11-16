from datetime import datetime, date
from sqlalchemy import create_engine, insert
from src.operations.models import operation, Operation
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
# Insert data
from sqlalchemy.orm import Session
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", future=True, echo=True)
with Session(bind=engine) as session:
    # stmp = (
    #     insert(operation).values(id=1, quantity="quantity", figi = "figi", instrument_type = "instrument_type",date=datetime.now(),type = "type")
    # )
    
    # session.execute(stmp)
    # session.commit()
    #oper1 = operation()
    oper2 = Operation(id=2, quantity="test2", figi="test2", instrument_type="test3", date=datetime.now(), type="type2")
    session.add_all([oper2])
    session.commit()
    #session.add_all([oper1])
    #session.commit()

