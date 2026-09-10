import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Este es el alcance o permiso: Le decimos a Google que queremos modificar presentaciones
SCOPES = ['https://www.googleapis.com/auth/presentations']

# ID de la plantilla de Google Slides
PRESENTATION_ID = '1G2-phuROq_Crjazr-x7XH6ZphOmN9eMXQnH6i8EJBFc'


def autenticar_google():
    print("Protocolo de seguridad OAuth 2.0 con Google...")
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('slides', 'v1', credentials=creds)


def probar_inyeccion_slides():
    servicio = autenticar_google()
    print("Conexión establecida. Escribiendo en la plantilla...")

    peticiones = [
        {'replaceAllText': {'containsText': {'text': '{{facebook_campana}}', 'matchCase': True}, 'replaceText': 'Universal en Becas - Facebook'}},
        {'replaceAllText': {'containsText': {'text': '{{facebook_impresiones}}', 'matchCase': True}, 'replaceText': '154820'}},
        {'replaceAllText': {'containsText': {'text': '{{facebook_alcance}}', 'matchCase': True}, 'replaceText': '98250'}},
        {'replaceAllText': {'containsText': {'text': '{{facebook_clics}}', 'matchCase': True}, 'replaceText': '5760'}},
        {'replaceAllText': {'containsText': {'text': '{{facebook_ctr}}', 'matchCase': True}, 'replaceText': '3.72%'}},
        {'replaceAllText': {'containsText': {'text': '{{facebook_gasto}}', 'matchCase': True}, 'replaceText': '$3,961.17'}},
        {'replaceAllText': {'containsText': {'text': '{{instagram_campana}}', 'matchCase': True}, 'replaceText': 'Universal en Becas - Instagram'}},
        {'replaceAllText': {'containsText': {'text': '{{instagram_impresiones}}', 'matchCase': True}, 'replaceText': '193410'}},
        {'replaceAllText': {'containsText': {'text': '{{instagram_alcance}}', 'matchCase': True}, 'replaceText': '128900'}},
        {'replaceAllText': {'containsText': {'text': '{{instagram_clics}}', 'matchCase': True}, 'replaceText': '6214'}},
        {'replaceAllText': {'containsText': {'text': '{{instagram_ctr}}', 'matchCase': True}, 'replaceText': '3.21%'}},
        {'replaceAllText': {'containsText': {'text': '{{instagram_gasto}}', 'matchCase': True}, 'replaceText': '$2,845.93'}},
        {'replaceAllText': {'containsText': {'text': '{{google_campana}}', 'matchCase': True}, 'replaceText': 'Universal en Becas - Google Ads'}},
        {'replaceAllText': {'containsText': {'text': '{{google_impresiones}}', 'matchCase': True}, 'replaceText': '321560'}},
        {'replaceAllText': {'containsText': {'text': '{{google_clics}}', 'matchCase': True}, 'replaceText': '12800'}},
        {'replaceAllText': {'containsText': {'text': '{{google_ctr}}', 'matchCase': True}, 'replaceText': '3.98%'}},
        {'replaceAllText': {'containsText': {'text': '{{google_costo}}', 'matchCase': True}, 'replaceText': '$4,120.40'}},
        {'replaceAllText': {'containsText': {'text': '{{google_cpc}}', 'matchCase': True}, 'replaceText': '$0.32'}},
        {'replaceAllText': {'containsText': {'text': '{{google_conversiones}}', 'matchCase': True}, 'replaceText': '241'}},
    ]

    cuerpo = {'requests': peticiones}

    try:
        respuesta = servicio.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=cuerpo).execute()

        reemplazos = len(respuesta.get('replies', []))
        print(f" Se modificó la presentación en vivo.")

    except Exception as e:
        print(f"Ocurrió un error al contactar a Google: {e}")


if __name__ == '__main__':
    probar_inyeccion_slides()