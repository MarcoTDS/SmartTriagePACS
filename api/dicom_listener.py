import os
import sys
import requests
import logging
from datetime import datetime
from pynetdicom import AE, evt, StoragePresentationContexts
from pydicom.dataset import Dataset

API_URL = os.getenv("API_URL")
STORAGE_DIR = os.getenv("STORAGE_DIR")
MY_PORT = int(os.getenv("DICOM_PORT"))
MY_AET = os.getenv("DICOM_AET")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DICOM_NODE")

def get_storage_path(ds: Dataset, base_path: str) -> str:
    modality = str(ds.get("Modality", "UNK"))
    study_date = ds.get("StudyDate", datetime.now().strftime("%Y%m%d"))
    study_uid = str(ds.get("StudyInstanceUID", "unknown_study"))
    series_uid = str(ds.get("SeriesInstanceUID", "unknown_series"))
    sop_uid = str(ds.get("SOPInstanceUID", "unknown_image"))
    year, month, day = study_date[:4], study_date[4:6], study_date[6:8]
    full_path = os.path.join(base_path, modality, year, month, day, study_uid, series_uid)
    os.makedirs(full_path, exist_ok=True)
    return os.path.join(full_path, f"{sop_uid}.dcm")

def notify_api(ds: Dataset, file_path: str):
    """Envia os dados para a API FastAPI registrar no banco"""
    payload = {
        "study_instance_uid": str(ds.get("StudyInstanceUID")),
        "study_date": ds.get("StudyDate", ""),
        "study_time": ds.get("StudyTime", ""),
        "file_path": file_path,
        "modality": str(ds.get("Modality", "")),
        "accession_number": str(ds.get("AccessionNumber", "")),
        "patient_id": str(ds.get("PatientID", "")),
        "patient_name": str(ds.get("PatientName", "")),
        "body_part": str(ds.get("BodyPartExamined", "")),
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 201:
            logger.info(f"------API notificada com sucesso: {payload['study_instance_uid']}")
        else:
            logger.error(f"------Erro ao notificar API: {response.text}")
    except Exception as e:
        logger.error(f"------Falha ao conectar na API: {e}")

def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    
    try:
        final_path = get_storage_path(ds, STORAGE_DIR)
        ds.save_as(final_path, enforce_file_format=True)
        notify_api(ds, final_path)
        
        return 0x0000
    except Exception as e:
        logger.error(f"Erro: {e}")
        return 0xC000

if __name__ == "__main__":
    ae = AE(ae_title=MY_AET)
    ae.supported_contexts = StoragePresentationContexts
    
    logger.info(f"🚀 Iniciando DICOM Listener na porta {MY_PORT}...")
    logger.info(f"📂 Salvando em: {STORAGE_DIR}")
    
    ae.start_server(('', MY_PORT), evt_handlers=[(evt.EVT_C_STORE, handle_store)])