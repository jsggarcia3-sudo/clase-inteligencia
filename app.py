import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 🛡️ 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO (CSS)
# ==========================================
st.set_page_config(page_title="DIPOL - HUB DE INTELIGENCIA", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Estilo de Tarjetas Doctrinales */
    .doctrina-card {
        background-color: #161b22;
        padding: 20px;
        border-left: 5px solid #004a99;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    
    .sub-titulo { color: #00d4ff; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; }

    /* Botones y Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #1a1c23; padding: 10px; border-radius: 15px; }
    .stTabs [aria-selected="true"] { background-color: #004a99 !important; border: 1px solid #00d4ff; }
    
    .stButton>button {
        background: linear-gradient(135deg, #004a99 0%, #002d55 100%);
        color: white; border: none; border-radius: 8px; font-weight: bold;
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
        st.image(img_seguridad, width=200)
        st.title("🔐 Intelligence Access")
        with st.form("login"):
            usuario = st.text_input("Agente (Nombre/ID)")
            clave = st.text_input("Access Key", type="password")
            if st.form_submit_button("DECRYPT & ENTER"):
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["agente"] = usuario
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
    st.stop()

# ==========================================
# 🚀 3. CONTENIDO DOCTRINARIO (NIVELES)
# ==========================================
st.markdown(f"### ⚡ Terminal Activa: Agente {st.session_state['agente']}")

tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "📂 DOCTRINA Y NIVELES", "📡 RECOLECCIÓN", "🧠 ANÁLISIS"
])

with tab_niveles:
    st.header("📖 Marco Doctrinal de Inteligencia")
    
    # --- BLOQUE 1: DEFINICIÓN DE INTELIGENCIA ---
    st.markdown('<div class="doctrina-card">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">I. Definición de Inteligencia</p>', unsafe_allow_html=True)
    st.write("""
    Es el conocimiento obtenido a través del procesamiento adecuado de la información, que se brinda a los responsables de tomar decisiones.
    
    Es una actividad **multi y transdisciplinaria**, compleja, dinámica y necesaria en un mundo en el cual el aprovechamiento de la oportunidad del futuro asegura el éxito.
    
    * **Función:** Asesoramiento, proporcionando conocimiento integrado que reduzca las diversas incertidumbres para la toma de decisión.
    * **Naturaleza:** Capacidad de aprender o comprender. Se diferencia del intelecto por hacer hincapié en las habilidades para manejar situaciones concretas y beneficiarse de la experiencia sensorial.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- BLOQUE 2: INTELIGENCIA POLICIAL ---
    st.markdown('<div class="doctrina-card" style="border-left-color: #00d4ff;">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">II. Inteligencia Policial</p>', unsafe_allow_html=True)
    st.write("""
    Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la **seguridad y convivencia ciudadana**.
    
    Su fin es contribuir a la definición de políticas (a nivel nacional, departamental y local), al diseño de estrategias institucionales y a orientar la ejecución de operaciones en cumplimiento de la misión policial.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- BLOQUE 3: NIVELES DE INTELIGENCIA ---
    
    st.markdown('<div class="doctrina-card" style="border-left-color: #2ecc71;">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">III. Inteligencia según su Nivel</p>', unsafe_allow_html=True)
    
    col_est, col_ope, col_tac = st.columns(3)
    with col_est:
        st.markdown("**ESTRATÉGICA**")
        st.caption("Liderazgo Político/Policial")
        st.write("Formulación de planes y políticas orientadas hacia objetivos nacionales, seguridad y bienestar de la nación.")
    with col_ope:
        st.markdown("**OPERACIONAL**")
        st.caption("Planeamiento Regional")
        st.write("Recolección y análisis para apoyar a jefes de operación en áreas específicas, minimizando riesgos.")
    with col_tac:
        st.markdown("**TÁCTICA**")
        st.caption("Equipos de Campo")
        st.write("Enfocada en capacidades del objetivo y ambiente inmediato. Es dinámica y varía constantemente.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- VALIDACIÓN ---
    st.divider()
    if st.checkbox("✔ He finalizado la lectura de la doctrina de niveles"):
        st.success("🔓 MÓDULO DE EVALUACIÓN DESBLOQUEADO")
        opc = st.radio("Un plan nacional de seguridad a 5 años es un ejemplo de inteligencia:", 
                       ["...", "Estratégica", "Operacional", "Táctica"])
        if st.button("VALIDAR CONOCIMIENTO"):
            if opc == "Estratégica":
                st.balloons()
                st.success("CORRECTO: El alcance nacional y político define el nivel Estratégico.")
            else:
                st.error("ERROR: Revise la definición de objetivos nacionales.")
    else:
        st.info("📖 Lea el material doctrinal para habilitar la evaluación.")

# (Las pestañas de Recolección y Análisis se mantienen con su estructura previa)
