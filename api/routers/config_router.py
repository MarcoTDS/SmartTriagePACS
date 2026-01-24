import os
import dotenv
from fastapi import APIRouter, Depends
from api.utils.process_manager import start_dicom_listener, stop_dicom_listener, get_status
from api.models.user_model import UserModel
from api.dependencies import get_current_user # Segurança: só admin/logado mexe nisso

router = APIRouter(prefix="/config", tags=["Configuration"])

MY_PORT = int(os.getenv("DICOM_PORT"))
MY_AET = os.getenv("DICOM_AET")
STORAGE_DIR = os.getenv("STORAGE_DIR")

@router.get("/server/status")
def server_status(current_user: UserModel = Depends(get_current_user)):
    return get_status()

@router.post("/server/start")
def start_server(current_user: UserModel = Depends(get_current_user)):
    # Aqui você poderia buscar as configs do banco (ServerConfModel) antes de iniciar
    return start_dicom_listener(MY_PORT, MY_AET, STORAGE_DIR)
                                

@router.post("/server/stop")
def stop_server(current_user: UserModel = Depends(get_current_user)):
    return stop_dicom_listener()