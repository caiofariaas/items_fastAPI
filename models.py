from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelos Pydantic

    # Modelo para entrada(create)
class ItemCreate(BaseModel):
    name: str
    desc: str
    
    # Modelo para saída

class ItemRead(BaseModel):
    id: int
    name: str
    desc: str
    
    # Modelo para Uptade
    
class ItemUpdate(BaseModel):
    name: str
    desc: str
    
    # Modelo que contem todos os campos
    
class Item(ItemCreate, ItemUpdate):
    pass

# Modelos SQLAlchemy, criação das tabelas

class ItemDB(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    desc = Column(String)
