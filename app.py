import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 🛡️ 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO (CSS)
# ==========================================
st.set_page_config(page_title="DIPOL - Intelligence Hub", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Fondo y Colores Base */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Tarjetas de Doctrina */
    .doctrina-card {
        background-color: #161b22;
        padding: 25px;
        border-left: 5px solid #004a99;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    .sub-titulo { color: #00d4ff; font-weight: bold; text-transform: uppercase; font-size: 1.2rem; margin-bottom: 12px; }
    .resaltado { color: #2ecc71; font-weight: bold; }

    /* Pestañas (Tabs) Estilo Moderno */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: #1a1c23; padding: 12px; border-radius: 15px; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 8px; background-color: #262730; color: #ffffff; }
    .stTabs [aria-selected="true"] { background-color: #004a99 !important; border: 1px solid #00d4ff; }

    /* Botones Tácticos */
    .stButton>button {
        background: linear-gradient(135deg, #004a99 0%, #002d55 100%);
        color: white; border: none; border-radius: 8px; padding: 12px;
        font-weight: bold; text-transform: uppercase; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0px 0px 20px #00d4ff; transform: scale(1.01); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🔑 2. SISTEMA DE LOGIN
# ==========================================
if "identificado" not in st.session_state:
    # Imagen de seguridad (La que confirmaste que funciona)
    img_seguridad = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=400"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image(img_seguridad, width=250)
        st.title("🔐 Intelligence Access")
        st.subheader("Dirección de Inteligencia Policial")
        
        with st.form("login_form"):
            usuario = st.text_input("Agente (Nombre Completo / Placa)")
            clave = st.text_input("Access Key (Contraseña)", type="password")
            entrar = st.form_submit_button("DECRYPT & ENTER")
            
            if entrar:
                if clave == "DIPOL2026":
                    st.session_state["identificado"] = True
                    st.session_state["agente"] = usuario
                    st.rerun()
                else:
                    st.error("❌ ACCESS DENIED: Credenciales No Válidas")
    st.stop()

# ==========================================
# 🚀 3. INTERFAZ OPERATIVA (Post-Login)
# ==========================================
st.markdown(f"### ⚡ Terminal Activa: Agente {st.session_state['agente']}")

tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "📂 DOCTRINA Y NIVELES", "📡 RECOLECCIÓN", "🧠 ANÁLISIS"
])

# --- PESTAÑA 1: NIVELES Y DOCTRINA ---
with tab_niveles:
    st.header("📖 Marco Doctrinal de Inteligencia")

    # Bloque I: Definición General
    st.markdown('<div class="doctrina-card">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">I. Definición de Inteligencia</p>', unsafe_allow_html=True)
    st.write("""
    Es el conocimiento obtenido a través del **procesamiento adecuado de la información**, que se brinda a los responsables de tomar decisiones.
    
    Es una actividad multi y transdisciplinaria, compleja, dinámica y necesaria en un mundo en el cual el aprovechamiento de la oportunidad del futuro, asegura el éxito. 
    Su función es la de asesoramiento, proporcionando el conocimiento integrado que reduzca las diversas incertidumbres.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Bloque II: Inteligencia Policial
    st.markdown('<div class="doctrina-card" style="border-left-color: #00d4ff;">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">II. Inteligencia Policial</p>', unsafe_allow_html=True)
    st.write("""
    Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la **seguridad y convivencia ciudadana**. 
    Contribuye a la definición de políticas públicas, diseño de estrategias institucionales y orientación de operaciones en cumplimiento de la misión policial.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Bloque III: Niveles de Inteligencia
    
    st.markdown('<div class="doctrina-card" style="border-left-color: #2ecc71;">', unsafe_allow_html=True)
    st.markdown('<p class="sub-titulo">III. Inteligencia según su Nivel</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<span class='resaltado'>ESTRATEGICA</span>", unsafe_allow_html=True)
        st.write("Empleada por líderes políticos y policiales para formulación de planes y políticas orientadas hacia objetivos nacionales.")
    with c2:
        st.markdown("<span class='resaltado'>OPERACIONAL</span>", unsafe_allow_html=True)
        st.write("Requerida para el planeamiento de operaciones en áreas específicas. Asesora al jefe de operación para minimizar riesgos.")
    with c3:
        st.markdown("<span class='resaltado'>TÁCTICA</span>", unsafe_allow_html=True)
        st.write("Conducción de operaciones a nivel de equipos. Se enfoca en capacidades inmediatas del objetivo y el ambiente.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- EVALUACIÓN MEJORADA ---
    st.divider()
    confirmar = st.checkbox("✅ Confirmo que he leído y comprendido el marco doctrinal de Inteligencia.")

    if confirmar:
        st.markdown("### ⚡ SIMULADOR DE EVALUACIÓN DOCTRINAL")
        st.info("Analice los escenarios y asigne el nivel de inteligencia correcto.")

        # Escenarios con Selectbox
        e1 = st.selectbox("1. Informe sobre la evolución de pandillas en la región para los próximos 10 años:", 
                          ["Seleccione...", "Estratégica", "Operacional", "Táctica"], key="niv_1")
        
        e2 = st.selectbox("2. Planificación de allanamientos en Coxen Hole para desarticular una banda el próximo mes:", 
                          ["Seleccione...", "Estratégica", "Operacional", "Táctica"], key="niv_2")
        
        e3 = st.selectbox("3. Ubicación exacta de un sospechoso armado detectado por cámaras en este momento:", 
                          ["Seleccione...", "Estratégica", "Operacional", "Táctica"], key="niv_3")

        if st.button("🚀 CALIFICAR MISIÓN"):
            puntos = 0
            if e1 == "Estratégica": puntos += 33
            if e2 == "Operacional": puntos += 33
            if e3 == "Táctica": puntos += 34
            
            if puntos == 100:
                st.balloons()
                st.success(f"¡EXCELENTE! Nota: {puntos}/100. Dominio doctrinal total.")
            elif puntos >= 60:
                st.warning(f"APROBADO. Nota: {puntos}/100. Revise las diferencias entre niveles.")
            else:
                st.error(f"REPROBADO. Nota: {puntos}/100. Debe repasar la teoría.")
    else:
        st.warning("⚠️ El examen táctico se desbloqueará al confirmar la lectura superior.")

# --- PESTAÑAS RESTANTES (Estructura base para que tú las llenes) ---
with tab_recoleccion:
    st.header("Fase de Recolección")
    st.info("Módulo en desarrollo para la siguiente fase de la clase.")

with tab_analisis:
    st.header("Fase de Análisis")
    st.info("Módulo en desarrollo para la fase final.")

st.markdown("---")
st.caption("🔒 DIPOL SYSTEM v2.0 | Bay Islands | Secretaría de Seguridad 2026")
