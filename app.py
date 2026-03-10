import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 🛡️ 1. CONFIGURACIÓN Y ESTILO TÁCTICO
# ==========================================
st.set_page_config(page_title="DIPOL - HUB DE INTELIGENCIA", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .doctrina-card {
        background-color: #161b22;
        padding: 25px;
        border-left: 5px solid #004a99;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    .sub-titulo { color: #00d4ff; font-weight: bold; text-transform: uppercase; font-size: 1.2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: #1a1c23; padding: 12px; border-radius: 15px; }
    .stTabs [aria-selected="true"] { background-color: #004a99 !important; border: 1px solid #00d4ff; }
    .stButton>button {
        background: linear-gradient(135deg, #004a99 0%, #002d55 100%);
        color: white; border: none; border-radius: 8px; font-weight: bold; padding: 12px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🔑 2. SISTEMA DE LOGIN
# ==========================================
if "identificado" not in st.session_state:
    img_seguridad = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=400"
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img_seguridad, width=250)
        st.title("🔐 Intelligence Access")
        with st.form("login"):
            usuario = st.text_input("Funcionario (Nombre Completo / Placa)")
            clave = st.text_input("Access Key", type="password")
            if st.form_submit_button("INGRESAR"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["funcionario"] = usuario
                    st.rerun()
                else:
                    st.error("ACCESO DENEGADO")
    st.stop()

# ==========================================
# 📊 3. CONEXIÓN A GOOGLE SHEETS
# ==========================================
try:
    # Usamos ttl=0 para que siempre lea datos frescos del instructor
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error crítico de conexión: {e}")

# ==========================================
# 🚀 4. INTERFAZ OPERATIVA
# ==========================================
st.markdown(f"### ⚡ Terminal Activa: {st.session_state['funcionario']}")

tab_niveles, tab_recoleccion, tab_admin = st.tabs([
    "📂 DOCTRINA Y NIVELES", "📡 RECOLECCIÓN", "📊 PANEL INSTRUCTOR"
])

# --- TAB 1: NIVELES ---
with tab_niveles:
    st.header("📖 Marco Doctrinal de Inteligencia")

    st.markdown('<div class="doctrina-card"><p class="sub-titulo">I. Definición de Inteligencia</p>Es el conocimiento obtenido a través del procesamiento adecuado de la información...</div>', unsafe_allow_html=True)
    st.markdown('<div class="doctrina-card" style="border-left-color: #00d4ff;"><p class="sub-titulo">II. Inteligencia Policial</p>Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información...</div>', unsafe_allow_html=True)
    
    st.divider()
    
    if st.checkbox("✅ He analizado la doctrina de Inteligencia"):
        st.subheader("⚡ SIMULADOR DE EVALUACIÓN")
        e1 = st.selectbox("1. Plan de 5 años para seguridad nacional:", ["...", "Estratégica", "Operacional", "Táctica"], key="q1")
        e2 = st.selectbox("2. Allanamientos programados para el próximo mes:", ["...", "Estratégica", "Operacional", "Táctica"], key="q2")
        e3 = st.selectbox("3. Persecución en curso (inmediata):", ["...", "Estratégica", "Operacional", "Táctica"], key="q3")

        if st.button("🚀 ENVIAR CALIFICACIÓN"):
            if "..." in [e1, e2, e3]:
                st.warning("⚠️ Por favor responda todas las preguntas.")
            else:
                puntos = 0
                if e1 == "Estratégica": puntos += 33
                if e2 == "Operacional": puntos += 33
                if e3 == "Táctica": puntos += 34
                
                nueva_nota = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Funcionario": st.session_state['funcionario'],
                    "Modulo": "Niveles de Inteligencia",
                    "Nota": puntos
                }])
                
                try:
                    # LEER DATOS ACTUALES
                    df_actual = conn.read()
                    # CONCATENAR
                    df_final = pd.concat([df_actual, nueva_nota], ignore_index=True)
                    # ACTUALIZAR NUBE
                    conn.update(data=df_final)
                    st.success(f"✅ ¡ÉXITO! Nota de {puntos}/100 guardada en la base de datos.")
                    if puntos == 100: st.balloons()
                except Exception as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
                    st.info(f"Su nota fue: {puntos}/100. Tome captura de pantalla como respaldo.")
    else:
        st.info("📖 Lea la doctrina superior para habilitar el examen.")

# --- TAB 2: RECOLECCIÓN (VACÍO POR AHORA) ---
with tab_recoleccion:
    st.info("Módulo de Recolección de Información - Próximamente.")

# --- TAB 3: PANEL INSTRUCTOR (CORREGIDO) ---
with tab_admin:
    st.header("📊 Registro de Calificaciones (Instructor)")
    clave_maestra = st.text_input("Ingrese Clave de Mando para ver resultados:", type="password")
    
    if clave_maestra == "DIPOL_MASTER":
        try:
            # Forzamos lectura sin caché para ver los 30 alumnos al instante
            df_total = conn.read(ttl=0)
            st.write("### Listado de Agentes Evaluados")
            st.dataframe(df_total, use_container_width=True)
            
            # Botón para descargar reporte
            csv = df_total.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Reporte CSV", csv, "reporte_dipol.csv", "text/csv")
        except Exception as e:
            st.error(f"No se pudo cargar la base de datos: {e}")
    elif clave_maestra != "":
        st.error("Clave incorrecta.")

st.markdown("---")
st.caption("🔒 DIPOL HUB v2.5 | Bay Islands | 2026")
