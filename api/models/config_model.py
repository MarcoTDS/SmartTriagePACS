from sqlalchemy import Column, Integer, String, Boolean
from api.config.database import Base

class ServerConfModel(Base):
    __tablename__ = "server_conf"

    id_conf = Column(Integer, primary_key=True, index=True)
    ae_title = Column(String(16), default="SMART_TRIAGE") # Nome do seu PACS
    port = Column(Integer, default=11112) # Porta padrão DICOM (geralmente 104 ou 11112)
    storage_path = Column(String(500)) # Ex: C:\storage\pacs
    allowed_ips = Column(String(1000)) # Ex: "192.168.0.10, 192.168.0.20" (Separado por vírgula)
    active = Column(Boolean, default=True)