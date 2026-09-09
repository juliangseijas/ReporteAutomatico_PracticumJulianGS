import os
import requests
import pandas as pd
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/presentations']

# GENERACION  DEL ENLACE
def obtener_credenciales_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            # Esto es lo que imprimirá el enlace larguísimo en tu terminal
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

def obtener_datos_meta(account_id):
    token = os.getenv("META_ACCESS_TOKEN")
    if not account_id.startswith('act_'): account_id = f"act_{account_id}"
    
    url = f"https://graph.facebook.com/v19.0/{account_id}/insights"
    parametros = {'access_token': token, 'fields': 'campaign_name,spend,clicks,ctr', 'date_preset': 'last_30d', 'level': 'campaign'}
    
    respuesta = requests.get(url, params=parametros).json()
    if 'data' in respuesta and respuesta['data']:
        df = pd.DataFrame(respuesta['data'])
        return df.iloc[0] 
    return None

def renderizar_slide(presentation_id, datos_campana):
    # Invocamos el motor de autenticación aquí
    creds = obtener_credenciales_google()
    servicio_slides = build('slides', 'v1', credentials=creds)
    
    peticiones = [
        {'replaceAllText': {'containsText': {'text': '{{nombre_campana}}', 'matchCase': True}, 'replaceText': str(datos_campana['campaign_name'])}},
        {'replaceAllText': {'containsText': {'text': '{{gasto}}', 'matchCase': True}, 'replaceText': str(datos_campana['spend'])}},
        {'replaceAllText': {'containsText': {'text': '{{clics}}', 'matchCase': True}, 'replaceText': str(datos_campana['clicks'])}},
        {'replaceAllText': {'containsText': {'text': '{{ctr}}', 'matchCase': True}, 'replaceText': str(datos_campana['ctr'])}}
    ]
    
    servicio_slides.presentations().batchUpdate(
        presentationId=presentation_id, body={'requests': peticiones}
    ).execute()
    print(" ¡Éxito! El reporte ha sido renderizado en Google Slides.")

if __name__ == "__main__":
    ID_PRESENTACION_SLIDES = "1GTbblgcXLwfP_YljzqnxEkScu8fRqX1QZpeV_JVpyzs"
    ID_CLIENTE_META = "act_792323499648312"
    
    print(" Iniciando Fábrica de Datos ETL...")
    datos = obtener_datos_meta(ID_CLIENTE_META)
    
    if datos is not None:
        print(f" Datos transformados listos. Inyectando campaña '{datos['campaign_name']}' en Slides...")
        renderizar_slide(ID_PRESENTACION_SLIDES, datos)
    else:
        print(" No se encontraron datos para renderizar.")