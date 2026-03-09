import streamlit as st

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Academia DIPOL", page_icon="👮‍♂️", layout="wide")

# 2. INTERRUPTOR DE MISIÓN
clase_activa = True 

if not clase_activa:
    st.error("🔒 ACCESO RESTRINGIDO: La sesión de Inteligencia ha finalizado.")
    st.stop() 

# 3. ESTILO Y LOGOS
logo_oficial = "https://www.policianacional.gob.hn/images/logo_policia_nacional.png"

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #002d55; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
col1, col2 = st.columns([1, 5])
with col1: st.image(logo_oficial, width=100)
with col2: 
    st.title("Dirección de Inteligencia Policial (DIPOL)")
    st.subheader("Plataforma de Autoaprendizaje - Ciclo de Inteligencia")

st.write("---")

# 4. ESTRUCTURA AUTODIDACTA POR PESTAÑAS
tab_inicio, tab_intel, tab_recoleccion, tab_analisis = st.tabs([
    "🏠 Inicio", 
    "🕵️‍♂️ Conceptualizacion Inteligencia", 
    "📡 Fase: Recolección", 
    "🧠 Fase: Análisis"
])


with tab_intel:
    st.header("Teoría: Conceptos y Niveles de Inteligencia")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("¿Qué es Inteligencia?")
        st.write("""
        Es el producto resultante del procesamiento de información relativo a naciones extranjeras, 
        fuerzas hostiles o áreas de operaciones, con el fin de **reducir la incertidumbre** del mando.
        """)
    with col_b:
        st.subheader("Inteligencia Policial")
        st.write("""
        Es la aplicación de la inteligencia en el ámbito de seguridad pública para 
        prevenir, neutralizar y combatir el fenómeno criminal y las estructuras delictivas.
        """)

    st.markdown("---")
    st.subheader("🗺️ Niveles de Inteligencia")
    st.write("Dependiendo de **quién** tome la decisión y el **tiempo** de ejecución, se clasifica en:")
    
    # Usamos columnas para comparar los niveles
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**Estratégica**")
        st.caption("Largo Plazo / Alta Dirección")
        st.write("Apoya planes nacionales y políticas de seguridad del Estado.")
    with c2:
        st.warning("**Operacional**")
        st.caption("Mediano Plazo / Regional")
        st.write("Se enfoca en desarticular estructuras criminales en una zona específica.")
    with c3:
        st.error("**Táctica**")
        st.caption("Corto Plazo / Inmediata")
        st.write("Información directa para una captura o allanamiento en curso.")

    st.markdown("---")
    st.subheader("⚡ Ejercicio de Validación: Clasificación de Niveles")
    st.write("Escenario: Se está planificando un operativo de captura contra un cabecilla de banda criminal que se realizará **mañana a las 05:00 AM**.")
    
    nivel_resp = st.radio("¿A qué nivel de inteligencia pertenece este escenario?", 
                          ["Estratégica", "Operacional", "Táctica"])
    
    if st.button("Validar Nivel"):
        if nivel_resp == "Táctica":
            st.success("¡Correcto! Es Táctica porque es información inmediata para una ejecución directa en el terreno.")
            st.balloons()
        else:
            st.error("Incorrecto. Recuerde: si es para una acción inmediata, es Táctica.")

# ... (Continúa con las pestañas de Recolección y Análisis que ya teníamos)
