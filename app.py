import streamlit as st
import pandas as pd
from datetime import datetime

# 🛡️ CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="DIPOL - HUB DE NOTAS", page_icon="🛡️", layout="wide")

# 🔗 TU ENLACE DE PUBLICACIÓN CSV
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR-AxmzspxC9YcY0q3cCEQFmgJ8jJXRq9QcDLk8EQzCTcCCBQM96eL9GBoxJPITUtvNg8_Z2WgLDeKX/pub?output=csv"

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .doctrina-card { background-color: #161b22; padding: 20px; border-left: 5px solid #004a99; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #004a99 0%, #002d55 100%); color: white; width: 100%; font-weight: bold; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 SISTEMA DE ACCESO
if "identificado" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Acceso Sistema DIPOL")
        with st.form("login"):
            usuario = st.text_input("Funcionario (Nombre o Placa)")
            clave = st.text_input("Clave de Acceso", type="password")
            if st.form_submit_button("INGRESAR"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["funcionario"] = usuario
                    st.rerun()
                else: st.error("ACCESO DENEGADO")
    st.stop()

# 🚀 CUERPO DE LA APLICACIÓN
st.markdown(f"### ⚡ Terminal Activa: {st.session_state['funcionario']}")

tab_eval, tab_admin = st.tabs(["📂 EVALUACIÓN DOCTRINAL", "📊 PANEL DE INSTRUCTOR"])

with tab_eval:
    st.markdown('<div class="doctrina-card"><b>INSTRUCCIONES:</b> Seleccione el nivel de inteligencia que corresponde a cada escenario planteado.</div>', unsafe_allow_html=True)
    
    q1 = st.selectbox("1. Elaboración del Plan Estratégico de Seguridad para los próximos 5 años:", ["...", "Estratégica", "Operacional", "Táctica"])
    q2 = st.selectbox("2. Planificación de una serie de allanamientos contra estructuras criminales para el próximo mes:", ["...", "Estratégica", "Operacional", "Táctica"])
    q3 = st.selectbox("3. Ejecución inmediata de una persecución tras un hecho delictivo en curso:", ["...", "Estratégica", "Operacional", "Táctica"])

    if st.button("🚀 ENVIAR RESULTADOS"):
        if "..." in [q1, q2, q3]:
            st.warning("⚠️ Debe responder todas las interrogantes.")
        else:
            # Cálculo de nota
            nota = 0
            if q1 == "Estratégica": nota += 33
            if q2 == "Operacional": nota += 33
            if q3 == "Táctica": nota += 34
            
            st.success(f"✅ EVALUACIÓN COMPLETADA: {nota}/100")
            st.balloons()
            
            # Nota importante sobre la escritura
            st.info("""
            **AVISO DE SEGURIDAD:** Debido a las restricciones de escritura directa en la red, 
            por favor **tome una captura de pantalla** de este resultado y envíela al instructor 
            como respaldo oficial de su calificación.
            """)

with tab_admin:
    st.header("📊 Registro Centralizado de Notas")
    clave_mando = st.text_input("Ingrese Clave de Mando para visualizar:", type="password")
    
    if clave_mando == "DIPOL_MASTER":
        try:
            # Aquí usamos el link que me pasaste para LEER los datos
            df_clase = pd.read_csv(URL_CSV)
            st.write("Datos sincronizados con la nube de Google:")
            st.dataframe(df_clase, use_container_width=True)
        except Exception as e:
            st.error("Error al sincronizar con la base de datos.")
            st.info("Verifique que la hoja de Google tenga al menos una fila de datos y esté publicada correctamente.")

st.caption("🔒 DIPOL HUB | Dirección de Inteligencia Policial | 2026")
