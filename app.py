import streamlit as st
import datetime

st.set_page_config(page_title="Fábrica de Datos Monstruo Canela", page_icon="👹")

st.title(" Generador de Reportes Automatizados")
st.markdown("Selecciona los parámetros para generar la presentación en Google Slides.")

# 1. Selección de Cliente
clientes_disponibles = ["Universal en Becas", "Distrito Financiero", "Cliente 3"]
cliente_seleccionado = st.selectbox("👤 Selecciona el Cliente:", clientes_disponibles)

# 2. Rango de Fechas
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input(" Fecha de Inicio", datetime.date(2026, 8, 1))
with col2:
    fecha_fin = st.date_input("Fecha de Fin", datetime.date(2026, 8, 31))

# 3. Botón de Acción (Disparador)
if st.button(" Generar Reporte"):
    st.info(f"Clonando plantilla y procesando datos para {cliente_seleccionado}...")
    # Aquí conectaremos tu pipeline ETL (main.py) en el futuro
    st.success("¡Reporte generado con éxito en Google Drive!")