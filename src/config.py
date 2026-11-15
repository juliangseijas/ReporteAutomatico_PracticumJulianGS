import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar las variables ocultas desde el archivo .env en la raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Config:
    # Credenciales Meta
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
    META_APP_ID = os.getenv("META_APP_ID")
    META_APP_SECRET = os.getenv("META_APP_SECRET")
    META_API_VERSION = os.getenv("META_API_VERSION", "v19.0")

    # Credenciales Google
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_DEVELOPER_TOKEN = os.getenv("GOOGLE_DEVELOPER_TOKEN")

    # Archivos OAuth de Google
    CREDENTIALS_FILE = str(ROOT_DIR / "credentials.json")
    TOKEN_FILE = str(ROOT_DIR / "token.json")

    # Permisos de Google API (Slides + Drive para clonar plantillas)
    GOOGLE_SCOPES = [
        "https://www.googleapis.com/auth/presentations",
        "https://www.googleapis.com/auth/drive",
    ]

    # ID por defecto de la plantilla de Google Slides
    DEFAULT_PRESENTATION_ID = os.getenv(
        "GOOGLE_SLIDES_TEMPLATE_ID",
        "1G2-phuROq_Crjazr-x7XH6ZphOmN9eMXQnH6i8EJBFc",
    )

    # Catálogo de clientes configurados en la agencia Monstruo Canela
    CLIENTES = {
        "Universal en Becas": {
            "company_name": "Universal en Becas",
            "ad_account_id": os.getenv("META_AD_ACCOUNT_UNIVERSAL", "act_792323499648312"),
            "facebook_page_id": os.getenv("META_FB_PAGE_UNIVERSAL", "235411783191404"),
            "instagram_account_id": os.getenv("META_IG_ACCOUNT_UNIVERSAL", "17841403196156646"),
            "instagram_handle": "@universalenbecas",
            "presentation_id": os.getenv(
                "GOOGLE_SLIDES_TEMPLATE_ID",
                "1G2-phuROq_Crjazr-x7XH6ZphOmN9eMXQnH6i8EJBFc",
            ),
        },
        "Distrito Financiero": {
            "company_name": "Distrito Financiero",
            "ad_account_id": os.getenv("META_AD_ACCOUNT_DISTRITO", "act_792323499648312"),
            "facebook_page_id": os.getenv("META_FB_PAGE_DISTRITO", ""),
            "instagram_account_id": os.getenv("META_IG_ACCOUNT_DISTRITO", ""),
            "instagram_handle": "@distritofinanciero",
            "presentation_id": os.getenv(
                "GOOGLE_SLIDES_TEMPLATE_ID",
                "1G2-phuROq_Crjazr-x7XH6ZphOmN9eMXQnH6i8EJBFc",
            ),
        },
        "Cliente 3": {
            "company_name": "Cliente 3",
            "ad_account_id": os.getenv("META_AD_ACCOUNT_CLIENTE3", "act_792323499648312"),
            "facebook_page_id": os.getenv("META_FB_PAGE_CLIENTE3", ""),
            "instagram_account_id": os.getenv("META_IG_ACCOUNT_CLIENTE3", ""),
            "instagram_handle": "@cliente3",
            "presentation_id": os.getenv(
                "GOOGLE_SLIDES_TEMPLATE_ID",
                "1G2-phuROq_Crjazr-x7XH6ZphOmN9eMXQnH6i8EJBFc",
            ),
        },
    }

    @classmethod
    def obtener_cliente(cls, nombre_cliente):
        return cls.CLIENTES.get(
            nombre_cliente,
            {
                "company_name": nombre_cliente,
                "ad_account_id": "act_792323499648312",
                "facebook_page_id": "",
                "instagram_account_id": "",
                "instagram_handle": f"@{nombre_cliente.lower().replace(' ', '')}",
                "presentation_id": cls.DEFAULT_PRESENTATION_ID,
            },
        )


if __name__ == "__main__":
    print("Módulo de configuración cargado con éxito. Entorno seguro.")