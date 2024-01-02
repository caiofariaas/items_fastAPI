from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.pool import NullPool
from models import Base

DATABASE_URL = "sqlite:///./data.db"

# este objeto 'Database()' é usado para gerenciar a conexão com o banco de dados
# ele fornece uma interface assíncrona para operações de banco de dados

database = Database(DATABASE_URL)

# o objeto 'Engine' é responsável por estabelecer e gerenciar uma conexão com o banco de dados
# tambem fornece uma interface para executar consultas SQL e gerenciar transações no banco de dados


# "check_same_thread": False
# No SQLite, por padrão, o acesso ao banco de dados é permitido apenas no mesmo thread em que a conexão foi criada.
# No entanto, ao definir check_same_thread como False, você está permitindo que a conexão seja usada em threads diferentes do que foi criada.

# 'poolclass=NullPool'
# Desativa completamente o pooling de conexões (poolclass=NullPool).

# Essa configuração é específica para o SQLite e é
# frequentemente usada em ambientes onde o SQLite é 
# usado em conjunto com o FastAPI e o SQLAlchemy para evitar problemas de threading. 

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=NullPool)

# objeto 'MetaData()' é usado para armazenar info's sobre as tabelas e outros elementos do banco de dados
# ex: Nome de tabelas, indices, info sobre foreign key's etc
# quando criamos o modelo de dados usando o SQLAlchemy definimos a estrutura das tabelas usando classes Python, o MetaData é usado para coletar essas definições
# e aplica-lás no banco de dados

metadata = MetaData()

# agora utilizados o 'create_all' do objeto 'metadata' para criar todas as tabelas definidas no nosso codigo
# o 'bind=engine' especifica que as tabelas devem ser criadas usando a conexão do 'Engine' que criamos

Base.metadata.create_all(bind=engine)

# cria sessões que são responsáveis pela interação com o banco de dados
# SessionLocal está configurando uma fábrica de sessões que:
# Desativa o modo de autocommit automático.
# Desativa o modo de autoflush automático.
# Vincula a sessão a um mecanismo de banco de dados específico (engine).

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
