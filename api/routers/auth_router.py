from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from api.config.database import get_db
from api.schemas.user_schema import UserCreate, UserResponse, Token
from api.services.user_service import UserService
from api.utils.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Authentication"])

# Rota para Criar Conta (Sign Up)
@router.post("/auth/signup", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    
    # Verifica se email já existe
    db_user = await service.get_user_by_email(user.user_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await service.create_user(user)

# Rota de Login (Gera o Token)
@router.post("/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Nota: OAuth2PasswordRequestForm espera 'username' e 'password'. 
    # O 'username' dele será o nosso 'user_email'.
    
    service = UserService(db)
    user = await service.get_user_by_email(form_data.username)
    
    # Verifica se usuário existe e se a senha bate
    if not user or not verify_password(form_data.password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}