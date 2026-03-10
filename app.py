import streamlit as st

# ==========================================
# 🛡️ 1. CONFIGURACIÓN DE LA INTERFAZ
# ==========================================
st.set_page_config(page_title="Acceso - Academia DIPOL", page_icon="🔒", layout="centered")

# Imagen de respaldo (Escudo de seguridad digital) - Esta NO va a fallar
img_seguridad = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=400"

# ==========================================
# 🔑 2. SISTEMA DE LOGIN (OCULTA TODO LO DEMÁS)
# ==========================================
if "identificado" not in st.session_state:
    st.image(img_seguridad, width=200)
    st.title("Sistema de Inteligencia - DIPOL")
    st.subheader("Acceso Restringido")
    
    with st.form("login_form"):
        usuario = st.text_input("Nombre Completo o Número de Placa")
        clave = st.text_input("Contraseña de la Clase", type="password")
        boton_entrar = st.form_submit_button("INGRESAR AL SISTEMA")
        
        if boton_entrar:
            # Aquí defines la clave para tus alumnos
            if clave == "DIPOL2026": 
                st.session_state["identificado"] = True
                st.session_state["agente"] = usuario
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
    st.stop() # Bloquea el resto del código hasta que se logueen

# ==========================================
# 🚀 3. CONTENIDO PRINCIPAL (Solo tras el Login)
# ==========================================
st.title(f"Bienvenido, Agente: {st.session_state['agente']}")
st.write("---")

# Estructura de Pestañas Autodidactas
tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "🕵️‍♂️ 1. Niveles", 
    "📡 2. Recolección", 
    "🧠 3. Análisis"
])

# --- PESTAÑA 1: NIVELES ---
with tab_niveles:
    st.header("Teoría: Niveles de Inteligencia")
    st.write("""
    * **Estratégico:** Largo plazo / Nacional.
    * **Operacional:** Mediano plazo / Regional.
    * **Táctico:** Inmediato / Ejecución de campo.
    """)
    
    st.divider()
    
    # Sistema de desbloqueo
    confirmar_1 = st.checkbox("✅ He leído la teoría de niveles.")
    
    if confirmar_1:
        st.success("🔓 EJERCICIO DESBLOQUEADO")
        pregunta_1 = st.radio("Un plan para capturar a un objetivo MAÑANA es:", 
                             ["Seleccione...", "Estratégico", "Operacional", "Táctico"])
        
        if st.button("Validar Niveles"):
            if pregunta_1 == "Táctico":
                st.balloons()
                st.success("¡Correcto! Es Táctico.")
            else:
                st.error("Incorrecto. Revise la definición de inmediatez.")
    else:
        st.info("📖 Marque la casilla para habilitar el ejercicio.")

# --- PESTAÑA 2: RECOLECCIÓN ---
with tab_recoleccion:
    st.header("Teoría: Fase de Recolección")
    st.write("Toda información se califica con Fiabilidad (A-F) y Veracidad (1-6).")
    
    st.divider()
    
    confirmar_2 = st.checkbox("✅ He comprendido la tabla de evaluación.")
    
    if confirmar_2:
        st.success("🔓 EJERCICIO DESBLOQUEADO")
        st.write("Escenario: Fuente nueva (F) y dato confirmado por GPS (1).")
        resp_fial = st.selectbox("Calificación:", ["Seleccione...", "F-1", "A-1", "F-6"])
        if st.button("Validar Recolección"):
            if resp_fial == "F-1":
                st.success("¡Excelente!")
    else:
        st.info("📖 Lea la teoría para habilitar el desafío.")

# Pie de página
st.caption(f"Sesión activa: {st.session_state['agente']} | DIPOL Honduras 2026")
