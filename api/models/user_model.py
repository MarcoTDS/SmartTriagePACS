from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.config.database import Base

class UserTypeModel(Base):
    __tablename__ = "usertypes"  # SQL: userTypes (postgres costuma usar lowercase)
    
    id_user_type = Column(Integer, primary_key=True, index=True)
    user_type_name = Column(String(100))

class UserModel(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), unique=True)
    user_password = Column(String(255))
    user_name = Column(String(255))
    crm = Column(String(10))
    crm_uf = Column(String(2))
    
    # Chave Estrangeira
    id_user_type = Column(Integer, ForeignKey("usertypes.id_user_type"), nullable=True)
    
    # Relacionamento para acessar os dados do tipo diretamente (opcional, mas útil)
    user_type = relationship("UserTypeModel")