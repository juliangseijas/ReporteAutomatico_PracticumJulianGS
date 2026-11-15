import pandas as pd

MARCADORES_IMAGEN = {
    "{{f_top1_url}}",
    "{{f_top2_url}}",
    "{{f_top3_url}}",
    "{{i_top1_url}}",
    "{{i_top2_url}}",
    "{{i_top3_url}}",
    "{{i_mapa_calor}}",
}


def formatear_numero(valor, decimales=2, mostrar_moneda=False):
    if valor is None:
        valor = 0

    if isinstance(valor, str):
        try:
            valor = float(valor) if ("." in valor or decimales > 0) else int(valor)
        except ValueError:
            return valor

    if mostrar_moneda:
        return (
            f"${valor:,.{decimales}f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    if isinstance(valor, float) or decimales > 0:
        return (
            f"{float(valor):,.{decimales}f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    return f"{int(valor):,}".replace(",", ".")


def simular_datos_meta():
    datos_json = [
        {
            "campaign_name": "Universal_en_Becas_Leads",
            "impressions": 15000,
            "clicks": 1359,
            "spend": 3961.17,
        },
        {
            "campaign_name": "Diplomados_Online_Tráfico",
            "impressions": 8500,
            "clicks": 210,
            "spend": 600.00,
        },
    ]
    return datos_json


def transformar_datos(datos_crudos):
    """
    Convierte una lista de diccionarios de campañas en un DataFrame de Pandas
    y calcula KPIs matemáticos (CTR %, CPC medio y Costo por Lead).
    """
    if not datos_crudos:
        return pd.DataFrame(
            columns=[
                "campaign_name",
                "impressions",
                "clicks",
                "spend",
                "ctr_porcentaje",
                "cpc_medio",
            ]
        )

    df = pd.DataFrame(datos_crudos).copy()

    for col in ("impressions", "clicks", "spend", "reach", "leads", "interactions"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Fórmula del CTR = (Clics / Impresiones) * 100
    df["ctr_porcentaje"] = df.apply(
        lambda r: (r["clicks"] / r["impressions"] * 100) if r.get("impressions", 0) > 0 else 0.0,
        axis=1,
    )

    # Fórmula del CPC = Costo / Clics
    df["cpc_medio"] = df.apply(
        lambda r: (r["spend"] / r["clicks"]) if r.get("clicks", 0) > 0 else 0.0,
        axis=1,
    )

    if "leads" in df.columns:
        df["cpl_medio"] = df.apply(
            lambda r: (r["spend"] / r["leads"]) if r.get("leads", 0) > 0 else 0.0,
            axis=1,
        )

    return df.round(2)


def construir_marcadores_reporte(datos_campana):
    """
    Construye el diccionario completo de marcadores {{...}} para inyectar en Google Slides.
    Incluye métricas de Facebook Orgánico, Instagram Orgánico, Meta Ads y metadatos generales.
    """
    facebook = {
        "{{f_seguidores_total}}": formatear_numero(datos_campana.get("facebook_followers_total", 0), 0),
        "{{f_nuevos_seguidores}}": formatear_numero(datos_campana.get("facebook_new_followers", 0), 0),
        "{{f_impresiones}}": formatear_numero(datos_campana.get("facebook_impressions", 0), 0),
        "{{f_alcance}}": formatear_numero(datos_campana.get("facebook_reach", 0), 0),
        "{{f_interacciones}}": formatear_numero(datos_campana.get("facebook_total_interactions", 0), 0),
        "{{f_vistas}}": formatear_numero(datos_campana.get("facebook_views", 0), 0),
        "{{f_clicks_enlace}}": formatear_numero(datos_campana.get("facebook_link_clicks", 0), 0),
        "{{f_contenido_publicado}}": formatear_numero(datos_campana.get("facebook_content_volume", 0), 0),
        "{{f_hombres}}": formatear_numero(datos_campana.get("facebook_gender_men", 0), 0),
        "{{f_mujeres}}": formatear_numero(datos_campana.get("facebook_gender_women", 0), 0),
        "{{f_18_24}}": formatear_numero(datos_campana.get("facebook_age_18_24", 0), 0),
        "{{f_25_34}}": formatear_numero(datos_campana.get("facebook_age_25_34", 0), 0),
        "{{f_35_44}}": formatear_numero(datos_campana.get("facebook_age_35_44", 0), 0),
        "{{f_45_54}}": formatear_numero(datos_campana.get("facebook_age_45_54", 0), 0),
        "{{f_55_64}}": formatear_numero(datos_campana.get("facebook_age_55_64", 0), 0),
        "{{f_65_mas}}": formatear_numero(datos_campana.get("facebook_age_65_plus", 0), 0),
        "{{f_ciudad_1}}": str(datos_campana.get("facebook_city_1", "Ciudad 1")),
        "{{f_ciudad_1_valor}}": formatear_numero(datos_campana.get("facebook_city_1_value", 0), 0),
        "{{f_ciudad_2}}": str(datos_campana.get("facebook_city_2", "Ciudad 2")),
        "{{f_ciudad_2_valor}}": formatear_numero(datos_campana.get("facebook_city_2_value", 0), 0),
        "{{f_ciudad_3}}": str(datos_campana.get("facebook_city_3", "Ciudad 3")),
        "{{f_ciudad_3_valor}}": formatear_numero(datos_campana.get("facebook_city_3_value", 0), 0),
        "{{f_ciudad_4}}": str(datos_campana.get("facebook_city_4", "Ciudad 4")),
        "{{f_ciudad_4_valor}}": formatear_numero(datos_campana.get("facebook_city_4_value", 0), 0),
        "{{f_ciudad_5}}": str(datos_campana.get("facebook_city_5", "Ciudad 5")),
        "{{f_ciudad_5_valor}}": formatear_numero(datos_campana.get("facebook_city_5_value", 0), 0),
        "{{f_top1_formato}}": str(datos_campana.get("facebook_top3_1_formato", "Reel")),
        "{{f_top1_texto}}": str(datos_campana.get("facebook_top3_1_texto", "Texto principal 1")),
        "{{f_top1_url}}": str(datos_campana.get("facebook_top3_1_url_imagen", "https://example.com/imagen-1.jpg")),
        "{{f_top1_alcance}}": formatear_numero(datos_campana.get("facebook_top3_1_alcance", 0), 0),
        "{{f_top1_reacciones}}": formatear_numero(datos_campana.get("facebook_top3_1_reacciones", 0), 0),
        "{{f_top2_formato}}": str(datos_campana.get("facebook_top3_2_formato", "Imagen")),
        "{{f_top2_texto}}": str(datos_campana.get("facebook_top3_2_texto", "Texto principal 2")),
        "{{f_top2_url}}": str(datos_campana.get("facebook_top3_2_url_imagen", "https://example.com/imagen-2.jpg")),
        "{{f_top2_alcance}}": formatear_numero(datos_campana.get("facebook_top3_2_alcance", 0), 0),
        "{{f_top2_reacciones}}": formatear_numero(datos_campana.get("facebook_top3_2_reacciones", 0), 0),
        "{{f_top3_formato}}": str(datos_campana.get("facebook_top3_3_formato", "Carrusel")),
        "{{f_top3_texto}}": str(datos_campana.get("facebook_top3_3_texto", "Texto principal 3")),
        "{{f_top3_url}}": str(datos_campana.get("facebook_top3_3_url_imagen", "https://example.com/imagen-3.jpg")),
        "{{f_top3_alcance}}": formatear_numero(datos_campana.get("facebook_top3_3_alcance", 0), 0),
        "{{f_top3_reacciones}}": formatear_numero(datos_campana.get("facebook_top3_3_reacciones", 0), 0),
    }

    instagram = {
        "{{i_seguidores_total}}": formatear_numero(datos_campana.get("instagram_followers_total", 0), 0),
        "{{i_nuevos_seguidores}}": formatear_numero(datos_campana.get("instagram_new_followers", 0), 0),
        "{{i_impresiones}}": formatear_numero(datos_campana.get("instagram_impressions", 0), 0),
        "{{i_alcance}}": formatear_numero(datos_campana.get("instagram_reach", 0), 0),
        "{{i_interacciones}}": formatear_numero(datos_campana.get("instagram_interactions", 0), 0),
        "{{i_vistas}}": formatear_numero(datos_campana.get("instagram_views", 0), 0),
        "{{i_contenido_publicado}}": formatear_numero(datos_campana.get("instagram_content_published", 0), 0),
        "{{i_hombres}}": formatear_numero(datos_campana.get("instagram_gender_men", 0), 0),
        "{{i_mujeres}}": formatear_numero(datos_campana.get("instagram_gender_women", 0), 0),
        "{{i_18_24}}": formatear_numero(datos_campana.get("instagram_age_18_24", 0), 0),
        "{{i_25_34}}": formatear_numero(datos_campana.get("instagram_age_25_34", 0), 0),
        "{{i_35_44}}": formatear_numero(datos_campana.get("instagram_age_35_44", 0), 0),
        "{{i_45_54}}": formatear_numero(datos_campana.get("instagram_age_45_54", 0), 0),
        "{{i_55_64}}": formatear_numero(datos_campana.get("instagram_age_55_64", 0), 0),
        "{{i_65_mas}}": formatear_numero(datos_campana.get("instagram_age_65_plus", 0), 0),
        "{{i_ciudad_1}}": str(datos_campana.get("instagram_city_1", "Ciudad 1")),
        "{{i_ciudad_1_valor}}": formatear_numero(datos_campana.get("instagram_city_1_value", 0), 0),
        "{{i_ciudad_2}}": str(datos_campana.get("instagram_city_2", "Ciudad 2")),
        "{{i_ciudad_2_valor}}": formatear_numero(datos_campana.get("instagram_city_2_value", 0), 0),
        "{{i_ciudad_3}}": str(datos_campana.get("instagram_city_3", "Ciudad 3")),
        "{{i_ciudad_3_valor}}": formatear_numero(datos_campana.get("instagram_city_3_value", 0), 0),
        "{{i_ciudad_4}}": str(datos_campana.get("instagram_city_4", "Ciudad 4")),
        "{{i_ciudad_4_valor}}": formatear_numero(datos_campana.get("instagram_city_4_value", 0), 0),
        "{{i_ciudad_5}}": str(datos_campana.get("instagram_city_5", "Ciudad 5")),
        "{{i_ciudad_5_valor}}": formatear_numero(datos_campana.get("instagram_city_5_value", 0), 0),
        "{{i_mapa_calor}}": str(datos_campana.get("instagram_mapa_calor_imagen", "https://example.com/mapa-calor.jpg")),
        "{{i_top1_formato}}": str(datos_campana.get("instagram_top3_1_formato", "Reel")),
        "{{i_top1_texto}}": str(datos_campana.get("instagram_top3_1_texto", "Texto principal 1")),
        "{{i_top1_alcance}}": formatear_numero(datos_campana.get("instagram_top3_1_alcance", 0), 0),
        "{{i_top1_reacciones}}": formatear_numero(datos_campana.get("instagram_top3_1_reacciones", 0), 0),
        "{{i_top1_url}}": str(datos_campana.get("instagram_top3_1_url_imagen", "https://example.com/instagram-1.jpg")),
        "{{i_top2_formato}}": str(datos_campana.get("instagram_top3_2_formato", "Imagen")),
        "{{i_top2_texto}}": str(datos_campana.get("instagram_top3_2_texto", "Texto principal 2")),
        "{{i_top2_alcance}}": formatear_numero(datos_campana.get("instagram_top3_2_alcance", 0), 0),
        "{{i_top2_reacciones}}": formatear_numero(datos_campana.get("instagram_top3_2_reacciones", 0), 0),
        "{{i_top2_url}}": str(datos_campana.get("instagram_top3_2_url_imagen", "https://example.com/instagram-2.jpg")),
        "{{i_top3_formato}}": str(datos_campana.get("instagram_top3_3_formato", "Carrusel")),
        "{{i_top3_texto}}": str(datos_campana.get("instagram_top3_3_texto", "Texto principal 3")),
        "{{i_top3_alcance}}": formatear_numero(datos_campana.get("instagram_top3_3_alcance", 0), 0),
        "{{i_top3_reacciones}}": formatear_numero(datos_campana.get("instagram_top3_3_reacciones", 0), 0),
        "{{i_top3_url}}": str(datos_campana.get("instagram_top3_3_url_imagen", "https://example.com/instagram-3.jpg")),
    }

    meta_ads = {
        "{{m_leads}}": formatear_numero(datos_campana.get("meta_leads", 0), 0),
        "{{m_costo_resultado}}": formatear_numero(datos_campana.get("meta_cost_per_result", 0), 2, mostrar_moneda=True),
        "{{m_importe_gastado_total}}": formatear_numero(datos_campana.get("meta_total_spend", 0), 2, mostrar_moneda=True),
        "{{m_gasto_total}}": formatear_numero(datos_campana.get("meta_total_spend", 0), 2, mostrar_moneda=True),
        "{{m_clicks_enlace}}": formatear_numero(datos_campana.get("meta_link_clicks", 0), 0),
        "{{m_interacciones}}": formatear_numero(datos_campana.get("meta_interactions", 0), 0),
        "{{m_alcance}}": formatear_numero(datos_campana.get("meta_reach", 0), 0),
        "{{m_impresiones_pagadas}}": formatear_numero(datos_campana.get("meta_paid_impressions", 0), 0),
    }

    base = {
        "{{nombre_empresa}}": str(datos_campana.get("company_name", "Empresa")),
        "{{nombre_campana}}": str(datos_campana.get("campaign_name", "Campaña")),
        "{{periodo_reporte}}": str(datos_campana.get("periodo_reporte", "Mensual")),
        "{{gasto}}": formatear_numero(datos_campana.get("spend", 0), 2, mostrar_moneda=True),
        "{{clics}}": formatear_numero(datos_campana.get("clicks", 0), 0),
        "{{ctr}}": formatear_numero(datos_campana.get("ctr", 0), 2) + "%",
        "{{impresiones}}": formatear_numero(datos_campana.get("impressions", 0), 0),
    }

    base.update(facebook)
    base.update(instagram)
    base.update(meta_ads)
    return base


def extraer_marcadores_imagen_validos(marcadores):
    """
    Filtra los marcadores de imagen que contienen una URL pública válida (no example.com)
    para poder inyectarlos como imágenes mediante replaceAllShapesWithImage en Google Slides.
    """
    imagenes = {}
    for marcador in MARCADORES_IMAGEN:
        url = str(marcadores.get(marcador, "")).strip()
        if (
            url.startswith(("http://", "https://"))
            and "example.com" not in url
        ):
            imagenes[marcador] = url
    return imagenes


if __name__ == "__main__":
    datos_simulados = simular_datos_meta()
    tabla_limpia = transformar_datos(datos_simulados)

    print("\n=== Tabla Transformada y Lista para el Reporte ===")
    print(tabla_limpia)