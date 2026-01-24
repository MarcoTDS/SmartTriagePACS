import subprocess
import sys
import os

# Variável global para guardar a referência do processo
dicom_process = None

def start_dicom_listener(port: int = 1050, aet: str = "SMARTTRIAGE", storage: str = "C:/TESTEDICOM/STORAGE"):
    global dicom_process
    
    if dicom_process and dicom_process.poll() is None:
        return {"status": "already_running", "pid": dicom_process.pid}

    # Define as variáveis de ambiente para o subprocesso
    env = os.environ.copy()
    env["DICOM_PORT"] = str(port)
    env["DICOM_AET"] = aet
    env["STORAGE_DIR"] = storage

    # Inicia o script dicom_listener.py como um processo separado
    # sys.executable garante que usamos o mesmo Python do ambiente virtual
    dicom_process = subprocess.Popen(
        [sys.executable, "api\\dicom_listener.py"],
        env=env,
        cwd=os.getcwd() # Garante que roda na raiz do projeto
    )
    
    return {"status": "started", "pid": dicom_process.pid}

def stop_dicom_listener():
    global dicom_process
    
    if dicom_process and dicom_process.poll() is None:
        dicom_process.terminate() # Tenta fechar graciosamente
        dicom_process.wait()      # Espera fechar
        dicom_process = None
        return {"status": "stopped"}
    
    return {"status": "not_running"}

def get_status():
    global dicom_process
    if dicom_process and dicom_process.poll() is None:
        return {"active": True, "pid": dicom_process.pid}
    return {"active": False, "pid": None}