from fastapi import FastAPI
from api.config.database import engine, Base
from api.routers import study_router, auth_router, config_router

from api.models import study_model, user_model

app = FastAPI(title="SmartTriagePACS API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(study_router.router)
app.include_router(auth_router.router)
app.include_router(config_router.router)