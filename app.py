import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 🛡️ CONFIGURACIÓN
st.set_page_config(page_title="DIPOL - SISTEMA DE NOTAS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .doctrina-card { background-color: #161b22; padding: 20px; border-left: 5px solid #004a99; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #004a99 0%, #002d55 100%); color: white; width: 100%; font-weight: bold; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 LOGIN
if "identificado" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Acceso DIPOL")
        with st.form("login"):
            usuario = st.text_input("Funcionario (Nombre / Placa)")
            clave = st.text_input("Clave", type="password")
            if st.form_submit_button("INGRESAR"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["funcionario"] = usuario
                    st.rerun()
                else: st.error("Clave incorrecta")
    st.stop()

# 📊 CONFIGURACIÓN DE LA HOJA
URL_HOJA = "https://docs.google.com/spreadsheets/d/1fw89-tdtBGU76hl6msHPlWlNdER12cYAfgIr0NpaT_M"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error de inicialización: {e}")

# 🚀 INTERFAZ
tab_eval, tab_admin = st.tabs(["📂 EVALUACIÓN", "📊 PANEL INSTRUCTOR"])

with tab_eval:
    st.markdown('<div class="doctrina-card">Analice los escenarios y seleccione el nivel de inteligencia adecuado.</div>', unsafe_allow_html=True)
    
    e1 = st.selectbox("1. Plan de 5 años para seguridad nacional:", ["...", "Estratégica", "Operacional", "Táctica"])
    e2 = st.selectbox("2. Allanamientos programados para el próximo mes:", ["...", "Estratégica", "Operacional", "Táctica"])
    e3 = st.selectbox("3. Persecución en curso (inmediata):", ["...", "Estratégica", "Operacional", "Táctica"])

    if st.button("🚀 ENVIAR CALIFICACIÓN"):
        if "..." in [e1, e2, e3]:
            st.warning("⚠️ Por favor, responda todas las preguntas.")
        else:
            puntos = 0
            if e1 == "Estratégica": puntos += 33
            if e2 == "Operacional": puntos += 33
            if e3 == "Táctica": puntos += 34
            
            nueva_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Funcionario": st.session_state['funcionario'],
                "Modulo": "Niveles de Inteligencia",
                "Nota": puntos
            }])
            
            try:
                # LEER: Especificamos la URL y el nombre de la pestaña exacto
                df_actual = conn.read(spreadsheet=URL_HOJA, worksheet="Hoja 1", ttl=0)
                
                # UNIR
                df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
                
                # ACTUALIZAR
                conn.update(spreadsheet=URL_HOJA, worksheet="Hoja 1", data=df_final)
                
                st.success(f"✅ ¡REGISTRO EXITOSO! Nota: {puntos}/100")
                st.balloons()
            except Exception as e:
                # Si falla, mostramos el error detallado para diagnosticar
                st.error(f"Error al guardar. Verifique que la hoja esté en modo 'Editor'.")
                st.code(f"Detalle técnico: {str(e)}")
                st.info(f"Su nota fue: {puntos}/100. Tome captura de pantalla.")

with tab_admin:
    st.header("📊 Registro de Calificaciones")
    if st.text_input("Clave Instructor", type="password") == "DIPOL_MASTER":
        try:
            # Forzamos lectura fresca
            df_resumen = conn.read(spreadsheet=URL_HOJA, worksheet="Hoja 1", ttl=0)
            st.dataframe(df_resumen, use_container_width=True)
        except:
            st.error("No se pudo cargar la base de datos.")

st.caption("🔒 DIPOL HUB | Bay Islands | 2026")
