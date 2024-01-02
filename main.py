from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import *
from models import *


app = FastAPI()

# o 'response_model' é usado para especificar qual modelo pydantic será usado para validar e documentar a resposta da rota
# usamos om 'ItemRead' por ela ser a classe mais completa e essas operações retornam
# detalhes completos dos items, pós CRUD

@app.post('/create_item/', response_model=ItemRead)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    
    # criamos um objeto SQLAlchemy 'ItemDB'
    # Converte a instancia pydantic a um dicionário para se encaixar em ItemDB
    
    db_item = ItemDB(**item.dict())
    
    # Adiciona a sessão do banco de dados
    
    db.add(db_item)
    
    # Realiza o commit das alterações à sessão do banco
    
    db.commit()
    
    # atualiza a instancia do modelo 'ItemDB' com os valores do banco após o commit
    # após o commit a instancia terá um novo 'id' gerado pelo banco
    
    db.refresh(db_item)
    
    return db_item

@app.get('/get_item/{item_id}', response_model=ItemRead)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    if item is None:
        raise HTTPException(status_code=404, detail='Item Not Found')
    
    return item
