import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 🛡️ CONFIGURACIÓN
st.set_page_config(page_title="DIPOL - SISTEMA DE NOTAS", layout="wide")

# 📊 URL DIRECTA (Sin /edit)
URL_FINAL = "https://docs.google.com/spreadsheets/d/1fw89-tdtBGU76hl6msHPlWlNdER12cYAfgIr0NpaT_M"

# 🔑 LOGIN
if "identificado" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Acceso DIPOL")
        with st.form("login"):
            usuario = st.text_input("Funcionario")
            clave = st.text_input("Clave", type="password")
            if st.form_submit_button("INGRESAR"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["funcionario"] = usuario
                    st.rerun()
                else: st.error("Clave incorrecta")
    st.stop()

# 📡 CONEXIÓN
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error de inicialización: {e}")

# 🚀 INTERFAZ
tab_eval, tab_admin = st.tabs(["📂 EVALUACIÓN", "📊 PANEL INSTRUCTOR"])

with tab_eval:
    e1 = st.selectbox("1. Plan de 5 años:", ["...", "Estratégica", "Operacional", "Táctica"])
    e2 = st.selectbox("2. Allanamientos:", ["...", "Estratégica", "Operacional", "Táctica"])
    e3 = st.selectbox("3. Persecución:", ["...", "Estratégica", "Operacional", "Táctica"])

    if st.button("🚀 ENVIAR CALIFICACIÓN"):
        if "..." in [e1, e2, e3]:
            st.warning("Responda todo.")
        else:
            puntos = 33 if e1 == "Estratégica" else 0
            puntos += 33 if e2 == "Operacional" else 0
            puntos += 34 if e3 == "Táctica" else 0
            
            nueva_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Funcionario": st.session_state['funcionario'],
                "Modulo": "Niveles",
                "Nota": puntos
            }])
            
            try:
                # Forzamos la URL directa aquí para evitar el 404
                df_actual = conn.read(spreadsheet=URL_FINAL, worksheet="Resultados", ttl=0)
                df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
                conn.update(spreadsheet=URL_FINAL, worksheet="Resultados", data=df_final)
                st.success(f"✅ REGISTRADO: {puntos}/100")
                st.balloons()
            except Exception as e:
                st.error(f"Error 404: La hoja no responde. Verifique que la pestaña se llame 'Resultados'.")
                st.code(str(e))

with tab_admin:
    if st.text_input("Clave Instructor", type="password") == "DIPOL_MASTER":
        try:
            st.dataframe(conn.read(spreadsheet=URL_FINAL, worksheet="Resultados", ttl=0))
        except: st.error("No se pudo leer la base de datos.")
