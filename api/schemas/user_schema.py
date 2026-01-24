from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Base
class UserBase(BaseModel):
    user_email: EmailStr
    user_name: str
    crm: Optional[str] = None
    crm_uf: Optional[str] = None
    id_user_type: Optional[int] = None

# Cadastro (Input)
class UserCreate(UserBase):
    user_password: str # Senha crua que o usuário digita

# Resposta (Output) - NÃO retornamos a senha!
class UserResponse(UserBase):
    id_user: int
    
    model_config = ConfigDict(from_attributes=True)

# Login (Token)
class Token(BaseModel):
    access_token: str
    token_type: str