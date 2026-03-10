import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 🛡️ CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="DIPOL - HUB DE INTELIGENCIA", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .doctrina-card { background-color: #161b22; padding: 25px; border-left: 5px solid #004a99; border-radius: 12px; margin-bottom: 25px; }
    .sub-titulo { color: #00d4ff; font-weight: bold; text-transform: uppercase; font-size: 1.2rem; }
    .stButton>button { background: linear-gradient(135deg, #004a99 0%, #002d55 100%); color: white; border-radius: 8px; font-weight: bold; padding: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 LOGIN
if "identificado" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Intelligence Access")
        with st.form("login"):
            usuario = st.text_input("Funcionario (Nombre / Placa)")
            clave = st.text_input("Access Key", type="password")
            if st.form_submit_button("INGRESAR"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["funcionario"] = usuario
                    st.rerun()
                else: st.error("ACCESO DENEGADO")
    st.stop()

# 📊 CONEXIÓN
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error de conexión: {e}")

# 🚀 INTERFAZ
st.markdown(f"### ⚡ Terminal Activa: {st.session_state['funcionario']}")
tab_niveles, tab_admin = st.tabs(["📂 DOCTRINA Y NIVELES", "📊 PANEL INSTRUCTOR"])

with tab_niveles:
    st.header("📖 Marco Doctrinal")
    st.markdown('<div class="doctrina-card"><p class="sub-titulo">I. Definición de Inteligencia</p>Conocimiento obtenido mediante el procesamiento de información para la toma de decisiones.</div>', unsafe_allow_html=True)
    
    if st.checkbox("✅ He analizado la doctrina"):
        st.subheader("⚡ EVALUACIÓN")
        e1 = st.selectbox("1. Plan nacional (5 años):", ["...", "Estratégica", "Operacional", "Táctica"], key="q1")
        e2 = st.selectbox("2. Allanamientos el próximo mes:", ["...", "Estratégica", "Operacional", "Táctica"], key="q2")
        e3 = st.selectbox("3. Persecución inmediata:", ["...", "Estratégica", "Operacional", "Táctica"], key="q3")

        if st.button("🚀 ENVIAR CALIFICACIÓN"):
            if "..." in [e1, e2, e3]:
                st.warning("⚠️ Responda todas las preguntas.")
            else:
                puntos = 0
                if e1 == "Estratégica": puntos += 33
                if e2 == "Operacional": puntos += 33
                if e3 == "Táctica": puntos += 34
                
                nueva_nota = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Funcionario": st.session_state['funcionario'],
                    "Modulo": "Niveles",
                    "Nota": puntos
                }])
                
                try:
                    df_actual = conn.read()
                    df_final = pd.concat([df_actual, nueva_nota], ignore_index=True)
                    conn.update(data=df_final)
                    st.success(f"✅ ¡ÉXITO! Nota de {puntos}/100 guardada.")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error al guardar: {str(e)}")
                    st.info(f"Su nota: {puntos}/100. Tome captura.")

with tab_admin:
    st.header("📊 Registro")
    if st.text_input("Clave de Mando:", type="password") == "DIPOL_MASTER":
        try:
            df_total = conn.read(ttl=0)
            st.dataframe(df_total, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("🔒 DIPOL HUB | 2026")
