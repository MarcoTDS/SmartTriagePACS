from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.config.database import get_db
from api.utils.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from api.models.user_model import UserModel

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    Função de dependência que valida o Token JWT.
    Se o token for inválido ou expirado, lança erro 401.
    Se for válido, busca o usuário no banco e o retorna.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Tenta decodificar o token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no banco de dados
    result = await db.execute(select(UserModel).where(UserModel.user_email == email))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user