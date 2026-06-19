from sqlalchemy import Column, Integer, String
from database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    number = Column(String)
    owner = Column(String)
    model = Column(String)