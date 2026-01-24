from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models.study_model import StudyModel
from api.schemas.study_schema import StudyCreate, StudyUpdate

class StudyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_study(self, study: StudyCreate):
        # Transforma o schema Pydantic no model SQLAlchemy
        new_study = StudyModel(**study.model_dump())
        
        self.db.add(new_study)
        await self.db.commit()
        await self.db.refresh(new_study)
        return new_study

    async def get_all_studies(self, skip: int = 0, limit: int = 100):
        # Query assíncrona
        query = select(StudyModel).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_study_by_uid(self, uid: str):
        query = select(StudyModel).where(StudyModel.study_instance_uid == uid)
        result = await self.db.execute(query)
        return result.scalars().first()
        
    async def update_status(self, study_id: int, status: str):
        query = select(StudyModel).where(StudyModel.id_study == study_id)
        result = await self.db.execute(query)
        study = result.scalars().first()
        
        if study:
            study.study_status = status
            await self.db.commit()
            await self.db.refresh(study)
        return study