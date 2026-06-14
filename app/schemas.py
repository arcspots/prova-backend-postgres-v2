from pydantic import BaseModel
from datetime import datetime

# schema para criar usuario (request body)
class UserCreate(BaseModel):
    name: str
    email: str

# schema de resposta da API 
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    
    
    class Config:
        from_attributes = True
# schema para atualizar usuario (request body)
class UserUpdate(BaseModel):
    name: str
    email: str
    
# schema usado para login
class LoginData(BaseModel):
    username: str
    password: str

# schema de resposta com token
class Token(BaseModel):
    access_token: str
    token_type: str

# schema para entrada da IA
class PredictionInput(BaseModel):
    value: float

# schema para saída da IA
class PredictionOutput(BaseModel):
    prediction: float