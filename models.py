from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelos Pydantic

    # Modelo para entrada(create)
class ItemCreate(BaseModel):
    name: str
    desc: str
    price: float
    
    # o 'validator' é uma função do 'pydantic' que permite você definir funções dentro de uma classe de modelo
    # é usado para validar e processar dados antes que eles sejam atribuidos aos campos do model
    # aqui por exemplo usamos para criar um tratamento de exceção para o campo 'price'
    
    @validator('price')
    def price_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Must be greater than or equal to 0')
        return value
    
    # Modelo para saída

class ItemRead(BaseModel):
    id: int
    name: str
    desc: str
    price: float
    
    # Modelo para Uptade
    
class ItemUpdate(BaseModel):
    name: str
    desc: str
    price: float
    
    @validator('price')
    def price_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Must be greater than or equal to 0')
        return value
    
# Modelo que contem todos os campos
    
class Item(ItemCreate, ItemUpdate):
    pass

# Modelos SQLAlchemy, criação das tabelas

class ItemDB(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, index=True)
    desc = Column(String)
