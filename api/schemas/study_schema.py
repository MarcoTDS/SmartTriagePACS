from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

# Base comum
class StudyBase(BaseModel):
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    patient_sex: Optional[str] = None
    patient_birth_date: Optional[date] = None
    body_part: Optional[str] = None
    modality: Optional[str] = None
    accession_number: Optional[str] = None
    study_instance_uid: str  # Obrigatório e único
    study_date: datetime
    study_description: Optional[str] = None
    study_priority: int = 0
    file_path: Optional[str] = None

# Schema para criar (pode ter validações extras)
class StudyCreate(StudyBase):
    pass

# Schema para atualizar (todos opcionais)
class StudyUpdate(BaseModel):
    study_status: Optional[str] = None
    study_priority: Optional[int] = None

# Schema de resposta (inclui ID gerado pelo banco)
class StudyResponse(StudyBase):
    id_study: int
    study_status: str
    study_last_import: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema usado pelo DICOM Listener para registrar o estudo via API
class StudyIngest(StudyBase):
    study_instance_uid: str
    study_date: str
    study_time: str
    file_path: str # Caminho local onde o listener salvou
    accession_number: Optional[str] = None
    study_description: Optional[str] = None
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    patient_birth_date: Optional[str] = None
    patient_sex: Optional[str] = None
    modality: Optional[str] = None
    body_part: Optional[str] = None