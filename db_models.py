from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Patients(Base):

    __tablename__ = "patients"
    
    id= Column(String, primary_key = True, index = True)
    name= Column(String)
    city = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)
    verdict = Column(String)