from sqlalchemy import Column, Integer, String, DateTime # type: ignore
from datetime import datetime  
from app.database import Base 

class User(Base):
    __tablename__ = "users"
    
    # ID auto incrementável
    id = Column(Integer, primary_key=True, index=True)
   
    # nome do usuário
    name = Column(String, nullable=False)
    
    # email unico para evitar duplicação
    email = Column(String, unique=True, nullable=False)
    
    # timestamp de criação 
    created_at = Column(DateTime, default=datetime.utcnow)