import pandas as pd

def simular_datos_meta():
    # Este es el formato JSON exacto que nos entregará la API de Meta
    datos_json = [
        {"campaign_name": "Universal_en_Becas_Leads", "impressions": 15000, "clicks": 1359, "spend": 3961.17},
        {"campaign_name": "Diplomados_Online_Tráfico", "impressions": 8500, "clicks": 210, "spend": 600.00}
    ]
    return datos_json

def transformar_datos(datos_crudos):
    print("Aplanando el JSON a un DataFrame (Tabla) de Pandas...")
    df = pd.DataFrame(datos_crudos)
    
    print("Calculando KPIs matemáticos (CTR y CPC Medio)...")
    # Fórmula del CTR = (Clics / Impresiones) * 100
    df['ctr_porcentaje'] = (df['clicks'] / df['impressions']) * 100
    
    # Fórmula del CPC = Costo / Clics
    df['cpc_medio'] = df['spend'] / df['clicks']
    
    # Redondear a 2 decimales para que se vea bien en el reporte
    df = df.round(2)
    
    return df

# Prueba rápida del archivo
if __name__ == "__main__":
    datos_simulados = simular_datos_meta()
    tabla_limpia = transformar_datos(datos_simulados)
    
    print("\n=== Tabla Transformada y Lista para el Reporte ===")
    print(tabla_limpia)