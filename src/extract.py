import json
import datetime
import requests
try:
    from src.config import Config
except ImportError:
    from config import Config


def _construir_rango_fechas(fecha_inicio=None, fecha_fin=None, date_preset="last_30d"):
    """Construye los parámetros de fecha para la Graph API de Meta."""
    if fecha_inicio and fecha_fin:
        inicio_str = (
            fecha_inicio.strftime("%Y-%m-%d")
            if isinstance(fecha_inicio, (datetime.date, datetime.datetime))
            else str(fecha_inicio)
        )
        fin_str = (
            fecha_fin.strftime("%Y-%m-%d")
            if isinstance(fecha_fin, (datetime.date, datetime.datetime))
            else str(fecha_fin)
        )
        return {"time_range": json.dumps({"since": inicio_str, "until": fin_str})}
    return {"date_preset": date_preset}


def generar_datos_demo_completos(
    nombre_cliente="Universal en Becas",
    fecha_inicio=None,
    fecha_fin=None,
):
    """
    Genera un conjunto completo de datos simulados (basado en el reporte oficial de
    Universal en Becas) con métricas de Facebook Orgánico, Instagram Orgánico y Meta Ads.
    """
    periodo_str = "Julio 2026"
    if fecha_inicio and fecha_fin:
        periodo_str = f"{fecha_inicio} al {fecha_fin}"

    campanas_raw = [
        {
            "campaign_name": f"{nombre_cliente.replace(' ', '_')}_Leads",
            "impressions": 64812,
            "reach": 33155,
            "clicks": 1359,
            "inline_link_clicks": 295,
            "spend": 5224.83,
            "ctr": 2.10,
            "leads": 45,
            "interactions": 12420,
        },
        {
            "campaign_name": f"{nombre_cliente.replace(' ', '_')}_Reconocimiento_y_Tráfico",
            "impressions": 30000,
            "reach": 15200,
            "clicks": 540,
            "inline_link_clicks": 110,
            "spend": 2200.00,
            "ctr": 1.80,
            "leads": 17,
            "interactions": 6116,
        },
    ]

    total_spend = sum(c["spend"] for c in campanas_raw)
    total_impressions = sum(c["impressions"] for c in campanas_raw)
    total_reach = sum(c["reach"] for c in campanas_raw)
    total_clicks = sum(c["clicks"] for c in campanas_raw)
    total_link_clicks = sum(c["inline_link_clicks"] for c in campanas_raw)
    total_leads = sum(c["leads"] for c in campanas_raw)
    total_interactions = sum(c["interactions"] for c in campanas_raw)
    ctr_global = round((total_clicks / total_impressions) * 100, 2) if total_impressions else 0.0
    costo_por_lead = round(total_spend / total_leads, 2) if total_leads else 0.0

    return {
        "origen_datos": "demo",
        "periodo_reporte": periodo_str,
        "company_name": nombre_cliente,
        "campaign_name": campanas_raw[0]["campaign_name"],
        "spend": total_spend,
        "clicks": total_clicks,
        "ctr": ctr_global,
        "impressions": total_impressions,
        "campanas": campanas_raw,
        # Facebook Orgánico (basado en páginas 2-4 del PDF de referencia)
        "facebook_followers_total": 3987,
        "facebook_new_followers": 6,
        "facebook_impressions": 2903,
        "facebook_reach": 1935,
        "facebook_total_interactions": 83,
        "facebook_views": 393,
        "facebook_link_clicks": 127,
        "facebook_content_volume": 25,
        "facebook_gender_men": 28.1,
        "facebook_gender_women": 71.9,
        "facebook_age_18_24": 1.1,
        "facebook_age_25_34": 16.8,
        "facebook_age_35_44": 41.0,
        "facebook_age_45_54": 24.1,
        "facebook_age_55_64": 9.7,
        "facebook_age_65_plus": 7.3,
        "facebook_city_1": "Puebla de Zaragoza",
        "facebook_city_1_value": 809,
        "facebook_city_2": "Ciudad de México",
        "facebook_city_2_value": 374,
        "facebook_city_3": "Chihuahua",
        "facebook_city_3_value": 69,
        "facebook_city_4": "Ciudad Juárez",
        "facebook_city_4_value": 55,
        "facebook_city_5": "Querétaro",
        "facebook_city_5_value": 51,
        "facebook_top3_1_formato": "Reel",
        "facebook_top3_1_texto": "Si tu hijo aún no entra a primaria",
        "facebook_top3_1_url_imagen": "https://placehold.co/600x800/76b5a9/ffffff.png?text=FB+Top+1+Reel",
        "facebook_top3_1_alcance": 331,
        "facebook_top3_1_reacciones": 4,
        "facebook_top3_2_formato": "Reel",
        "facebook_top3_2_texto": "¿Una aportación pequeña realmente puede cambiar el futuro?",
        "facebook_top3_2_url_imagen": "https://placehold.co/600x800/76b5a9/ffffff.png?text=FB+Top+2+Reel",
        "facebook_top3_2_alcance": 297,
        "facebook_top3_2_reacciones": 5,
        "facebook_top3_3_formato": "Reel",
        "facebook_top3_3_texto": "Hoy es pequeño, pero sus sueños ya están creciendo",
        "facebook_top3_3_url_imagen": "https://placehold.co/600x800/76b5a9/ffffff.png?text=FB+Top+3+Reel",
        "facebook_top3_3_alcance": 279,
        "facebook_top3_3_reacciones": 1,
        # Instagram Orgánico (basado en páginas 5-8 del PDF de referencia)
        "instagram_followers_total": 2332,
        "instagram_new_followers": 11,
        "instagram_impressions": 2020,
        "instagram_reach": 500,
        "instagram_interactions": 79,
        "instagram_views": 37,
        "instagram_content_published": 25,
        "instagram_gender_men": 38.7,
        "instagram_gender_women": 61.3,
        "instagram_age_18_24": 4.9,
        "instagram_age_25_34": 31.5,
        "instagram_age_35_44": 35.2,
        "instagram_age_45_54": 19.0,
        "instagram_age_55_64": 6.7,
        "instagram_age_65_plus": 2.7,
        "instagram_city_1": "Puebla de Zaragoza",
        "instagram_city_1_value": 214,
        "instagram_city_2": "Ciudad de México",
        "instagram_city_2_value": 158,
        "instagram_city_3": "Santiago de Chile",
        "instagram_city_3_value": 79,
        "instagram_city_4": "Querétaro",
        "instagram_city_4_value": 41,
        "instagram_city_5": "Tlaxcalancingo, Puebla",
        "instagram_city_5_value": 30,
        "instagram_mapa_calor_imagen": "https://placehold.co/900x450/76b5a9/ffffff.png?text=Mapa+de+Calor+IG",
        "instagram_top3_1_formato": "Reel",
        "instagram_top3_1_texto": "Papá, mamá, ¿también sientes que tu hijo creció en un abrir y cerrar de ojos?",
        "instagram_top3_1_alcance": 272,
        "instagram_top3_1_reacciones": 3,
        "instagram_top3_1_url_imagen": "https://placehold.co/600x800/d96b38/ffffff.png?text=IG+Top+1+Reel",
        "instagram_top3_2_formato": "Imagen",
        "instagram_top3_2_texto": "¿Ya pensaste cómo te gustaría apoyar la educación de tu hijo?",
        "instagram_top3_2_alcance": 215,
        "instagram_top3_2_reacciones": 3,
        "instagram_top3_2_url_imagen": "https://placehold.co/600x800/d96b38/ffffff.png?text=IG+Top+2+Imagen",
        "instagram_top3_3_formato": "Imagen",
        "instagram_top3_3_texto": "¡Anáhuac Puebla se une a nuestra red de convenios!",
        "instagram_top3_3_alcance": 199,
        "instagram_top3_3_reacciones": 1,
        "instagram_top3_3_url_imagen": "https://placehold.co/600x800/d96b38/ffffff.png?text=IG+Top+3+Imagen",
        # Meta Ads (basado en página 9 del PDF de referencia)
        "meta_leads": total_leads,
        "meta_cost_per_result": costo_por_lead,
        "meta_total_spend": total_spend,
        "meta_link_clicks": total_link_clicks,
        "meta_interactions": total_interactions,
        "meta_reach": total_reach,
        "meta_paid_impressions": total_impressions,
    }


def _extraer_accion(lista_acciones, tipos_objetivo):
    """
    Extrae el valor del primer action_type que coincida según el orden de prioridad
    en 'tipos_objetivo', evitando duplicar conteos cuando Meta devuelve tanto 'lead'
    como 'onsite_conversion.lead_grouped'.
    """
    if not isinstance(lista_acciones, list):
        return 0
    mapa = {}
    for item in lista_acciones:
        tipo = item.get("action_type")
        if tipo:
            try:
                mapa[tipo] = float(item.get("value", 0))
            except (TypeError, ValueError):
                pass
    for tipo_prioritario in tipos_objetivo:
        if tipo_prioritario in mapa:
            return int(round(mapa[tipo_prioritario]))
    return 0


def extraer_insights_ads(account_id, fecha_inicio=None, fecha_fin=None, token=None):
    """
    Extrae métricas de campañas pagadas desde Meta Marketing API (/act_<id>/insights).
    """
    token = token or Config.META_ACCESS_TOKEN
    if not token:
        raise RuntimeError("No existe META_ACCESS_TOKEN en el archivo .env")

    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"

    url = f"https://graph.facebook.com/{Config.META_API_VERSION}/{account_id}/insights"
    parametros = {
        "access_token": token,
        "fields": (
            "campaign_name,spend,impressions,reach,clicks,"
            "inline_link_clicks,ctr,cpc,actions,cost_per_action_type"
        ),
        "level": "campaign",
    }
    parametros.update(_construir_rango_fechas(fecha_inicio, fecha_fin, date_preset="last_30d"))

    respuesta_http = requests.get(url, params=parametros, timeout=30)
    respuesta = respuesta_http.json()

    if "error" in respuesta:
        error = respuesta["error"]
        raise RuntimeError(
            f"Meta rechazó la consulta ({error.get('code')}): {error.get('message')}"
        )

    campanas = respuesta.get("data", [])
    if not campanas:
        return None

    campanas_procesadas = []
    for c in campanas:
        acciones = c.get("actions", [])
        leads = _extraer_accion(
            acciones,
            ["lead", "onsite_conversion.lead_grouped", "offsite_conversion.fb_pixel_lead"],
        )
        interacciones = _extraer_accion(
            acciones,
            ["post_engagement", "page_engagement"],
        )
        spend = float(c.get("spend", 0) or 0)
        impressions = int(float(c.get("impressions", 0) or 0))
        reach = int(float(c.get("reach", 0) or 0))
        clicks = int(float(c.get("clicks", 0) or 0))
        link_clicks = int(float(c.get("inline_link_clicks", clicks) or 0))
        ctr = float(c.get("ctr", 0) or 0)

        campanas_procesadas.append(
            {
                "campaign_name": c.get("campaign_name", "Campaña Meta"),
                "spend": spend,
                "impressions": impressions,
                "reach": reach,
                "clicks": clicks,
                "inline_link_clicks": link_clicks,
                "ctr": ctr,
                "leads": leads,
                "interactions": interacciones,
            }
        )

    return campanas_procesadas


def _parsear_demografia_meta(mapa_genero_edad, prefijo):
    """
    Convierte un diccionario tipo {'F.25-34': 120, 'M.35-44': 80, ...} en porcentajes
    para hombres, mujeres y rangos de edad (18-24, 25-34, 35-44, 45-54, 55-64, 65+).
    """
    if not isinstance(mapa_genero_edad, dict) or not mapa_genero_edad:
        return {}
    total = sum(float(v or 0) for v in mapa_genero_edad.values())
    if total <= 0:
        return {}

    hombres = 0.0
    mujeres = 0.0
    edades = {
        "18-24": 0.0,
        "25-34": 0.0,
        "35-44": 0.0,
        "45-54": 0.0,
        "55-64": 0.0,
        "65+": 0.0,
    }

    for clave, valor in mapa_genero_edad.items():
        val = float(valor or 0)
        partes = str(clave).split(".")
        genero = partes[0].upper() if len(partes) > 1 else ""
        rango = partes[-1]
        if genero == "M":
            hombres += val
        elif genero == "F":
            mujeres += val
        if rango in edades:
            edades[rango] += val

    return {
        f"{prefijo}_gender_men": round((hombres / total) * 100, 1),
        f"{prefijo}_gender_women": round((mujeres / total) * 100, 1),
        f"{prefijo}_age_18_24": round((edades["18-24"] / total) * 100, 1),
        f"{prefijo}_age_25_34": round((edades["25-34"] / total) * 100, 1),
        f"{prefijo}_age_35_44": round((edades["35-44"] / total) * 100, 1),
        f"{prefijo}_age_45_54": round((edades["45-54"] / total) * 100, 1),
        f"{prefijo}_age_55_64": round((edades["55-64"] / total) * 100, 1),
        f"{prefijo}_age_65_plus": round((edades["65+"] / total) * 100, 1),
    }


def _parsear_top_ciudades(mapa_ciudades, prefijo):
    """Extrae el Top 5 de ciudades ordenadas de mayor a menor audiencia."""
    if not isinstance(mapa_ciudades, dict) or not mapa_ciudades:
        return {}
    ordenadas = sorted(
        mapa_ciudades.items(),
        key=lambda kv: float(kv[1] or 0),
        reverse=True,
    )[:5]
    salida = {}
    for idx, (ciudad, valor) in enumerate(ordenadas, start=1):
        nombre_limpio = str(ciudad).split(",")[0].strip()
        salida[f"{prefijo}_city_{idx}"] = nombre_limpio
        salida[f"{prefijo}_city_{idx}_value"] = int(float(valor or 0))
    return salida


def extraer_insights_organicos_pagina(
    page_id=None,
    ig_account_id=None,
    fecha_inicio=None,
    fecha_fin=None,
    token=None,
):
    """
    Extrae métricas orgánicas completas de Facebook Page e Instagram Business Account
    (seguidores, impresiones, alcance, interacciones, vistas, demografía, top 5 ciudades
    y top 3 publicaciones).
    """
    token = token or Config.META_ACCESS_TOKEN
    if not token:
        return {}

    resultado = {}
    base_url = f"https://graph.facebook.com/{Config.META_API_VERSION}"
    params_fecha = {}
    if fecha_inicio and fecha_fin:
        params_fecha["since"] = str(fecha_inicio)
        params_fecha["until"] = str(fecha_fin)

    try:
        page_token = token
        # Si no se especificó page_id, intentamos descubrir la primera página asociada al token
        if not page_id:
            resp_pages = requests.get(
                f"{base_url}/me/accounts",
                params={
                    "access_token": token,
                    "fields": "id,name,access_token,fan_count,followers_count,instagram_business_account",
                },
                timeout=15,
            ).json()
            paginas = resp_pages.get("data", [])
            if paginas:
                primera = paginas[0]
                page_id = primera.get("id")
                page_token = primera.get("access_token", token)
                resultado["facebook_followers_total"] = primera.get(
                    "followers_count", primera.get("fan_count", 0)
                )
                if not ig_account_id and "instagram_business_account" in primera:
                    ig_account_id = primera["instagram_business_account"].get("id")

        if page_id:
            info_page = requests.get(
                f"{base_url}/{page_id}",
                params={
                    "access_token": page_token,
                    "fields": "name,fan_count,followers_count,posts.limit(15){message,full_picture,shares,reactions.summary(true),attachments{media_type}}",
                },
                timeout=15,
            ).json()
            if "error" not in info_page:
                if info_page.get("access_token"):
                    page_token = info_page["access_token"]
                resultado["facebook_followers_total"] = info_page.get(
                    "followers_count", info_page.get("fan_count", 0)
                )
                posts = info_page.get("posts", {}).get("data", [])
                resultado["facebook_content_volume"] = len(posts)
                posts_ordenados = sorted(
                    posts,
                    key=lambda p: p.get("reactions", {}).get("summary", {}).get("total_count", 0),
                    reverse=True,
                )
                for idx, post in enumerate(posts_ordenados[:3], start=1):
                    reacciones = (
                        post.get("reactions", {}).get("summary", {}).get("total_count", 0)
                    )
                    adjuntos = post.get("attachments", {}).get("data", [])
                    formato = adjuntos[0].get("media_type", "Post").capitalize() if adjuntos else "Post"
                    resultado[f"facebook_top3_{idx}_formato"] = formato
                    resultado[f"facebook_top3_{idx}_texto"] = (post.get("message") or f"Publicación #{idx}")[:90]
                    if post.get("full_picture"):
                        resultado[f"facebook_top3_{idx}_url_imagen"] = post["full_picture"]
                    resultado[f"facebook_top3_{idx}_reacciones"] = reacciones

            # Insights diarios de Página de Facebook (impresiones, alcance, interacciones, vistas, nuevos seguidores)
            fb_metrics = (
                "page_impressions,page_impressions_unique,page_post_engagements,"
                "page_video_views,page_daily_follows_unique"
            )
            resp_fb_ins = requests.get(
                f"{base_url}/{page_id}/insights",
                params={"access_token": page_token, "metric": fb_metrics, "period": "day", **params_fecha},
                timeout=15,
            ).json()
            for item in resp_fb_ins.get("data", []):
                nombre_m = item.get("name")
                suma_val = sum(
                    int(float(v.get("value", 0) or 0))
                    for v in item.get("values", [])
                    if isinstance(v.get("value"), (int, float, str))
                )
                if nombre_m == "page_impressions":
                    resultado["facebook_impressions"] = suma_val
                elif nombre_m == "page_impressions_unique":
                    resultado["facebook_reach"] = suma_val
                elif nombre_m == "page_post_engagements":
                    resultado["facebook_total_interactions"] = suma_val
                elif nombre_m == "page_video_views":
                    resultado["facebook_views"] = suma_val
                elif nombre_m == "page_daily_follows_unique":
                    resultado["facebook_new_followers"] = suma_val

            # Demografía y Ciudades de Facebook (lifetime)
            resp_fb_demo = requests.get(
                f"{base_url}/{page_id}/insights",
                params={
                    "access_token": page_token,
                    "metric": "page_fans_gender_age,page_fans_city",
                    "period": "lifetime",
                },
                timeout=15,
            ).json()
            for item in resp_fb_demo.get("data", []):
                valores = item.get("values", [])
                ultimo_dict = valores[-1].get("value", {}) if valores else {}
                if item.get("name") == "page_fans_gender_age":
                    resultado.update(_parsear_demografia_meta(ultimo_dict, "facebook"))
                elif item.get("name") == "page_fans_city":
                    resultado.update(_parsear_top_ciudades(ultimo_dict, "facebook"))

        if ig_account_id:
            info_ig = requests.get(
                f"{base_url}/{ig_account_id}",
                params={
                    "access_token": token,
                    "fields": "username,followers_count,media_count,media.limit(15){caption,media_type,media_url,thumbnail_url,like_count,comments_count}",
                },
                timeout=15,
            ).json()
            if "error" not in info_ig:
                resultado["instagram_followers_total"] = info_ig.get("followers_count", 0)
                media_list = info_ig.get("media", {}).get("data", [])
                resultado["instagram_content_published"] = len(media_list)
                media_ordenada = sorted(
                    media_list,
                    key=lambda m: (m.get("like_count", 0) or 0) + (m.get("comments_count", 0) or 0),
                    reverse=True,
                )
                for idx, m in enumerate(media_ordenada[:3], start=1):
                    reacciones = (m.get("like_count", 0) or 0) + (m.get("comments_count", 0) or 0)
                    tipo_raw = m.get("media_type", "IMAGE")
                    formato = (
                        "Reel"
                        if tipo_raw == "VIDEO"
                        else ("Carrusel" if tipo_raw == "CAROUSEL_ALBUM" else "Imagen")
                    )
                    resultado[f"instagram_top3_{idx}_formato"] = formato
                    resultado[f"instagram_top3_{idx}_texto"] = (m.get("caption") or f"Post IG #{idx}")[:90]
                    url_img = m.get("thumbnail_url") or m.get("media_url")
                    if url_img:
                        resultado[f"instagram_top3_{idx}_url_imagen"] = url_img
                    resultado[f"instagram_top3_{idx}_reacciones"] = reacciones

            # Insights de cuenta de Instagram (alcance, impresiones, interacciones, nuevos seguidores)
            resp_ig_ins = requests.get(
                f"{base_url}/{ig_account_id}/insights",
                params={
                    "access_token": token,
                    "metric": "impressions,reach,follower_count",
                    "period": "day",
                    **params_fecha,
                },
                timeout=15,
            ).json()
            for item in resp_ig_ins.get("data", []):
                nombre_m = item.get("name")
                suma_val = sum(
                    int(float(v.get("value", 0) or 0))
                    for v in item.get("values", [])
                    if isinstance(v.get("value"), (int, float, str))
                )
                if nombre_m == "impressions":
                    resultado["instagram_impressions"] = suma_val
                elif nombre_m == "reach":
                    resultado["instagram_reach"] = suma_val
                elif nombre_m == "follower_count":
                    resultado["instagram_new_followers"] = suma_val
    except requests.exceptions.RequestException:
        pass

    return resultado


def listar_clientes_meta_business(token=None):
    """
    Consulta automáticamente todas las Cuentas Publicitarias (/me/adaccounts) y
    Páginas de Facebook + Cuentas de Instagram (/me/accounts) asociadas al token
    del Business Suite, para que todos los clientes aparezcan automáticamente.
    """
    token = token or Config.META_ACCESS_TOKEN
    if not token:
        return {}

    base_url = f"https://graph.facebook.com/{Config.META_API_VERSION}"
    clientes_detectados = {}

    try:
        resp_ads = requests.get(
            f"{base_url}/me/adaccounts",
            params={
                "access_token": token,
                "fields": "name,account_id,id,account_status,promote_pages{id,name,instagram_business_account{id,username}}",
                "limit": 100,
            },
            timeout=15,
        ).json()
        cuentas_ads = resp_ads.get("data", [])

        resp_pages = requests.get(
            f"{base_url}/me/accounts",
            params={
                "access_token": token,
                "fields": "id,name,instagram_business_account{id,username}",
                "limit": 100,
            },
            timeout=15,
        ).json()
        paginas = resp_pages.get("data", [])

        # Mapear páginas por nombre aproximado para vincularlas con su cuenta publicitaria
        mapa_paginas = {p.get("name", "").lower(): p for p in paginas if p.get("name")}

        for ad in cuentas_ads:
            nombre = ad.get("name") or f"Cuenta {ad.get('account_id')}"
            ad_id = ad.get("id") or f"act_{ad.get('account_id')}"
            promoted = ad.get("promote_pages", {}).get("data", [])
            pagina_match = promoted[0] if promoted else mapa_paginas.get(nombre.lower(), {})
            ig_info = pagina_match.get("instagram_business_account", {})

            clientes_detectados[nombre] = {
                "company_name": nombre,
                "ad_account_id": ad_id,
                "facebook_page_id": pagina_match.get("id", ""),
                "instagram_account_id": ig_info.get("id", ""),
                "instagram_handle": f"@{ig_info.get('username')}" if ig_info.get("username") else "",
                "presentation_id": Config.DEFAULT_PRESENTATION_ID,
            }

        # Agregar también páginas que no tengan el mismo nombre exacto que la cuenta publicitaria
        for pag in paginas:
            nombre_pag = pag.get("name")
            if nombre_pag and nombre_pag not in clientes_detectados:
                ig_info = pag.get("instagram_business_account", {})
                ad_default = cuentas_ads[0].get("id") if cuentas_ads else "act_792323499648312"
                clientes_detectados[nombre_pag] = {
                    "company_name": nombre_pag,
                    "ad_account_id": ad_default,
                    "facebook_page_id": pag.get("id", ""),
                    "instagram_account_id": ig_info.get("id", ""),
                    "instagram_handle": f"@{ig_info.get('username')}" if ig_info.get("username") else "",
                    "presentation_id": Config.DEFAULT_PRESENTATION_ID,
                }
    except requests.exceptions.RequestException:
        pass

    return clientes_detectados


def extraer_datos_completos_cliente(
    nombre_cliente="Universal en Becas",
    account_id=None,
    fecha_inicio=None,
    fecha_fin=None,
    usar_demo=False,
    permitir_fallback=True,
):
    """
    Extrae todas las métricas necesarias para el reporte de un cliente en el rango de fechas.
    Si usar_demo=True o si la API falla y permitir_fallback=True, retorna datos demo completos
    con la estructura exacta del reporte de Monstruo Canela.
    """
    cfg_cliente = Config.obtener_cliente(nombre_cliente)
    account_id = account_id or cfg_cliente["ad_account_id"]
    base_demo = generar_datos_demo_completos(
        nombre_cliente=cfg_cliente["company_name"],
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )

    if usar_demo:
        return base_demo

    try:
        campanas = extraer_insights_ads(
            account_id=account_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )
        if not campanas:
            if permitir_fallback:
                base_demo["origen_datos"] = "demo_sin_campanas"
                base_demo["aviso_api"] = (
                    f"Meta no devolvió campañas activas para {account_id} en el periodo seleccionado. "
                    "Se cargaron datos de demostración."
                )
                return base_demo
            return None

        total_spend = sum(c["spend"] for c in campanas)
        total_impressions = sum(c["impressions"] for c in campanas)
        total_reach = sum(c["reach"] for c in campanas)
        total_clicks = sum(c["clicks"] for c in campanas)
        total_link_clicks = sum(c["inline_link_clicks"] for c in campanas)
        total_leads = sum(c["leads"] for c in campanas)
        total_interactions = sum(c["interactions"] for c in campanas)
        ctr_global = (
            round((total_clicks / total_impressions) * 100, 2)
            if total_impressions
            else float(campanas[0].get("ctr", 0))
        )
        costo_por_lead = round(total_spend / total_leads, 2) if total_leads else 0.0

        datos = dict(base_demo)
        datos.update(
            {
                "origen_datos": "meta_api",
                "company_name": cfg_cliente["company_name"],
                "campaign_name": campanas[0]["campaign_name"],
                "spend": total_spend,
                "clicks": total_clicks,
                "ctr": ctr_global,
                "impressions": total_impressions,
                "campanas": campanas,
                "facebook_campaign_name": campanas[0]["campaign_name"],
                "facebook_spend": total_spend,
                "facebook_clicks": total_clicks,
                "facebook_ctr": ctr_global,
                "facebook_impressions": total_impressions,
                "meta_leads": total_leads,
                "meta_cost_per_result": costo_por_lead,
                "meta_total_spend": total_spend,
                "meta_link_clicks": total_link_clicks,
                "meta_interactions": total_interactions,
                "meta_reach": total_reach,
                "meta_paid_impressions": total_impressions,
            }
        )

        organico = extraer_insights_organicos_pagina(
            page_id=cfg_cliente.get("facebook_page_id"),
            ig_account_id=cfg_cliente.get("instagram_account_id"),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )
        datos.update(organico)
        return datos

    except Exception as e:
        if permitir_fallback:
            base_demo["origen_datos"] = "demo_fallback_error"
            base_demo["aviso_api"] = (
                f"No fue posible conectar con Meta API ({e}). "
                "Usando datos simulados para continuar con el flujo."
            )
            return base_demo
        raise


def extraer_datos_meta(account_id=None, fecha_inicio=None, fecha_fin=None):
    """
    Función compatible con versiones previas para extraer lista de campañas de Meta Ads.
    Si falla o no hay token, retorna datos simulados (Mock Data).
    """
    print("Iniciando protocolo de conexión con Meta Marketing API...")
    token = Config.META_ACCESS_TOKEN
    account_id = account_id or Config.obtener_cliente("Universal en Becas")["ad_account_id"]

    if not token:
        print("Credenciales no detectadas. Usando datos simulados (Mock Data) para continuar el desarrollo.")
        return generar_datos_demo_completos()["campanas"]

    print("Token detectado. Conectando a los servidores de Meta...")
    try:
        campanas = extraer_insights_ads(
            account_id=account_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            token=token,
        )
        return campanas or []
    except Exception as e:
        print(f"Error al conectar con Meta ({e}). Usando datos simulados de respaldo.")
        return generar_datos_demo_completos()["campanas"]


if __name__ == "__main__":
    datos = extraer_datos_meta()
    print("\nDatos extraídos exitosamente:")
    print(datos)