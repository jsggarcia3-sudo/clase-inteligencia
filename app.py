import streamlit as st

# ==========================================
# 🛡️ 1. CONFIGURACIÓN DE LA INTERFAZ
# ==========================================
st.set_page_config(page_title="Acceso - Academia DIPOL", page_icon="🔒", layout="centered")

# Imagen de seguridad digital (La que sí aparece)
img_seguridad = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=400"

# ==========================================
# 🔑 2. SISTEMA DE LOGIN (PUERTA DE ENLACE)
# ==========================================
if "identificado" not in st.session_state:
    st.image(img_seguridad, width=250)
    st.title("Sistema de Inteligencia - DIPOL")
    st.subheader("Acceso Restringido para Agentes")
    
    with st.form("login_form"):
        usuario = st.text_input("Nombre Completo y Número de Placa")
        clave = st.text_input("Contraseña de la Clase", type="password")
        boton_entrar = st.form_submit_button("INGRESAR AL SISTEMA")
        
        if boton_entrar:
            # Esta es la clave que les darás en tu presentación
            if clave == "DIPOL2026": 
                st.session_state["identificado"] = True
                st.session_state["agente"] = usuario
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas. Verifique con su instructor.")
    st.stop() # Bloqueo total hasta que se identifiquen

# ==========================================
# 🚀 3. CONTENIDO PARA EL AGENTE (Tras el Login)
# ==========================================
# Cambiamos a layout ancho para mejor lectura
st.set_page_config(layout="wide") 

st.title(f"Misión de Entrenamiento: {st.session_state['agente']}")
st.write("---")

# Estructura de Pestañas Autodidactas (Teoría + Ejercicio)
tab_inicio, tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "🏠 Instrucciones", 
    "🕵️‍♂️ 1. Niveles", 
    "📡 2. Recolección", 
    "🧠 3. Análisis"
])

# --- PESTAÑA: INSTRUCCIONES ---
with tab_inicio:
    st.header("Bienvenido a la Plataforma de Inteligencia")
    st.write("""
    Agente, esta herramienta es autodidacta. Para completar la misión con éxito:
    1. Lea detenidamente la teoría en cada pestaña.
    2. Marque la casilla de confirmación al final de la lectura.
    3. Resuelva el desafío práctico que aparecerá dinámicamente.
    """)
    st.info("💡 Su progreso será evaluado al finalizar cada sección.")

# --- PESTAÑA: NIVELES ---
with tab_niveles:
    st.header("Teoría: Niveles de Inteligencia")
    st.markdown("""
    * **Estratégica:** Apoya planes nacionales y decisiones de alto mando (Dirección General).
    * **Operacional:** Enfocada en desarticular grupos criminales en zonas específicas (Región).
    * **Táctica:** Información para ejecución inmediata en el terreno (Allanamientos/Capturas).
    """)
    st.divider()
    
    confirmar_1 = st.checkbox("✅ He analizado la teoría de Niveles (Estratégico, Operacional y Táctico).")
    
    if confirmar_1:
        st.success("🔓 DESAFÍO DESBLOQUEADO")
        st.subheader("⚡ Caso Práctico #1")
        preg_1 = st.radio("Se ordena realizar un allanamiento MAÑANA a las 06:00 AM basándose en un informe de campo. ¿Qué nivel de inteligencia es?", 
                         ["Seleccione...", "Estratégica", "Operacional", "Táctica"])
        
        if st.button("Validar Respuesta - Niveles"):
            if preg_1 == "Táctica":
                st.balloons()
                st.success("¡Correcto! Es Táctica por la inmediatez de la acción.")
            else:
                st.error("Incorrecto. Recuerde que la ejecución inmediata es nivel Táctico.")
    else:
        st.info("📖 Lea la teoría superior para habilitar el ejercicio práctico.")

# --- PESTAÑA: RECOLECCIÓN ---
with tab_recoleccion:
    st.header("Teoría: Fase de Recolección")
    st.write("""
    La recolección es obtener datos brutos. Toda fuente debe ser evaluada:
    * **Fiabilidad (A-F):** ¿Qué tan confiable es el informante? (F = Fuente Nueva).
    * **Veracidad (1-6):** ¿Qué tan cierto es el dato? (1 = Confirmado).
    """)
    st.divider()
    
    confirmar_2 = st.checkbox("✅ Comprendo la tabla de evaluación de fuentes y veracidad.")
    
    if confirmar_2:
        st.success("🔓 DESAFÍO DESBLOQUEADO")
        st.write("🕵️ **Escenario:** Fuente Nueva (F) reporta una ubicación, y usted la confirma con GPS (1).")
        resp_fial = st.selectbox("¿Cómo califica esta información?", ["Seleccione...", "A-1", "F-6", "F-1"])
        
        if st.button("Validar Respuesta - Recolección"):
            if resp_fial == "F-1":
                st.success("¡Excelente! Es F-1: Fuente nueva pero dato confirmado técnicamente.")
            else:
                st.error("Incorrecto. Revise el escenario: Fuente Nueva (F) + Confirmado (1).")
    else:
        st.info("📖 Lea la teoría de recolección para continuar.")

# --- PESTAÑA: ANÁLISIS ---
with tab_analisis:
    st.header("Teoría: Fase de Análisis")
    st.info("Concepto: **Polarización Geográfica**. Es cuando el crimen se concentra en un punto específico (Puntos Calientes o Hotspots).")
    st.divider()
    
    confirmar_3 = st.checkbox("✅ He leído sobre la concentración criminal y polarización.")
    
    if confirmar_3:
        st.success("🔓 DESAFÍO FINAL DESBLOQUEADO")
        resp_analisis = st.radio("Si los delitos se agrupan en un solo barrio de la isla, estamos ante:", 
                                ["Dispersión Criminal", "Polarización Geográfica"])
        if st.button("Finalizar Misión"):
            if resp_analisis == "Polarización Geográfica":
                st.balloons()
                st.success("¡Misión Cumplida! Ha identificado correctamente el patrón criminal.")
    else:
        st.info("📖 Lea el concepto de análisis para finalizar el simulador.")

# Pie de página institucional
st.write("---")
st.caption(f"Sesión Activa: Agente {st.session_state['agente']} | DIPOL Honduras 2026")
