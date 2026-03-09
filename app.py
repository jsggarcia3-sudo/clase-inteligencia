import streamlit as st

# ==========================================
# 🛡️ 1. CONFIGURACIÓN DE LA INTERFAZ
# ==========================================
st.set_page_config(page_title="Academia DIPOL", page_icon="👮‍♂️", layout="wide")

# ==========================================
# 🚩 2. CONTROL DE ACCESO (EL INTERRUPTOR)
# ==========================================
# Cambia a False para cerrar la clase al terminar tus 35 diapositivas
clase_activa = True 

if not clase_activa:
    st.error("🔒 ACCESO RESTRINGIDO: La sesión de Inteligencia ha finalizado.")
    st.info("El material ha sido archivado por seguridad institucional. Consulte con su instructor.")
    st.stop() 

# URL del logo oficial (Ruta directa)
logo_url = "https://www.policianacional.gob.hn/images/logo_policia_nacional.png"

# Estilo visual institucional
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #002d55; color: white; font-weight: bold; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002d55; color: white ! drawing; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image(logo_url, width=90)
with col_titulo:
    st.title("Dirección de Inteligencia Policial (DIPOL)")
    st.subheader("Plataforma de Autoaprendizaje - Ciclo de Inteligencia")

st.write("---")

# ==========================================
# 📂 3. ESTRUCTURA DE PESTAÑAS (OVA)
# ==========================================
tab_inicio, tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "🏠 Inicio", 
    "🕵️‍♂️ 1. Niveles de Inteligencia", 
    "📡 2. Fase: Recolección", 
    "🧠 3. Fase: Análisis"
])

# --- PESTAÑA: INICIO ---
with tab_inicio:
    st.header("Bienvenido, Agente")
    st.write("Esta plataforma guiará su aprendizaje de forma interactiva. Lea la teoría y complete los desafíos.")
    nombre_agente = st.text_input("Ingrese su Nombre Completo y Placa:")
    if nombre_agente:
        st.success(f"Sesión iniciada: Agente {nombre_agente}. Proceda a la pestaña de 'Niveles'.")

# --- PESTAÑA: NIVELES DE INTELIGENCIA ---
with tab_niveles:
    st.header("Teoría: Conceptos y Niveles de Inteligencia")
    
    st.markdown("""
    **Inteligencia Policial:** Es el proceso de transformar datos en conocimiento útil para prevenir el delito. 
    Se divide según el nivel de decisión:
    
    1.  **Estratégica:** Apoya planes de largo plazo y políticas nacionales (Dirección General).
    2.  **Operacional:** Se enfoca en desarticular bandas en zonas o regiones específicas (DIPOL Regional).
    3.  **Táctica:** Información inmediata para una captura o allanamiento hoy mismo (Equipos de Campo).
    """)

    st.divider()

    # --- SISTEMA DE DESBLOQUEO ---
    confirmar_lectura_1 = st.checkbox("✅ He analizado la diferencia entre los niveles Estratégico, Operacional y Táctico.")

    if confirmar_lectura_1:
        st.success("🔓 EJERCICIO DE VALIDACIÓN DESBLOQUEADO")
        st.subheader("⚡ Desafío de Clasificación")
        
        pregunta_1 = st.radio(
            "Escenario: Se está planificando la captura de un cabecilla para ejecutarse mañana a las 05:00 AM.",
            ["Seleccione una opción...", "Inteligencia Estratégica", "Inteligencia Operacional", "Inteligencia Táctica"]
        )
        
        if st.button("Validar Respuesta - Niveles"):
            if pregunta_1 == "Inteligencia Táctica":
                st.balloons()
                st.success("¡Correcto! Es Táctica porque es información para ejecución inmediata.")
            elif pregunta_1 == "Seleccione una opción...":
                st.warning("Por favor, seleccione una respuesta.")
            else:
                st.error("Incorrecto. Recuerde: La inmediatez (mañana temprano) define el nivel Táctico.")
    else:
        st.info("📖 Lea la teoría superior y marque la casilla para habilitar el ejercicio práctico.")

# --- PESTAÑA: RECOLECCIÓN ---
with tab_recoleccion:
    st.header("Teoría: Fase de Recolección")
    st.write("""
    La recolección obtiene la 'materia prima'. Se clasifica por fuentes:
    * **HUMINT:** Fuentes humanas (Informantes).
    * **TECHINT:** Medios técnicos (Cámaras, Interceptación).
    * **OSINT:** Fuentes abiertas (Redes sociales).
    """)
    st.warning("⚠️ Toda información debe evaluarse con la Tabla de **Fiabilidad (A-F)** y **Veracidad (1-6)**.")

    st.divider()

    confirmar_lectura_2 = st.checkbox("✅ Comprendo cómo se clasifica la información recolectada.")

    if confirmar_lectura_2:
        st.success("🔓 EJERCICIO DE RECOLECCIÓN DESBLOQUEADO")
        st.subheader("⚡ Caso Práctico")
        st.write("Escenario: Un ciudadano que nunca ha colaborado (Fuente Nueva) da un dato que usted confirma con el GPS de la patrulla.")
        
        fial = st.selectbox("¿Fiabilidad de la Fuente?", ["Seleccione...", "A (Confiable)", "F (Fuente Nueva)"])
        vera = st.selectbox("¿Veracidad del Dato?", ["Seleccione...", "1 (Confirmado)", "6 (No determinado)"])
        
        if st.button("Validar Respuesta - Recolección"):
            if fial.startswith("F") and vera.startswith("1"):
                st.success("¡Excelente! Es F-1: Fuente nueva pero dato confirmado por tecnología.")
            else:
                st.error("Incorrecto. Si es fuente nueva es 'F' y si está confirmado es '1'.")
    else:
        st.info("📖 Lea la teoría de recolección para habilitar el desafío.")

# --- PESTAÑA: ANÁLISIS ---
with tab_analisis:
    st.header("Teoría: Fase de Análisis")
    st.info("Concepto Clave: **Polarización Geográfica**. Es cuando el delito se concentra en zonas específicas (Hotspots).")
    
    st.divider()
    
    confirmar_lectura_3 = st.checkbox("✅ He leído sobre los patrones de análisis criminal.")

    if confirmar_lectura_3:
        st.success("🔓 EJERCICIO DE ANÁLISIS DESBLOQUEADO")
        analisis_resp = st.radio("Si los robos ocurren siempre en la misma calle, estamos ante:", 
                                ["Dispersión", "Polarización Geográfica"])
        if st.button("Validar Respuesta - Análisis"):
            if analisis_resp == "Polarización Geográfica":
                st.success("¡Correcto! Ha identificado una concentración criminal.")
    else:
        st.info("📖 Lea la teoría de análisis para habilitar el desafío final.")

st.write("---")
st.caption("DIPOL - Dirección de Inteligencia Policial | Honduras 2026")
