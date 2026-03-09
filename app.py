import streamlit as st

# ==========================================
# 🛡️ 1. CONFIGURACIÓN DE LA INTERFAZ
# ==========================================
st.set_page_config(page_title="Acceso - Academia DIPOL", page_icon="🔒", layout="centered")

# URL del logo oficial
logo_url = "https://www.policianacional.gob.hn/images/logo_policia_nacional.png"

# ==========================================
# 🔑 2. SISTEMA DE LOGIN
# ==========================================
def login():
    st.image(logo_url, width=120)
    st.title("Sistema de Inteligencia - DIPOL")
    st.subheader("Acceso Restringido")
    
    with st.form("login_form"):
        usuario = st.text_input("Nombre Completo / Placa")
        clave = st.text_input("Contraseña Institucional", type="password")
        boton_entrar = st.form_submit_button("INGRESAR AL SISTEMA")
        
        # AQUÍ DEFINES TU CONTRASEÑA (Cámbiala por la que gustes)
        if boton_entrar:
            if clave == "DIPOL2026": # <--- Esta es la clave para tus alumnos
                st.session_state["identificado"] = True
                st.session_state["agente"] = usuario
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas. Verifique con el instructor.")

# Verificamos si el agente ya se identificó
if "identificado" not in st.session_state:
    login()
    st.stop() # Detiene el código aquí si no se ha logueado

# ==========================================
# 🚀 3. CONTENIDO PRINCIPAL (Solo se ve tras el Login)
# ==========================================
# Cambiamos el layout a ancho una vez que entran
st.set_page_config(layout="wide") 

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image(logo_url, width=90)
with col_titulo:
    st.title(f"Bienvenido, Agente: {st.session_state['agente']}")
    st.subheader("Plataforma de Autoaprendizaje - Ciclo de Inteligencia")

st.write("---")

# --- PESTAÑAS (OVA) ---
tab_niveles, tab_recoleccion, tab_analisis = st.tabs([
    "🕵️‍♂️ 1. Niveles de Inteligencia", 
    "📡 2. Fase: Recolección", 
    "🧠 3. Fase: Análisis"
])

# --- PESTAÑA: NIVELES ---
with tab_niveles:
    st.header("Teoría: Conceptos y Niveles")
    st.markdown("""
    * **Estratégica:** Decisiones de alto mando.
    * **Operacional:** Desarticulación de bandas en regiones.
    * **Táctica:** Ejecución inmediata (Capturas).
    """)
    
    st.divider()
    
    # Bloqueo de lectura
    confirmar_1 = st.checkbox("✅ Confirmo que he leído la teoría de Niveles.")
    
    if confirmar_1:
        st.success("🔓 EJERCICIO DESBLOQUEADO")
        pregunta_1 = st.radio("Un plan nacional de 5 años es nivel:", ["Seleccione...", "Estratégico", "Operacional", "Táctico"])
        if st.button("Validar Respuesta"):
            if pregunta_1 == "Estratégico":
                st.balloons()
                st.success("¡Correcto!")
            else:
                st.error("Incorrecto.")
    else:
        st.info("📖 Lea la teoría superior para habilitar el ejercicio.")

# --- PESTAÑA: RECOLECCIÓN (Igual que la anterior...) ---
with tab_recoleccion:
    st.header("Fase de Recolección")
    st.write("Toda información se califica con Fiabilidad (A-F) y Veracidad (1-6).")
    
    st.divider()
    
    confirmar_2 = st.checkbox("✅ Comprendo la tabla de evaluación de fuentes.")
    if confirmar_2:
        st.success("🔓 EJERCICIO DESBLOQUEADO")
        # Aquí puedes poner el código del ejercicio de recolección
    else:
        st.info("📖 Lea la teoría de recolección para continuar.")

# Pie de página
st.write("---")
st.caption(f"Sesión activa: {st.session_state['agente']} | DIPOL 2026")
