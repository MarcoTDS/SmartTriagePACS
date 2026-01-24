from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
import os
import dotenv

# Carrega as variáveis de ambiente do arquivo .env
dotenv.load_dotenv()

# Configurações (Em produção, isso deve vir de variáveis de ambiente .env)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para gerar o Hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar se a senha bate com o Hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o Token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt