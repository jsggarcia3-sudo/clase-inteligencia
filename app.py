import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 🛡️ 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO
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
    .resaltado { color: #2ecc71; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: #1a1c23; padding: 12px; border-radius: 15px; }
    .stTabs [aria-selected="true"] { background-color: #004a99 !important; border: 1px solid #00d4ff; }
    .stButton>button {
        background: linear-gradient(135deg, #004a99 0%, #002d55 100%);
        color: white; border: none; border-radius: 8px; font-weight: bold; padding: 12px;
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
            usuario = st.text_input("Agente (Nombre Completo / Placa)")
            clave = st.text_input("Access Key", type="password")
            if st.form_submit_button("INGRESAR"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["agente"] = usuario
                    st.rerun()
                else:
                    st.error("ACCESO DENEGADO")
    st.stop()

# ==========================================
# 📊 3. CONEXIÓN A BASE DE DATOS (GOOGLE SHEETS)
# ==========================================
# Nota: Configura tu URL de Google Sheets en los 'Secrets' de Streamlit como:
# [connections.gsheets]
# spreadsheet = "https://docs.google.com/spreadsheets/d/TU_ID_AQUI"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.warning("⚠️ Modo local: Las notas no se guardarán permanentemente.")

# ==========================================
# 🚀 4. INTERFAZ OPERATIVA
# ==========================================
st.markdown(f"### ⚡ Terminal Activa: Agente {st.session_state['agente']}")

tab_niveles, tab_recoleccion, tab_admin = st.tabs([
    "📂 DOCTRINA Y NIVELES", "📡 RECOLECCIÓN", "📊 PANEL INSTRUCTOR"
])

with tab_niveles:
    st.header("📖 Marco Doctrinal de Inteligencia")

    # I. Definición de Inteligencia
    st.markdown('<div class="doctrina-card">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">I. Definición de Inteligencia</p>', unsafe_allow_html=True)
    st.write("""
    Es el conocimiento obtenido a través del procesamiento adecuado de la información, que se brinda a los responsables de tomar decisiones. 
    Es una actividad multi y transdisciplinaria, compleja, dinámica y necesaria. Su función es la de asesoramiento, proporcionando conocimiento integrado que reduzca incertidumbres.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # II. Inteligencia Policial
    st.markdown('<div class="doctrina-card" style="border-left-color: #00d4ff;">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">II. Inteligencia Policial</p>', unsafe_allow_html=True)
    st.write("""
    Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la seguridad y convivencia ciudadana. 
    Contribuye a definir políticas, diseñar estrategias institucionales y orientar operaciones.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # III. Inteligencia según su Nivel
    
    st.markdown('<div class="doctrina-card" style="border-left-color: #2ecc71;">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">III. Inteligencia según su Nivel</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**ESTRATÉGICA**")
        st.write("Liderazgo político/policial. Formulación de planes y políticas para objetivos nacionales y seguridad de la nación.")
    with c2:
        st.markdown("**OPERACIONAL**")
        st.write("Planeamiento en áreas específicas. Identificación y análisis para apoyar al jefe de operación y minimizar riesgos.")
    with c3:
        st.markdown("**TÁCTICA**")
        st.write("Conducción de operaciones a nivel de equipos. Se enfoca en capacidades inmediatas del objetivo y el ambiente dinámico.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- EVALUACIÓN ---
    if st.checkbox("✅ He analizado la doctrina de Inteligencia"):
        st.subheader("⚡ SIMULADOR DE EVALUACIÓN")
        e1 = st.selectbox("1. Plan de 5 años para reducir el narcotráfico nacional:", ["...", "Estratégica", "Operacional", "Táctica"], key="q1")
        e2 = st.selectbox("2. Allanamientos en Coxen Hole programados para el próximo mes:", ["...", "Estratégica", "Operacional", "Táctica"], key="q2")
        e3 = st.selectbox("3. Persecución en curso de un vehículo sospechoso en West Bay:", ["...", "Estratégica", "Operacional", "Táctica"], key="q3")

        if st.button("🚀 ENVIAR CALIFICACIÓN"):
            puntos = 0
            if e1 == "Estratégica": puntos += 33
            if e2 == "Operacional": puntos += 33
            if e3 == "Táctica": puntos += 34
            
            # Registro de Datos
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            nueva_nota = pd.DataFrame([{"Fecha": timestamp, "Agente": st.session_state['agente'], "Nota": puntos}])
            
            # Guardado en Google Sheets (Si está configurado)
            try:
                df_old = conn.read()
                df_final = pd.concat([df_old, nueva_nota], ignore_index=True)
                conn.update(data=df_final)
                st.success(f"Nota de {puntos}/100 registrada correctamente.")
            except:
                st.info(f"Nota obtenida: {puntos}/100 (No se pudo conectar a la base de datos).")
            
            if puntos == 100: st.balloons()
    else:
        st.info("📖 Lea la doctrina para habilitar el examen.")

# --- PANEL DE INSTRUCTOR ---
with tab_admin:
    st.header("📊 Registro de Estudiantes")
    clave_mando = st.text_input("Clave de Mando:", type="password")
    if clave_mando == "DIPOL_MASTER":
        try:
            df_total = conn.read()
            st.dataframe(df_total, use_container_width=True)
            csv = df_total.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Reporte Excel", csv, "notas.csv", "text/csv")
        except:
            st.error("No hay conexión con la base de datos de notas.")

st.caption("🔒 DIPOL HUB v2.0 | Bay Islands | 2026")
