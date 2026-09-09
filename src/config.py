import os
from dotenv import load_dotenv

# Cargar las variables ocultas desde el archivo .env
load_dotenv()

class Config:
    # Credenciales Meta
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
    META_APP_ID = os.getenv("META_APP_ID")
    META_APP_SECRET = os.getenv("META_APP_SECRET")
    
    # Credenciales Google
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_DEVELOPER_TOKEN = os.getenv("GOOGLE_DEVELOPER_TOKEN")

# Prueba rápida para ver si funciona (luego borraremos este print)
if __name__ == "__main__":
    print("Módulo de configuración cargado con éxito. Entorno seguro.")