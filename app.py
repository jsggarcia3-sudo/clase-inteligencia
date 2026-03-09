import streamlit as st

# Configuración estética y profesional
st.set_page_config(page_title="Misión de Inteligencia DIPOL", page_icon="👮‍♂️", layout="centered")

# Estilo personalizado (colores institucionales)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #002d55; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 Centro de Evaluación de Inteligencia")
st.write("---")

# Registro del estudiante
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre Completo:")
with col2:
    id_agente = st.text_input("Número de Placa / ID:")

if nombre and id_agente:
    st.success(f"Bienvenido, Agente {nombre}. Iniciando evaluación de Fundamentos.")

    # --- EJERCICIO 1: RECOLECCIÓN (HUMINT) ---
    st.header("Fase 1: Recolección de Información")
    st.info("📌 **Escenario:** Un informante nuevo reporta una reunión de pandillas en un taller mecánico. No tenemos antecedentes de esta persona.")
    
    opcion_1 = st.radio(
        "¿Cómo clasificaría esta fuente y su información?",
        ["Seleccione...", "A-1 (Confiable/Confirmado)", "F-6 (Nueva/No determinada)", "B-2 (Usualmente confiable/Probable)"]
    )

    # --- EJERCICIO 2: ANÁLISIS ---
    st.header("Fase 2: Análisis y Procesamiento")
    st.write("Observe el mapa de calor proyectado en la Diapositiva 20.")
    analisis = st.selectbox(
        "Si los delitos se concentran en un solo cuadrante, usted está ante un fenómeno de:",
        ["Seleccione...", "Dispersión Criminal", "Polarización Geográfica", "Incidencia Aleatoria"]
    )

    # --- BOTÓN DE RESULTADOS ---
    if st.button("Finalizar Misión y Ver Puntuación"):
        puntos = 0
        
        # Validación Ejercicio 1
        if "F-6" in opcion_1:
            puntos += 50
            st.write("✅ **Ejercicio 1:** Correcto. Al ser fuente nueva, es F-6.")
        else:
            st.write("❌ **Ejercicio 1:** Incorrecto. Revise la tabla de evaluación A-F.")

        # Validación Ejercicio 2
        if analisis == "Polarización Geográfica":
            puntos += 50
            st.write("✅ **Ejercicio 2:** Correcto. Es el término técnico preciso.")
        else:
            st.write("❌ **Ejercicio 2:** Incorrecto. Repase el concepto de polarización.")

        # Nota Final
        st.metric(label="Calificación Final", value=f"{puntos}/100")
        
        if puntos == 100:
            st.balloons()
            st.success("¡Excelente! Está listo para el servicio de Inteligencia.")
        elif puntos >= 50:
            st.warning("Aprobado, pero se recomienda repasar la clasificación de fuentes.")
        else:
            st.error("Debe repetir la lección de fundamentos.")

st.sidebar.image("https://www.policianacional.gob.hn/images/logo_policia_nacional.png", width=100) # Opcional: Logo institucional
st.sidebar.markdown("### Guía de Clase\n35 Diapositivas - Fundamentos de Inteligencia")
