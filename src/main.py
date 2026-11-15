import argparse
import sys

try:
    from src.config import Config
    from src.extract import (
        extraer_datos_completos_cliente,
        generar_datos_demo_completos,
    )
    from src.transform import (
        formatear_numero,
        construir_marcadores_reporte,
        transformar_datos,
    )
    from src.load import (
        SCOPES,
        obtener_credenciales_google,
        copiar_plantilla,
        renderizar_slide,
    )
except ImportError:
    from config import Config
    from extract import (
        extraer_datos_completos_cliente,
        generar_datos_demo_completos,
    )
    from transform import (
        formatear_numero,
        construir_marcadores_reporte,
        transformar_datos,
    )
    from load import (
        SCOPES,
        obtener_credenciales_google,
        copiar_plantilla,
        renderizar_slide,
    )


def datos_demo_google(nombre_cliente="Universal en Becas", fecha_inicio=None, fecha_fin=None):
    """Retorna el set completo de datos demo para pruebas de automatización en Google Slides."""
    return generar_datos_demo_completos(
        nombre_cliente=nombre_cliente,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


def obtener_datos_meta(
    account_id,
    fecha_inicio=None,
    fecha_fin=None,
    nombre_cliente="Universal en Becas",
    permitir_fallback=False,
):
    """
    Obtiene los datos de Meta Ads y orgánicos para una cuenta publicitaria y rango de fechas.
    """
    return extraer_datos_completos_cliente(
        nombre_cliente=nombre_cliente,
        account_id=account_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        usar_demo=False,
        permitir_fallback=permitir_fallback,
    )


def ejecutar_pipeline_reporte(
    cliente="Universal en Becas",
    fecha_inicio=None,
    fecha_fin=None,
    usar_demo=False,
    permitir_fallback=True,
    presentation_id=None,
    account_id=None,
    generar_slides=True,
    inyectar_imagenes=True,
):
    """
    Orquesta el pipeline ETL completo:
      1. Extract: Obtiene métricas de Meta Ads + Facebook Orgánico + Instagram Orgánico (o Demo).
      2. Transform: Calcula KPIs con Pandas y construye todos los marcadores {{...}}.
      3. Load: Clona la plantilla en Google Drive e inyecta textos e imágenes en Google Slides.
    """
    cfg_cliente = Config.obtener_cliente(cliente)
    presentation_id = presentation_id or cfg_cliente["presentation_id"]
    account_id = account_id or cfg_cliente["ad_account_id"]

    # 1. EXTRACT
    datos = extraer_datos_completos_cliente(
        nombre_cliente=cliente,
        account_id=account_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        usar_demo=usar_demo,
        permitir_fallback=permitir_fallback,
    )

    if datos is None:
        return {
            "exito": False,
            "mensaje": "No se encontraron datos para el periodo seleccionado.",
            "datos": None,
            "tabla_campanas": None,
            "marcadores": None,
            "copia_slides": None,
        }

    # 2. TRANSFORM
    tabla_campanas = transformar_datos(datos.get("campanas", []))
    marcadores = construir_marcadores_reporte(datos)

    periodo_etiqueta = (
        f"{fecha_inicio} a {fecha_fin}"
        if (fecha_inicio and fecha_fin)
        else datos.get("periodo_reporte", "Mensual")
    )
    nombre_reporte = f"Reporte Social Media • {cfg_cliente['company_name']} ({periodo_etiqueta})"

    # 3. LOAD
    copia_slides = None
    if generar_slides:
        copia_slides = renderizar_slide(
            presentation_id=presentation_id,
            datos_campana=datos,
            nombre_reporte=nombre_reporte,
            inyectar_imagenes=inyectar_imagenes,
        )

    return {
        "exito": True,
        "nombre_reporte": nombre_reporte,
        "datos": datos,
        "tabla_campanas": tabla_campanas,
        "marcadores": marcadores,
        "copia_slides": copia_slides,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fábrica de Datos ETL - Generador Automatizado de Reportes Monstruo Canela"
    )
    parser.add_argument(
        "--cliente",
        default="Universal en Becas",
        help="Nombre del cliente (ej. 'Universal en Becas', 'Distrito Financiero')",
    )
    parser.add_argument("--inicio", default=None, help="Fecha de inicio (YYYY-MM-DD)")
    parser.add_argument("--fin", default=None, help="Fecha de fin (YYYY-MM-DD)")
    parser.add_argument(
        "--probar-google",
        action="store_true",
        help="Usar datos demo completos y generar la presentación en Google Slides",
    )
    parser.add_argument(
        "--solo-extraer",
        action="store_true",
        help="Ejecutar únicamente Extracción y Transformación sin conectar a Google Slides",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("Iniciando Fabrica de Datos ETL...")
    resultado = ejecutar_pipeline_reporte(
        cliente=args.cliente,
        fecha_inicio=args.inicio,
        fecha_fin=args.fin,
        usar_demo=args.probar_google,
        permitir_fallback=True,
        generar_slides=not args.solo_extraer,
    )

    if resultado["exito"]:
        datos = resultado["datos"]
        if datos.get("aviso_api"):
            print(f"[AVISO] {datos['aviso_api']}")
        print(f"[OK] Datos transformados listos para '{datos['company_name']}'.")
        print("\n--- Tabla de Campañas (Pandas) ---")
        print(resultado["tabla_campanas"].to_string(index=False))

        if resultado["copia_slides"]:
            copia = resultado["copia_slides"]
            print(f"\n[EXITO] Reporte creado en Google Slides: {copia.get('webViewLink', copia['id'])}")
    else:
        print(f"[ERROR] {resultado.get('mensaje', 'No se encontraron datos para renderizar.')}")
        sys.exit(1)