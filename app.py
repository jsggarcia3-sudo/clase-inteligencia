import streamlit as st

# 1. CONFIGURACIÓN INICIAL (Siempre al principio)
st.set_page_config(page_title="Academia DIPOL", page_icon="👮‍♂️", layout="wide")

# 2. INTERRUPTOR GLOBAL (Cerrar clase)
clase_activa = True
if not clase_activa:
    st.error("🔒 ACCESO RESTRINGIDO: La sesión ha finalizado.")
    st.stop()

# 3. LOGO Y ENCABEZADO
logo_url = "https://www.policianacional.gob.hn/images/logo_policia_nacional.png"
col1, col2 = st.columns([1, 5])
with col1: st.image(logo_url, width=90)
with col2: 
    st.title("Dirección de Inteligencia Policial")
    st.subheader("Plataforma de Capacitación Continua")

st.write("---")

# 4. PESTAÑAS
tab_inicio, tab_niveles, tab_recoleccion = st.tabs(["🏠 Inicio", "🕵️‍♂️ Niveles de Inteligencia", "📡 Recolección"])

with tab_inicio:
    st.header("Bienvenido, Agente")
    nombre = st.text_input("Ingrese su nombre y placa para habilitar el sistema:")
    if nombre:
        st.success(f"Autenticado: Agente {nombre}. Proceda a la pestaña de Niveles.")

with tab_niveles:
    st.header("Teoría: Definiciones y Niveles")
    
    # --- CONTENIDO TEÓRICO ---
    st.markdown("""
    ### 1. Inteligencia Policial
    Es el conocimiento procesado que permite anticipar delitos y desarticular estructuras criminales.
    
    ### 2. Niveles de Inteligencia
    * **Estratégico:** Decisiones de alto mando (Planes de Nación).
    * **Operacional:** Grupos de tarea en zonas específicas (Regiones).
    * **Táctico:** Ejecución inmediata (Capturas, Allanamientos).
    """)
    
    st.divider()
    
    # --- EL BOTÓN DE DESBLOQUEO ---
    # Usamos un checkbox para que el alumno jure que leyó
    leido = st.checkbox("✅ He leído y comprendido la diferencia entre los niveles Estratégico, Operacional y Táctico.")

    if leido:
        st.success("🔓 MATERIAL COMPLEMENTARIO DESBLOQUEADO")
        st.subheader("⚡ Desafío de Clasificación")
        
        escenario = "El Director General ordena crear un plan de 5 años para reducir el narcotráfico en todo el país."
        opcion = st.radio("¿Qué nivel de inteligencia se está aplicando?", 
                         ["Seleccione...", "Estratégico", "Operacional", "Táctico"])
        
        if st.button("Validar Respuesta"):
            if opcion == "Estratégico":
                st.balloons()
                st.success("¡Correcto! Por ser a largo plazo y de nivel nacional, es Estratégico.")
            else:
                st.error("Incorrecto. Repase la teoría: el largo plazo define el nivel Estratégico.")
    else:
        st.warning("⚠️ El ejercicio práctico aparecerá aquí una vez que marque la casilla de lectura superior.")

# ... (Aquí puedes repetir la misma lógica para la pestaña de Recolección)
