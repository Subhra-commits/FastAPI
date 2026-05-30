from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:pg1234@localhost:5432/fastapi_tut"
db_engine = create_engine(db_url)
session = sessionmaker(autocommit = False, autoflush= False, bind= db_engine)
