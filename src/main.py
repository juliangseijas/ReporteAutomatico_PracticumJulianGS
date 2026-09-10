import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive',
]


def formatear_numero(valor, decimales=2, mostrar_moneda=False):
    if valor is None:
        valor = 0

    if isinstance(valor, str):
        return valor

    if mostrar_moneda:
        return f"${valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    if isinstance(valor, float):
        return f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return str(valor)


def construir_marcadores_reporte(datos_campana):
    facebook = {
        '{{f_seguidores_total}}': formatear_numero(datos_campana.get('facebook_followers_total', 0), 0),
        '{{f_nuevos_seguidores}}': formatear_numero(datos_campana.get('facebook_new_followers', 0), 0),
        '{{f_impresiones}}': formatear_numero(datos_campana.get('facebook_impressions', 0), 0),
        '{{f_alcance}}': formatear_numero(datos_campana.get('facebook_reach', 0), 0),
        '{{f_interacciones}}': formatear_numero(datos_campana.get('facebook_total_interactions', 0), 0),
        '{{f_vistas}}': formatear_numero(datos_campana.get('facebook_views', 0), 0),
        '{{f_clicks_enlace}}': formatear_numero(datos_campana.get('facebook_link_clicks', 0), 0),
        '{{f_contenido_publicado}}': formatear_numero(datos_campana.get('facebook_content_volume', 0), 0),
        '{{f_hombres}}': formatear_numero(datos_campana.get('facebook_gender_men', 0), 0),
        '{{f_mujeres}}': formatear_numero(datos_campana.get('facebook_gender_women', 0), 0),
        '{{f_18_24}}': formatear_numero(datos_campana.get('facebook_age_18_24', 0), 0),
        '{{f_25_34}}': formatear_numero(datos_campana.get('facebook_age_25_34', 0), 0),
        '{{f_35_44}}': formatear_numero(datos_campana.get('facebook_age_35_44', 0), 0),
        '{{f_45_54}}': formatear_numero(datos_campana.get('facebook_age_45_54', 0), 0),
        '{{f_55_64}}': formatear_numero(datos_campana.get('facebook_age_55_64', 0), 0),
        '{{f_65_mas}}': formatear_numero(datos_campana.get('facebook_age_65_plus', 0), 0),
        '{{f_ciudad_1}}': str(datos_campana.get('facebook_city_1', 'Ciudad 1')),
        '{{f_ciudad_1_valor}}': formatear_numero(datos_campana.get('facebook_city_1_value', 0), 0),
        '{{f_ciudad_2}}': str(datos_campana.get('facebook_city_2', 'Ciudad 2')),
        '{{f_ciudad_2_valor}}': formatear_numero(datos_campana.get('facebook_city_2_value', 0), 0),
        '{{f_ciudad_3}}': str(datos_campana.get('facebook_city_3', 'Ciudad 3')),
        '{{f_ciudad_3_valor}}': formatear_numero(datos_campana.get('facebook_city_3_value', 0), 0),
        '{{f_ciudad_4}}': str(datos_campana.get('facebook_city_4', 'Ciudad 4')),
        '{{f_ciudad_4_valor}}': formatear_numero(datos_campana.get('facebook_city_4_value', 0), 0),
        '{{f_ciudad_5}}': str(datos_campana.get('facebook_city_5', 'Ciudad 5')),
        '{{f_ciudad_5_valor}}': formatear_numero(datos_campana.get('facebook_city_5_value', 0), 0),
        '{{f_top1_formato}}': str(datos_campana.get('facebook_top3_1_formato', 'Reel')),
        '{{f_top1_texto}}': str(datos_campana.get('facebook_top3_1_texto', 'Texto principal 1')),
        '{{f_top1_url}}': str(datos_campana.get('facebook_top3_1_url_imagen', 'https://example.com/imagen-1.jpg')),
        '{{f_top1_alcance}}': formatear_numero(datos_campana.get('facebook_top3_1_alcance', 0), 0),
        '{{f_top1_reacciones}}': formatear_numero(datos_campana.get('facebook_top3_1_reacciones', 0), 0),
        '{{f_top2_formato}}': str(datos_campana.get('facebook_top3_2_formato', 'Imagen')),
        '{{f_top2_texto}}': str(datos_campana.get('facebook_top3_2_texto', 'Texto principal 2')),
        '{{f_top2_url}}': str(datos_campana.get('facebook_top3_2_url_imagen', 'https://example.com/imagen-2.jpg')),
        '{{f_top2_alcance}}': formatear_numero(datos_campana.get('facebook_top3_2_alcance', 0), 0),
        '{{f_top2_reacciones}}': formatear_numero(datos_campana.get('facebook_top3_2_reacciones', 0), 0),
        '{{f_top3_formato}}': str(datos_campana.get('facebook_top3_3_formato', 'Carrusel')),
        '{{f_top3_texto}}': str(datos_campana.get('facebook_top3_3_texto', 'Texto principal 3')),
        '{{f_top3_url}}': str(datos_campana.get('facebook_top3_3_url_imagen', 'https://example.com/imagen-3.jpg')),
        '{{f_top3_alcance}}': formatear_numero(datos_campana.get('facebook_top3_3_alcance', 0), 0),
        '{{f_top3_reacciones}}': formatear_numero(datos_campana.get('facebook_top3_3_reacciones', 0), 0),
    }

    instagram = {
        '{{i_seguidores_total}}': formatear_numero(datos_campana.get('instagram_followers_total', 0), 0),
        '{{i_nuevos_seguidores}}': formatear_numero(datos_campana.get('instagram_new_followers', 0), 0),
        '{{i_impresiones}}': formatear_numero(datos_campana.get('instagram_impressions', 0), 0),
        '{{i_alcance}}': formatear_numero(datos_campana.get('instagram_reach', 0), 0),
        '{{i_interacciones}}': formatear_numero(datos_campana.get('instagram_interactions', 0), 0),
        '{{i_vistas}}': formatear_numero(datos_campana.get('instagram_views', 0), 0),
        '{{i_contenido_publicado}}': formatear_numero(datos_campana.get('instagram_content_published', 0), 0),
        '{{i_hombres}}': formatear_numero(datos_campana.get('instagram_gender_men', 0), 0),
        '{{i_mujeres}}': formatear_numero(datos_campana.get('instagram_gender_women', 0), 0),
        '{{i_18_24}}': formatear_numero(datos_campana.get('instagram_age_18_24', 0), 0),
        '{{i_25_34}}': formatear_numero(datos_campana.get('instagram_age_25_34', 0), 0),
        '{{i_35_44}}': formatear_numero(datos_campana.get('instagram_age_35_44', 0), 0),
        '{{i_45_54}}': formatear_numero(datos_campana.get('instagram_age_45_54', 0), 0),
        '{{i_55_64}}': formatear_numero(datos_campana.get('instagram_age_55_64', 0), 0),
        '{{i_65_mas}}': formatear_numero(datos_campana.get('instagram_age_65_plus', 0), 0),
        '{{i_ciudad_1}}': str(datos_campana.get('instagram_city_1', 'Ciudad 1')),
        '{{i_ciudad_1_valor}}': formatear_numero(datos_campana.get('instagram_city_1_value', 0), 0),
        '{{i_ciudad_2}}': str(datos_campana.get('instagram_city_2', 'Ciudad 2')),
        '{{i_ciudad_2_valor}}': formatear_numero(datos_campana.get('instagram_city_2_value', 0), 0),
        '{{i_ciudad_3}}': str(datos_campana.get('instagram_city_3', 'Ciudad 3')),
        '{{i_ciudad_3_valor}}': formatear_numero(datos_campana.get('instagram_city_3_value', 0), 0),
        '{{i_ciudad_4}}': str(datos_campana.get('instagram_city_4', 'Ciudad 4')),
        '{{i_ciudad_4_valor}}': formatear_numero(datos_campana.get('instagram_city_4_value', 0), 0),
        '{{i_ciudad_5}}': str(datos_campana.get('instagram_city_5', 'Ciudad 5')),
        '{{i_ciudad_5_valor}}': formatear_numero(datos_campana.get('instagram_city_5_value', 0), 0),
        '{{i_mapa_calor}}': str(datos_campana.get('instagram_mapa_calor_imagen', 'https://example.com/mapa-calor.jpg')),
        '{{i_top1_formato}}': str(datos_campana.get('instagram_top3_1_formato', 'Reel')),
        '{{i_top1_texto}}': str(datos_campana.get('instagram_top3_1_texto', 'Texto principal 1')),
        '{{i_top1_alcance}}': formatear_numero(datos_campana.get('instagram_top3_1_alcance', 0), 0),
        '{{i_top1_reacciones}}': formatear_numero(datos_campana.get('instagram_top3_1_reacciones', 0), 0),
        '{{i_top1_url}}': str(datos_campana.get('instagram_top3_1_url_imagen', 'https://example.com/instagram-1.jpg')),
        '{{i_top2_formato}}': str(datos_campana.get('instagram_top3_2_formato', 'Imagen')),
        '{{i_top2_texto}}': str(datos_campana.get('instagram_top3_2_texto', 'Texto principal 2')),
        '{{i_top2_alcance}}': formatear_numero(datos_campana.get('instagram_top3_2_alcance', 0), 0),
        '{{i_top2_reacciones}}': formatear_numero(datos_campana.get('instagram_top3_2_reacciones', 0), 0),
        '{{i_top2_url}}': str(datos_campana.get('instagram_top3_2_url_imagen', 'https://example.com/instagram-2.jpg')),
        '{{i_top3_formato}}': str(datos_campana.get('instagram_top3_3_formato', 'Carrusel')),
        '{{i_top3_texto}}': str(datos_campana.get('instagram_top3_3_texto', 'Texto principal 3')),
        '{{i_top3_alcance}}': formatear_numero(datos_campana.get('instagram_top3_3_alcance', 0), 0),
        '{{i_top3_reacciones}}': formatear_numero(datos_campana.get('instagram_top3_3_reacciones', 0), 0),
        '{{i_top3_url}}': str(datos_campana.get('instagram_top3_3_url_imagen', 'https://example.com/instagram-3.jpg')),
    }

    meta_ads = {
        '{{m_leads}}': formatear_numero(datos_campana.get('meta_leads', 0), 0),
        '{{m_costo_resultado}}': formatear_numero(datos_campana.get('meta_cost_per_result', 0), 2, mostrar_moneda=True),
        '{{m_importe_gastado_total}}': formatear_numero(datos_campana.get('meta_total_spend', 0), 2, mostrar_moneda=True),
        '{{m_gasto_total}}': formatear_numero(datos_campana.get('meta_total_spend', 0), 2, mostrar_moneda=True),
        '{{m_clicks_enlace}}': formatear_numero(datos_campana.get('meta_link_clicks', 0), 0),
        '{{m_interacciones}}': formatear_numero(datos_campana.get('meta_interactions', 0), 0),
        '{{m_alcance}}': formatear_numero(datos_campana.get('meta_reach', 0), 0),
        '{{m_impresiones_pagadas}}': formatear_numero(datos_campana.get('meta_paid_impressions', 0), 0),
    }

    base = {
        '{{nombre_empresa}}': datos_campana.get('company_name', 'Empresa'),
        '{{nombre_campana}}': datos_campana.get('campaign_name', 'Campaña'),
        '{{gasto}}': formatear_numero(datos_campana.get('spend', 0), 2, mostrar_moneda=True),
        '{{clics}}': formatear_numero(datos_campana.get('clicks', 0), 0),
        '{{ctr}}': formatear_numero(datos_campana.get('ctr', 0), 2) + '%',
        '{{impresiones}}': formatear_numero(datos_campana.get('impressions', 0), 0),
    }

    base.update(facebook)
    base.update(instagram)
    base.update(meta_ads)
    return base


# GENERACION  DEL ENLACE
def obtener_credenciales_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None
        else:
            creds = None

        if creds is None:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def obtener_datos_meta(account_id):
    token = os.getenv("META_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("No existe META_ACCESS_TOKEN en el archivo .env")

    if not account_id.startswith('act_'):
        account_id = f"act_{account_id}"

    url = f"https://graph.facebook.com/v19.0/{account_id}/insights"
    parametros = {'access_token': token, 'fields': 'campaign_name,spend,clicks,ctr,impressions', 'date_preset': 'last_30d', 'level': 'campaign'}

    respuesta_http = requests.get(url, params=parametros, timeout=30)
    respuesta = respuesta_http.json()
    if 'error' in respuesta:
        error = respuesta['error']
        raise RuntimeError(
            f"Meta rechazó la consulta ({error.get('code')}): {error.get('message')}"
        )

    if 'data' in respuesta and respuesta['data']:
        df = pd.DataFrame(respuesta['data'])
        fila = df.iloc[0].to_dict()
        fila['facebook_campaign_name'] = fila.get('campaign_name', 'Facebook')
        fila['facebook_spend'] = fila.get('spend', 0)
        fila['facebook_clicks'] = fila.get('clicks', 0)
        fila['facebook_ctr'] = fila.get('ctr', 0)
        fila['facebook_impressions'] = fila.get('impressions', 0)
        return fila

    print(f"Meta respondió sin campañas para {account_id} en los últimos 30 días.")
    return None


def copiar_plantilla(presentation_id, nombre_reporte):
    creds = obtener_credenciales_google()
    servicio_drive = build('drive', 'v3', credentials=creds)
    copia = servicio_drive.files().copy(
        fileId=presentation_id,
        body={'name': nombre_reporte},
        fields='id,name,webViewLink',
    ).execute()
    return copia


def renderizar_slide(presentation_id, datos_campana, nombre_reporte):
    creds = obtener_credenciales_google()
    servicio_slides = build('slides', 'v1', credentials=creds)
    copia = copiar_plantilla(presentation_id, nombre_reporte)

    marcadores = construir_marcadores_reporte(datos_campana)
    peticiones = [
        {'replaceAllText': {'containsText': {'text': marcador, 'matchCase': True}, 'replaceText': str(valor)}}
        for marcador, valor in marcadores.items()
    ]

    servicio_slides.presentations().batchUpdate(
        presentationId=copia['id'], body={'requests': peticiones}
    ).execute()
    return copia


def datos_demo_google():
    return {
        'company_name': 'Universal en Becas',
        'campaign_name': 'Prueba de automatización Google',
        'facebook_followers_total': 12500,
        'facebook_new_followers': 320,
        'facebook_reach': 84500,
        'instagram_followers_total': 18900,
        'instagram_new_followers': 450,
        'instagram_reach': 102300,
        'meta_leads': 37,
        'meta_cost_per_result': 12.50,
        'meta_total_spend': 462.50,
    }


if __name__ == "__main__":
    ID_PRESENTACION_SLIDES = "1G2-phuROq_Crjazr-x7XH6ZphOmN9eMXQnH6i8EJBFc"
    ID_CLIENTE_META = "act_792323499648312"

    print(" Iniciando Fábrica de Datos ETL...")
    if '--probar-google' in sys.argv:
        datos = datos_demo_google()
        nombre_reporte = 'PRUEBA Google - automatización de Slides'
    else:
        datos = obtener_datos_meta(ID_CLIENTE_META)
        nombre_reporte = f"Reporte Meta - {datos.get('campaign_name', 'Campaña')}" if datos else None

    if datos is not None:
        print(f" Datos transformados listos. Inyectando campaña '{datos['campaign_name']}' en Slides...")
        copia = renderizar_slide(ID_PRESENTACION_SLIDES, datos, nombre_reporte)
        print(f" ¡Éxito! Reporte creado: {copia.get('webViewLink', copia['id'])}")
    else:
        print(" No se encontraron datos para renderizar.")