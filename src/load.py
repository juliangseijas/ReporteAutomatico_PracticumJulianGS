import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Este es el alcance o permiso: Le decimos a Google que queremos modificar presentaciones
SCOPES = ['https://www.googleapis.com/auth/presentations']

# Reemplaza esto con el ID largo de la URL de tu presentación de prueba
PRESENTATION_ID = '1GTbblgcXLwfP_YljzqnxEkScu8fRqX1QZpeV_JVpyzs'

def autenticar_google():
    print("Protocolo de seguridad OAuth 2.0 con Google...")
    creds = None
    
    # El archivo token.json se genera automáticamente la primera vez que inicias sesión.
    # Evita que tengas que poner tu contraseña todos los días.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # Si no hay credenciales o caducaron, pedimos iniciar sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Aquí Python lee tu archivo credentials.json
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Guardamos el token de larga duración
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('slides', 'v1', credentials=creds)

def probar_inyeccion_slides():
    servicio = autenticar_google()
    print("Conexión establecida. Escribiendo en la plantilla...")

    # Instrucción exacta para buscar tu marcador y reemplazarlo
    # Instrucciones exactas para buscar tus marcadores y reemplazarlos
    peticiones = [
        {
            'replaceAllText': {
                'containsText': {'text': '{{nombre_campana}}', 'matchCase': True},
                'replaceText': "Universal en Becas (Prueba Automática)"
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '{{gasto}}', 'matchCase': True},
                'replaceText': "3961.17"
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '{{clics}}', 'matchCase': True},
                'replaceText': "1359"
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '{{ctr}}', 'matchCase': True},
                'replaceText': "9.06"
            }
        }
    ]

    cuerpo = {
        'requests': peticiones
    }

    try:
        # Ejecutamos la orden en los servidores de Google
        respuesta = servicio.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=cuerpo).execute()
        
        reemplazos = len(respuesta.get('replies', []))
        print(f" Se modificó la presentación en vivo.")
        
    except Exception as e:
        print(f"Ocurrió un error al contactar a Google: {e}")

if __name__ == '__main__':
    probar_inyeccion_slides()