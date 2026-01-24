from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import dotenv

# Carrega as variáveis de ambiente do arquivo .env
dotenv.load_dotenv()

# Substitua com seus dados: postgresql+asyncpg://usuario:senha@localhost/nome_banco
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Dependência para injetar a sessão do banco nas rotas
async def get_db():
    async with SessionLocal() as session:
        yield session