from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session  # type: ignore
import joblib # type: ignore 

from app.auth import create_access_token, verify_token
from app.database import engine, Base, SessionLocal
import app.models as models
import app.schemas as schemas

# Carrega o modelo treinado de IA
ml_model = joblib.load("app/ml_model.pkl")

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Instancia a aplicação FastAPI
app = FastAPI(
    title="Prova Backend API",
    description="CRUD + IA",
    version="1.0.0"
)
# Sistema de autenticação Bearer (JWT)
security = HTTPBearer()


# Dependency Injection:
# Cada request abre uma sessão com o banco e fecha depois
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware simples para validar token JWT
def auth_guard(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    return verify_token(token)

@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "API funcionando normalmente"
    }

# Rota de login para obter token JWT
@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.LoginData):
    """
    Login simples com usuário fixo.
    Em produção usaríamos banco + hash de senha.
    """

    fake_username = "admin"
    fake_password = "123456"
    
    if (
        credentials.username != fake_username
        or credentials.password != fake_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )
    token = create_access_token(
        data={"sub": credentials.username}
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Rotas CRUD para usuários, todas protegidas por JWT
@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    user_data: dict = Depends(auth_guard)
):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado"
        )

    new_user = models.User(
        name=user.name,
        email=user.email
    )
    # Adiciona o novo usuário a sessão do SQLAlchemy
    db.add(new_user)
    
    # Persiste as mudanças no banco
    db.commit()
    
    # atualiza objeto com ID gerado pelo banco
    db.refresh(new_user)

    return new_user

# Rota para listar todos os usuários, protegida por JWT
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    user_data: dict = Depends(auth_guard)
):
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user_data: dict = Depends(auth_guard)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    updated_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    user_data: dict = Depends(auth_guard)
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    user.name = updated_data.name
    user.email = updated_data.email
    db.commit()
    db.refresh(user)

    return user

# Rota para deletar um usuário por ID, protegida por JWT
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user_data: dict = Depends(auth_guard)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Usuário removido com sucesso"
    }

@app.post("/predict", response_model=schemas.PredictionOutput)
def predict(
    data: schemas.PredictionInput,
    user_data: dict = Depends(auth_guard)
):
    """
    Recebe um valor numérico e retorna a predição do modelo de IA.
    """

    prediction = ml_model.predict([[data.value]])

    return {
        "prediction": float(prediction[0])
    }