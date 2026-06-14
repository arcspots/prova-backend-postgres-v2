from sqlalchemy import create_engine # type: ignore 
from sqlalchemy.orm import declarative_base, sessionmaker # type: ignore

# String de conexão com PostgreSQL
# formato:
# postgresql://usuario:senha@host:porta/database
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:123456@db:5432/prova_backend"
)

# Cria engine de conexão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fabrica sessões para cada request
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Classe base para os models
Base = declarative_base()