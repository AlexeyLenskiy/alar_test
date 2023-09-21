from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from src.db.settings import Base

class Data1Model(Base):
    __tablename__ = "data_1"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)

class Data2Model(Base):
    __tablename__ = "data_2"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)

class Data3Model(Base):
    __tablename__ = "data_3"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)


class Data(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True