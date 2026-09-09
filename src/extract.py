import requests
from config import Config

def extraer_datos_meta():
    print("Iniciando protocolo de conexión con Meta Marketing API...")
    
    # Revisamos si ya tenemos el Token en nuestro archivo .env
    token = Config.META_ACCESS_TOKEN
    
    if not token:
        print("Credenciales no detectadas. Usando datos simulados (Mock Data) para continuar el desarrollo.")
        # Retornamos los datos falsos para que el proceso no se detenga
        return [
            {"campaign_name": "Universal_en_Becas_Leads", "impressions": 15000, "clicks": 1359, "spend": 3961.17},
            {"campaign_name": "Diplomados_Online_Tráfico", "impressions": 8500, "clicks": 210, "spend": 600.00}
        ]
    
    # --- A PARTIR DE AQUÍ ES EL CÓDIGO REAL QUE FUNCIONARÁ CUANDO TENGAS EL TOKEN ---
    print("Token detectado. Conectando a los servidores de Meta...")
    
    # Aquí irá el ID de la cuenta publicitaria de Monstruo Canela (lo pondremos después)
    cuenta_id = "act_TU_ID_DE_CUENTA"
    url = f"https://graph.facebook.com/v19.0/{cuenta_id}/insights"
    
    # Parámetros exactos que le pediremos a la API (Impresiones, Clics, Gasto)
    parametros = {
        "access_token": token,
        "fields": "campaign_name,impressions,clicks,spend",
        "date_preset": "last_month" # Trae los datos del mes pasado automáticamente
    }
    
    try:
        # Hacemos la petición oficial a Meta
        respuesta = requests.get(url, params=parametros)
        respuesta.raise_for_status() # Nos avisa si Meta rechaza la conexión
        
        datos_reales = respuesta.json()
        return datos_reales.get("data", [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Meta: {e}")
        return []

# Prueba individual del módulo
if __name__ == "__main__":
    datos = extraer_datos_meta()
    print("\nDatos extraídos exitosamente:")
    print(datos)