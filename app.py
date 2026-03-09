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
tab_inicio, tab_recoleccion, tab_analisis = st.tabs(["🏠 Inicio", "📡 Fase: Recolección", "🧠 Fase: Análisis"])

with tab_inicio:
    st.header("Bienvenido, Agente")
    st.write("Esta plataforma está diseñada para que avance a su propio ritmo. Lea la teoría en cada pestaña y complete el ejercicio práctico para validar su conocimiento.")
    nombre = st.text_input("Ingrese su nombre para comenzar:")
    if nombre: st.success(f"Listo para iniciar, Agente {nombre}. Diríjase a la pestaña de 'Recolección'.")

with tab_recoleccion:
    st.header("Teoría: La Recolección de Información")
    st.write("""
    La recolección es obtener datos brutos. Se clasifican por su origen:
    * **HUMINT:** Fuentes humanas (entrevistas, informantes).
    * **OSINT:** Fuentes abiertas (redes, periódicos).
    * **TECHINT:** Medios técnicos (cámaras, interceptaciones).
    """)
    st.warning("📊 **REGLA DE ORO:** Toda información se califica con la tabla (A-F) para Fiabilidad y (1-6) para Veracidad.")
    
    st.markdown("---")
    st.subheader("⚡ Ejercicio de Validación")
    st.write("Escenario: Un ciudadano reporta una avioneta sospechosa. Usted confirma el dato con el radar de la base.")
    
    fial = st.selectbox("¿Fiabilidad del ciudadano (Fuente nueva)?", ["F", "A", "B"])
    vera = st.selectbox("¿Veracidad (Si el radar lo confirmó)?", ["6", "1", "2"])
    
    if st.button("Validar Recolección"):
        if fial == "F" and vera == "1":
            st.success("¡Excelente! Fuente nueva (F) pero dato confirmado (1). Clasificación F-1.")
            st.balloons()
        else: st.error("Incorrecto. Repase la teoría de evaluación de fuentes.")

with tab_analisis:
    st.header("Teoría: El Análisis Criminal")
    st.write("El análisis transforma la información en **Inteligencia**. Un concepto clave es detectar patrones.")
    st.info("Concepto: La **Polarización Geográfica** ocurre cuando el delito se concentra en puntos calientes (Hotspots).")
    
    st.markdown("---")
    st.subheader("⚡ Ejercicio de Validación")
    preg_analisis = st.radio("Si el 80% de los robos ocurren en 2 calles de Roatán, ¿cómo llamamos a este fenómeno?", 
                             ["Dispersión", "Polarización Geográfica", "Azar"])
    
    if st.button("Validar Análisis"):
        if preg_analisis == "Polarización Geográfica":
            st.success("¡Correcto! Ha identificado un patrón geográfico.")
        else: st.error("Incorrecto. Revise el concepto de concentración criminal.")
