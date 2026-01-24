from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models.user_model import UserModel
from api.schemas.user_schema import UserCreate
from api.utils.security import get_password_hash

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        query = select(UserModel).where(UserModel.user_email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user: UserCreate):
        # 1. Gera o hash da senha
        hashed_password = get_password_hash(user.user_password)
        
        # 2. Cria o modelo com a senha criptografada
        db_user = UserModel(
            user_email=user.user_email,
            user_name=user.user_name,
            user_password=hashed_password, # Salvando o hash!
            crm=user.crm,
            crm_uf=user.crm_uf,
            id_user_type=user.id_user_type
        )
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user