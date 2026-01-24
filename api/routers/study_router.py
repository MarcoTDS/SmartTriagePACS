from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.config.database import get_db
from api.schemas.study_schema import StudyCreate, StudyResponse, StudyUpdate, StudyIngest
from api.services.study_service import StudyService

router = APIRouter(prefix="/studies", tags=["Studies"])

@router.post("/", response_model=StudyResponse, status_code=201)
async def create_study(study: StudyCreate, db: AsyncSession = Depends(get_db)):
    service = StudyService(db)
    # Verifica se já existe (regra de negócio simples)
    existing = await service.get_study_by_uid(study.study_instance_uid)
    if existing:
        raise HTTPException(status_code=400, detail="Study UID already exists")
    
    return await service.create_study(study)

@router.get("/", response_model=List[StudyResponse])
async def list_studies(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    service = StudyService(db)
    return await service.get_all_studies(skip, limit)

@router.patch("/{id_study}/status", response_model=StudyResponse)
async def update_study_status(id_study: int, status: str, db: AsyncSession = Depends(get_db)):
    service = StudyService(db)
    updated_study = await service.update_status(id_study, status)
    if not updated_study:
        raise HTTPException(status_code=404, detail="Study not found")
    return updated_study

# Rota interna (pode ser protegida por IP ou API Key fixa no futuro)
@router.post("/internal/ingest", status_code=201)
async def ingest_dicom_study(data: StudyIngest, db: AsyncSession = Depends(get_db)):
    service = StudyService(db)
    # Aqui chamamos um método novo no service que lida com essa ingestão
    # Para simplificar, vamos reutilizar a lógica de criação ou adaptar:
    return await service.register_dicom_file(data)