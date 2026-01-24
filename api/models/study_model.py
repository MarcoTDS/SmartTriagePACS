from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, func
from api.config.database import Base

class StudyModel(Base):
    __tablename__ = "studies"

    # Mapeando exatamente seus campos SQL
    id_study = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(100))
    patient_name = Column(String(255))
    patient_sex = Column(String(1))
    patient_birth_date = Column(Date)
    body_part = Column(String(255))
    modality = Column(String(50))
    accession_number = Column(String(100))
    study_instance_uid = Column(String(100), unique=True, index=True)
    study_date = Column(DateTime, nullable=False)
    study_description = Column(Text)
    
    # "DEFAULT CURRENT_TIMESTAMP" no SQL vira server_default=func.now()
    study_last_import = Column(DateTime, server_default=func.now())
    study_status = Column(String(50), default='ANALISE PENDENTE')
    study_priority = Column(Integer, default=0)
    file_path = Column(String(512))