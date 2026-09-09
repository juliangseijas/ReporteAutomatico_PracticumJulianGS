import os
import requests
import pandas as pd  # <-- Agregamos Pandas aquí
from dotenv import load_dotenv

load_dotenv()

# ... (deja tu función listar_clientes_meta exactamente igual) ...

def extraer_metricas_campanas(account_id):
    token = os.getenv("META_ACCESS_TOKEN")
    
    if not account_id.startswith('act_'):
        account_id = f"act_{account_id}"

    print(f"\n📡 Extrayendo métricas de la cuenta: {account_id}...")
    url = f"https://graph.facebook.com/v19.0/{account_id}/insights"
    
    parametros = {
        'access_token': token,
        'fields': 'campaign_name,spend,impressions,clicks,ctr',
        'date_preset': 'last_30d', 
        'level': 'campaign'        
    }
    
    try:
        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()
        
        if 'error' in datos:
            print(f"Meta rechazó la petición: {datos['error']['message']}")
            return

        # LA MAGIA DE PANDAS COMIENZA AQUÍ
        lista_campanas = datos.get('data', [])
        
        if lista_campanas:
            # Convertimos el JSON crudo en una tabla estructurada (DataFrame)
            df = pd.DataFrame(lista_campanas)
            print("\nTABLA TRANSFORMADA POR PANDAS (Lista para el reporte):")
            print(df.to_string(index=False))
        else:
            print("No se encontraron campañas activas en los últimos 30 días.")
            
    except Exception as e:
        print(f"Ocurrió un error en el sistema: {e}")

if __name__ == "__main__":
    # Puedes dejar listados los clientes si quieres, o comentarlo con un #
    # listar_clientes_meta() 
    
    extraer_metricas_campanas("act_792323499648312") # Asegúrate de tener aquí tu ID real