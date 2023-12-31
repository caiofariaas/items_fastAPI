from sqlalchemy import create_engine, MetaData
from databases import Database
from sqlalchemy.orm import Session

DATABASE_URL = 'sqlite:///./data.db'

# este objeto 'Database()' é usado para gerenciar a conexão com o banco de dados
# ele fornece uma interface assíncrona para operações de banco de dados

database = Database(DATABASE_URL)

# objeto 'MetaData()' é usado para armazenar info's sobre as tabelas e outros elementos do banco de dados
# ex: Nome de tabelas, indices, info sobre foreign key's etc
# quando criamos o modelo de dados usando o SQLAlchemy definimos a estrutura das tabelas usando classes Python, o MetaData é usado para coletar essas definições
# e aplica-lás no banco de dados

metadata = MetaData()

# o objeto 'Engine' é responsável por estabelecer e gerenciar uma conexão com o banco de dados
# tambem fornece uma interface para executar consultas SQL e gerenciar transações no banco de dados

engine = create_engine(DATABASE_URL)

# agora utilizados o 'create_all' do objeto 'metadata' para criar todas as tabelas definidas no nosso codigo
# o 'bind=engine' especifica que as tabelas devem ser criadas usando a conexão do 'Engine' que criamos

metadata.create_all(bind= engine)

# nessa função utilizamos a funcionalidade de geradores 'yield' para criar um contexto
# na qual uma instancia do banco(db) é fornecida
# o finally é so para garantir que após o uso ela seja desconectada

def get_db():
    db = database
    try: 
        yield db
    finally:
        db.disconnect()
