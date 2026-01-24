from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from api.models.study_model import StudyModel
from api.schemas.study_schema import StudyCreate, StudyIngest

class StudyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- FUNÇÕES DE LEITURA (QUE ESTAVAM FALTANDO) ---
    async def get_all_studies(self, skip: int = 0, limit: int = 100):
        query = select(StudyModel).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_study_by_id(self, study_id: int):
        query = select(StudyModel).where(StudyModel.id_study == study_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    # --- FUNÇÕES DE CRIAÇÃO E INGESTÃO ---
    async def create_study(self, study: StudyCreate):
        new_study = StudyModel(**study.dict())
        self.db.add(new_study)
        await self.db.commit()
        await self.db.refresh(new_study)
        return new_study

    async def register_dicom_file(self, data: StudyIngest):
        """
        Recebe os dados brutos do DICOM Listener e salva no banco.
        """
        
        # 1. Verificar se o estudo já existe pelo UID
        query = select(StudyModel).where(StudyModel.study_instance_uid == data.study_instance_uid)
        result = await self.db.execute(query)
        existing_study = result.scalars().first()

        # 2. Se já existe, apenas retornamos ele (atualizando data de modificação)
        if existing_study:
            existing_study.study_last_import = datetime.now()
            await self.db.commit()
            return existing_study

        # 3. Tratamento de Datas (String DICOM -> Python Datetime)
        study_dt = datetime.now() # Valor padrão
        try:
            if data.study_date and data.study_time:
                date_str = data.study_date
                time_str = data.study_time.split('.')[0] 
                dt_combined = f"{date_str}{time_str}"
                study_dt = datetime.strptime(dt_combined, "%Y%m%d%H%M%S")
            elif data.study_date:
                 study_dt = datetime.strptime(data.study_date, "%Y%m%d")
        except ValueError:
            pass 

        # Tratamento da Data de Nascimento
        birth_date = None
        try:
            if data.patient_birth_date:
                birth_date = datetime.strptime(data.patient_birth_date, "%Y%m%d").date()
        except ValueError:
            pass

        # 4. Criar o objeto do Modelo
        new_study = StudyModel(
            patient_id=data.patient_id,
            patient_name=data.patient_name,
            patient_sex=data.patient_sex,
            patient_birth_date=birth_date,
            body_part=data.body_part,
            modality=data.modality,
            accession_number=data.accession_number,
            study_instance_uid=data.study_instance_uid,
            study_date=study_dt,
            study_description=data.study_description,
            study_priority=0,
            file_path=data.file_path,
            study_status="RECEBIDO",
            study_last_import=datetime.now()
        )

        # 5. Salvar no Banco
        self.db.add(new_study)
        await self.db.commit()
        await self.db.refresh(new_study)
        
        return new_study