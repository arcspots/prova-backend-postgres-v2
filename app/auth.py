from datetime import datetime, timedelta
from jose import jwt, JWTError  # type: ignore
from fastapi import HTTPException


# chave secreta (em produção iria para env/.env)
SECRET_KEY = "minha_super_chave_secreta_2026"

# algoritmo usado no JWT
ALGORITHM = "HS256"

# expiração do token (30 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# função para criar token JWT
def create_access_token(data: dict):
    """
    Gera token JWT com tempo de expiração.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# função para verificar token JWT 
def verify_token(token: str):
    """
    Verifica se o token é válido e se não expirou.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
    
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )