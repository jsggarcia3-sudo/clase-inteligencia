import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 🛡️ 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO (CSS)
# ==========================================
st.set_page_config(page_title="DIPOL - Intelligence Hub", page_icon="🛡️", layout="wide")

# CSS para transformar la apariencia de Streamlit
st.markdown("""
    <style>
    /* Fondo general y fuentes */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Estilo de las Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1a1c23;
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 10px;
        background-color: #262730;
        color: #ffffff;
        font-weight: bold;
        transition: 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #004a99 !important;
        border: 1px solid #00d4ff;
    }

    /* Tarjetas de contenido (Cards) */
    .teoria-card {
        background-color: #161b22;
        padding: 20px;
        border-left: 5px solid #004a99;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* Botones Tácticos */
    .stButton>button {
        background: linear-gradient(135deg, #004a99 0%, #002d55 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0px 0px 15px #00d4ff;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🔑 2. LOGIN CON EFECTO JAVASCRIPT
# ==========================================
if "identificado" not in st.session_state:
    # Imagen de seguridad
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
                    st.error("ACCESS DENIED: Credenciales No Válidas")
    
    # JavaScript para un efecto de "escaneo" visual
    components.html("""
        <script>
        console.log("DIPOL System Online");
        alert("SISTEMA RESTRINGIDO: Solo personal autorizado.");
        </script>
    """, height=0)
    st.stop()

# ==========================================
# 🚀 3. INTERFAZ TÁCTICA (Post-Login)
# ==========================================

# Saludo dinámico con JavaScript (Opcional)
st.markdown(f"### ⚡ Terminal Activa: Agente {st.session_state['agente']}")

tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "📂 NIVELES", "📡 RECOLECCIÓN", "🧠 ANÁLISIS"
])

# --- PESTAÑA 1 ---
with tab_niveles:
    st.markdown('<div class="teoria-card">', unsafe_allow_html=True)
    st.header("📍 Niveles de Inteligencia")
    st.write("Determine el alcance jerárquico y temporal de la información.")
    st.markdown("""
    * **ESTRATÉGICO:** Visión país (Dirección General).
    * **OPERACIONAL:** Visión Regional (DIPOL).
    * **TÁCTICO:** Visión Inmediata (Equipos de Campo).
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    check_1 = st.checkbox("✔ He analizado la doctrina de niveles")
    if check_1:
        st.markdown("---")
        st.subheader("🛠️ Desafío Táctico")
        opc = st.radio("Un plan de 5 años para reducir homicidios es:", ["...", "Estratégico", "Operacional", "Táctico"])
        if st.button("EJECUTAR VALIDACIÓN"):
            if opc == "Estratégico":
                st.balloons()
                st.success("VALIDADO: Nivel Estratégico confirmado.")
            else:
                st.error("ERROR: El tiempo y alcance no coinciden.")
    else:
        st.info("Utilice el interruptor superior para desbloquear el módulo de evaluación.")

# --- PESTAÑA 2 (Repetir estilo para el resto...) ---
with tab_recoleccion:
    st.markdown('<div class="teoria-card">', unsafe_allow_html=True)
    st.header("📡 Fase de Recolección")
    st.write("Clasificación de fuentes (A-F) y veracidad (1-6).")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.checkbox("✔ Confirmar lectura de protocolos"):
        st.success("Modulo de Recolección Abierto.")
        # Aquí va tu código de ejercicios anterior...

# Pie de página con estilo
st.markdown("---")
st.caption("🔒 DIPOL SYSTEM v2.0 | Bay Islands District | 2026")
