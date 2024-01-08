from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import *
from models import *
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# aqui colocamos uma lista de dominios permitidos a usarem a API, no caso o frontend

# origins = ["http://127.0.0.1:5500"]

# # adiciona um middleware a aplicação FastAPI, neste caso o CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "OPTIONS"],  # Adicione outros métodos conforme necessário
#     allow_headers=["*"],
# )

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

# UPDATE para os items

@app.put('/update_item/{item_id}', response_model=ItemRead)
async def update_item(item_id: int, upd_item: ItemUpdate, db: Session = Depends(get_db)):
    
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail='Item Not Found')

    # Criamos um for para percorrer todos os itens 'key : value'
    # usamos '.dict()' para transformar o objeto pydantic em um dict
    # items() retorna uma sequencia de tuplas onde cada uma contem um par key-value
    
    for key, value in upd_item.dict().items():
        
        # 'set attribute' é usada para definir o valor de um atributo em um objeto
        # recebe como parametro o objeto, o nome do atributo que deseja definir ou modificar e o valor que deseja atribuir ao mesmo
        
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

# Função para excluir do banco de dados

@app.delete('/delete_item/{item_id}')
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    if db_item:
        db.delete(db_item)
        db.commit()
        
        return {'message': f'Item with id "{item_id}" deleted', 'Deleted_item': db_item}
    else:
        raise HTTPException(status_code=404, detail='Item Not Found')

# GET para itens especificos

@app.get('/get_item/{item_id}', response_model=ItemRead)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    # Tratamento de exception's
    
    if item is None:
        raise HTTPException(status_code=404, detail='Item Not Found')
    
    return item

# GET para todos os items da lista

@app.get('/get_all_items', response_model=List[ItemRead])
async def get_all_items(db: Session = Depends(get_db)):
    items = db.query(ItemDB).all()
    
    return items
