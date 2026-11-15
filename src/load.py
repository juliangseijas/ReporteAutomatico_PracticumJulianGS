import os
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

try:
    from src.config import Config
    from src.transform import (
        construir_marcadores_reporte,
        extraer_marcadores_imagen_validos,
    )
except ImportError:
    from config import Config
    from transform import (
        construir_marcadores_reporte,
        extraer_marcadores_imagen_validos,
    )

SCOPES = Config.GOOGLE_SCOPES
PRESENTATION_ID = Config.DEFAULT_PRESENTATION_ID


def obtener_credenciales_google():
    """
    Obtiene o refresca las credenciales OAuth 2.0 de Google para Slides y Drive.
    """
    creds = None
    token_path = Config.TOKEN_FILE if os.path.exists(Config.TOKEN_FILE) else "token.json"
    creds_path = (
        Config.CREDENTIALS_FILE
        if os.path.exists(Config.CREDENTIALS_FILE)
        else "credentials.json"
    )

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None
        else:
            creds = None

        if creds is None:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(Config.TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds


def autenticar_google():
    """Retorna el cliente autenticado de Google Slides API v1."""
    print("Protocolo de seguridad OAuth 2.0 con Google...")
    creds = obtener_credenciales_google()
    return build("slides", "v1", credentials=creds)


def copiar_plantilla(presentation_id, nombre_reporte, creds=None):
    """
    Clona la presentación plantilla en Google Drive y retorna dict con id, name y webViewLink.
    """
    creds = creds or obtener_credenciales_google()
    servicio_drive = build("drive", "v3", credentials=creds)
    copia = (
        servicio_drive.files()
        .copy(
            fileId=presentation_id,
            body={"name": nombre_reporte},
            fields="id,name,webViewLink",
        )
        .execute()
    )
    return copia


def renderizar_slide(
    presentation_id,
    datos_campana,
    nombre_reporte,
    inyectar_imagenes=True,
):
    """
    Clona la plantilla de Google Slides, inyecta imágenes en las formas que contengan
    marcadores de imagen (ej. {{f_top1_url}}, {{i_top1_url}}, {{i_mapa_calor}}) y
    reemplaza todos los marcadores de texto {{...}}.
    """
    creds = obtener_credenciales_google()
    servicio_slides = build("slides", "v1", credentials=creds)
    copia = copiar_plantilla(presentation_id, nombre_reporte, creds=creds)

    marcadores = construir_marcadores_reporte(datos_campana)

    # 1. Inyección de imágenes mediante replaceAllShapesWithImage (si aplica)
    if inyectar_imagenes:
        marcadores_img = extraer_marcadores_imagen_validos(marcadores)
        for marcador_img, url_img in marcadores_img.items():
            try:
                servicio_slides.presentations().batchUpdate(
                    presentationId=copia["id"],
                    body={
                        "requests": [
                            {
                                "replaceAllShapesWithImage": {
                                    "imageUrl": url_img,
                                    "imageReplaceMethod": "CENTER_INSIDE",
                                    "containsText": {
                                        "text": marcador_img,
                                        "matchCase": True,
                                    },
                                }
                            }
                        ]
                    },
                ).execute()
            except Exception as e:
                print(
                    f"Aviso: No se pudo inyectar imagen para {marcador_img} ({e}). "
                    "Se reemplazará como texto."
                )

    # 2. Reemplazo masivo de todos los marcadores de texto restantes
    peticiones_texto = [
        {
            "replaceAllText": {
                "containsText": {"text": marcador, "matchCase": True},
                "replaceText": str(valor),
            }
        }
        for marcador, valor in marcadores.items()
    ]

    if peticiones_texto:
        servicio_slides.presentations().batchUpdate(
            presentationId=copia["id"],
            body={"requests": peticiones_texto},
        ).execute()

    return copia


def probar_inyeccion_slides():
    try:
        from src.extract import generar_datos_demo_completos
    except ImportError:
        from extract import generar_datos_demo_completos

    datos_demo = generar_datos_demo_completos("Universal en Becas")
    copia = renderizar_slide(
        PRESENTATION_ID,
        datos_demo,
        "PRUEBA Inyección Google Slides - Universal en Becas",
    )
    print(f"Se creó y actualizó la copia en vivo: {copia.get('webViewLink', copia['id'])}")
    return copia


if __name__ == "__main__":
    probar_inyeccion_slides()