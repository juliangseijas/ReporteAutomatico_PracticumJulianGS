import pandas as pd
try:
    from src.extract import extraer_insights_ads, generar_datos_demo_completos
except ImportError:
    from extract import extraer_insights_ads, generar_datos_demo_completos


def extraer_metricas_campanas(account_id="act_792323499648312", fecha_inicio=None, fecha_fin=None):
    print(f"\nExtrayendo metricas de la cuenta: {account_id}...")
    try:
        lista_campanas = extraer_insights_ads(
            account_id=account_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )
        if lista_campanas:
            df = pd.DataFrame(lista_campanas)
            print("\nTABLA TRANSFORMADA POR PANDAS (Lista para el reporte):")
            print(df.to_string(index=False))
            return df
        else:
            print("No se encontraron campañas activas en el periodo consultado.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Aviso de conexión con Meta API: {e}")
        print("Mostrando tabla de campañas simuladas (Modo Demo):")
        df_demo = pd.DataFrame(generar_datos_demo_completos()["campanas"])
        print(df_demo.to_string(index=False))
        return df_demo


if __name__ == "__main__":
    extraer_metricas_campanas("act_792323499648312")