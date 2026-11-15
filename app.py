import datetime
import streamlit as st
from src.config import Config
from src.extract import listar_clientes_meta_business
from src.main import ejecutar_pipeline_reporte

st.set_page_config(
    page_title="Fábrica de Datos Monstruo Canela",
    page_icon="👹",
    layout="wide",
)

st.title("👹 Fábrica de Datos • Generador de Reportes Automatizados")
st.markdown(
    "Extrae métricas de **Meta Ads, Facebook e Instagram**, calcula KPIs con **Pandas** "
    "y genera automáticamente la presentación en **Google Slides**."
)

# --- Barra lateral de configuración ---
with st.sidebar:
    st.header("⚙️ Configuración del Pipeline")
    if st.button("🔄 Sincronizar clientes de Business Suite", use_container_width=True):
        nuevos_clientes = listar_clientes_meta_business()
        if nuevos_clientes:
            Config.CLIENTES.update(nuevos_clientes)
            st.session_state["clientes_sincronizados"] = nuevos_clientes
            st.success(f"¡{len(nuevos_clientes)} cuentas detectadas en Meta Business Suite!")
        else:
            st.warning("No se pudieron listar cuentas. Verifica que META_ACCESS_TOKEN esté activo en .env.")

    if "clientes_sincronizados" in st.session_state:
        Config.CLIENTES.update(st.session_state["clientes_sincronizados"])

    modo_extraccion = st.radio(
        "Fuente de datos:",
        options=[
            "Meta API (con respaldo automático)",
            "Modo Demo (Datos simulados)",
            "Meta API (estricto)",
        ],
        index=0,
    )
    inyectar_imagenes = st.checkbox(
        "Inyectar imágenes en formas ({{..._url}})",
        value=True,
        help="Reemplaza las figuras que contengan marcadores de imagen con las fotos de los Top 3 posts.",
    )

# --- 1. Selección de Cliente y Parámetros ---
clientes_disponibles = list(Config.CLIENTES.keys())
col_cliente, col_inicio, col_fin = st.columns([2, 1, 1])

with col_cliente:
    cliente_seleccionado = st.selectbox("👤 Selecciona el Cliente:", clientes_disponibles)

cfg_actual = Config.obtener_cliente(cliente_seleccionado)

with col_inicio:
    fecha_inicio = st.date_input("📅 Fecha de Inicio", datetime.date(2026, 7, 1))

with col_fin:
    fecha_fin = st.date_input("📅 Fecha de Fin", datetime.date(2026, 7, 31))

with st.sidebar.expander("🔧 Parámetros Técnicos del Cliente", expanded=False):
    account_id_input = st.text_input(
        "ID Cuenta Meta Ads:",
        value=cfg_actual["ad_account_id"],
    )
    presentation_id_input = st.text_input(
        "ID Plantilla Google Slides:",
        value=cfg_actual["presentation_id"],
    )

if fecha_inicio > fecha_fin:
    st.error("⚠️ La fecha de inicio no puede ser posterior a la fecha de fin.")
    st.stop()

usar_demo = modo_extraccion == "Modo Demo (Datos simulados)"
permitir_fallback = modo_extraccion != "Meta API (estricto)"

col_btn_preview, col_btn_slides = st.columns(2)

with col_btn_preview:
    btn_previsualizar = st.button(
        "🔍 1. Extraer y Previsualizar KPIs",
        use_container_width=True,
    )

with col_btn_slides:
    btn_generar = st.button(
        "🚀 2. Generar Reporte en Google Slides",
        type="primary",
        use_container_width=True,
    )

if btn_previsualizar or btn_generar:
    generar_slides = bool(btn_generar)
    mensaje_spinner = (
        f"Clonando plantilla e inyectando reporte en Google Slides para {cliente_seleccionado}..."
        if generar_slides
        else f"Extrayendo y transformando datos de {cliente_seleccionado}..."
    )

    with st.spinner(mensaje_spinner):
        try:
            resultado = ejecutar_pipeline_reporte(
                cliente=cliente_seleccionado,
                fecha_inicio=fecha_inicio.strftime("%Y-%m-%d"),
                fecha_fin=fecha_fin.strftime("%Y-%m-%d"),
                usar_demo=usar_demo,
                permitir_fallback=permitir_fallback,
                presentation_id=presentation_id_input.strip(),
                account_id=account_id_input.strip(),
                generar_slides=generar_slides,
                inyectar_imagenes=inyectar_imagenes,
            )
            st.session_state["ultimo_resultado"] = resultado
        except Exception as err:
            st.error(f"❌ Error durante la ejecución del pipeline: {err}")
            st.stop()

# --- Mostrar resultados si existen en sesión ---
resultado = st.session_state.get("ultimo_resultado")
if resultado and resultado.get("exito"):
    datos = resultado["datos"]
    marcadores = resultado["marcadores"]
    df_campanas = resultado["tabla_campanas"]
    copia = resultado.get("copia_slides")

    if datos.get("aviso_api"):
        st.warning(f"ℹ️ {datos['aviso_api']}")

    if copia:
        url_slides = copia.get(
            "webViewLink",
            f"https://docs.google.com/presentation/d/{copia['id']}/edit",
        )
        st.success(f"✅ ¡Reporte **{resultado['nombre_reporte']}** generado con éxito en Google Drive!")
        st.link_button("📂 Abrir Presentación en Google Slides", url_slides)

    st.divider()
    st.subheader(f"📊 Resumen de Métricas • {datos.get('company_name')}")

    tab_ads, tab_fb, tab_ig, tab_marcadores = st.tabs(
        [
            "🎯 Meta Ads (Pauta)",
            "📘 Facebook Orgánico",
            "📸 Instagram Orgánico",
            "🧩 Marcadores Google Slides",
        ]
    )

    with tab_ads:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Importe Gastado", marcadores.get("{{m_importe_gastado_total}}", "$0"))
        c2.metric("Clientes Potenciales (Leads)", marcadores.get("{{m_leads}}", "0"))
        c3.metric("Costo por Resultado", marcadores.get("{{m_costo_resultado}}", "$0"))
        c4.metric("Impresiones Pagadas", marcadores.get("{{m_impresiones_pagadas}}", "0"))

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Alcance Pagado", marcadores.get("{{m_alcance}}", "0"))
        c6.metric("Clics en el Enlace", marcadores.get("{{m_clicks_enlace}}", "0"))
        c7.metric("Interacciones", marcadores.get("{{m_interacciones}}", "0"))
        c8.metric("CTR Global", marcadores.get("{{ctr}}", "0%"))

        st.markdown("#### Desglose por Campaña (Transformado con Pandas)")
        st.dataframe(df_campanas, use_container_width=True)

    with tab_fb:
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Seguidores Totales", marcadores.get("{{f_seguidores_total}}", "0"))
        f2.metric("Nuevos Seguidores", marcadores.get("{{f_nuevos_seguidores}}", "0"))
        f3.metric("Impresiones", marcadores.get("{{f_impresiones}}", "0"))
        f4.metric("Alcance", marcadores.get("{{f_alcance}}", "0"))

        f5, f6, f7, f8 = st.columns(4)
        f5.metric("Interacciones", marcadores.get("{{f_interacciones}}", "0"))
        f6.metric("Vistas", marcadores.get("{{f_vistas}}", "0"))
        f7.metric("Clics en Enlace", marcadores.get("{{f_clicks_enlace}}", "0"))
        f8.metric("Contenido Publicado", marcadores.get("{{f_contenido_publicado}}", "0"))

        col_ciudades_fb, col_top_fb = st.columns(2)
        with col_ciudades_fb:
            st.markdown("##### Top 5 Ciudades (Facebook)")
            st.table(
                [
                    {
                        "Ranking": f"0{i}",
                        "Ciudad": marcadores.get(f"{{{{f_ciudad_{i}}}}}"),
                        "Personas": marcadores.get(f"{{{{f_ciudad_{i}_valor}}}}"),
                    }
                    for i in range(1, 6)
                ]
            )
        with col_top_fb:
            st.markdown("##### Top 3 Mejores Posts (Facebook)")
            st.table(
                [
                    {
                        "Top": f"#{i}",
                        "Formato": marcadores.get(f"{{{{f_top{i}_formato}}}}"),
                        "Texto": marcadores.get(f"{{{{f_top{i}_texto}}}}"),
                        "Alcance": marcadores.get(f"{{{{f_top{i}_alcance}}}}"),
                        "Reacciones": marcadores.get(f"{{{{f_top{i}_reacciones}}}}"),
                    }
                    for i in range(1, 4)
                ]
            )

    with tab_ig:
        i1, i2, i3, i4 = st.columns(4)
        i1.metric("Seguidores Totales", marcadores.get("{{i_seguidores_total}}", "0"))
        i2.metric("Nuevos Seguidores", marcadores.get("{{i_nuevos_seguidores}}", "0"))
        i3.metric("Impresiones", marcadores.get("{{i_impresiones}}", "0"))
        i4.metric("Alcance", marcadores.get("{{i_alcance}}", "0"))

        i5, i6, i7 = st.columns(3)
        i5.metric("Interacciones", marcadores.get("{{i_interacciones}}", "0"))
        i6.metric("Vistas", marcadores.get("{{i_vistas}}", "0"))
        i7.metric("Contenido Publicado", marcadores.get("{{i_contenido_publicado}}", "0"))

        col_ciudades_ig, col_top_ig = st.columns(2)
        with col_ciudades_ig:
            st.markdown("##### Top 5 Ciudades (Instagram)")
            st.table(
                [
                    {
                        "Ranking": f"0{i}",
                        "Ciudad": marcadores.get(f"{{{{i_ciudad_{i}}}}}"),
                        "Personas": marcadores.get(f"{{{{i_ciudad_{i}_valor}}}}"),
                    }
                    for i in range(1, 6)
                ]
            )
        with col_top_ig:
            st.markdown("##### Top 3 Mejores Posts (Instagram)")
            st.table(
                [
                    {
                        "Top": f"#{i}",
                        "Formato": marcadores.get(f"{{{{i_top{i}_formato}}}}"),
                        "Texto": marcadores.get(f"{{{{i_top{i}_texto}}}}"),
                        "Alcance": marcadores.get(f"{{{{i_top{i}_alcance}}}}"),
                        "Reacciones": marcadores.get(f"{{{{i_top{i}_reacciones}}}}"),
                    }
                    for i in range(1, 4)
                ]
            )

    with tab_marcadores:
        st.markdown("Listado completo de marcadores `{{...}}` listos para inyectarse en la plantilla:")
        st.dataframe(
            [{"Marcador": k, "Valor Formateado": v} for k, v in marcadores.items()],
            use_container_width=True,
            height=400,
        )