import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
st.set_page_config(page_title="Plataforma DIPOL", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #001226; }
    .stButton>button { width: 100%; border-radius: 4px; background-color: #D4AF37; color: #001226; font-weight: bold; }
    .stForm { border: 1px solid #D4AF37 !important; background-color: #002147 !important; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stRadio>label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def login():
    st.markdown("<h1 style='text-align: center;'>🛡️ SISTEMA DE CAPACITACIÓN DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER"):
            if usuario == "admin" and clave == "DIPOL2026":
                st.session_state['autenticado'] = True
                st.rerun()
            else: st.error("Acceso Denegado")

# 3. INTERFAZ OPERATIVA
if not st.session_state['autenticado']:
    login()
else:
    # CONEXIÓN (Mantenemos tu lógica funcional)
    db_s = st.secrets["connections"]["postgresql"]
    pass_segura = quote_plus(db_s['password'])
    engine = create_engine(f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}", pool_pre_ping=True)

    with st.sidebar:
        st.title("📂 MENÚ")
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Progreso"])
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    if seccion == "🏠 Inicio":
        st.title("Bienvenido al Panel Académico")
        st.write("Seleccione 'Módulos' en el menú lateral para comenzar su formación.")

    elif seccion == "📚 Módulos":
        st.title("📚 Módulos de Especialización")
        
        # Diccionario con el contenido de los 6 módulos
        modulos = {
            "Módulo 1: Conceptualizacion de Inteligencia": ["¿Qué protocolo asegura la confidencialidad?", ["AES", "HTTP", "FTP"], "AES"],
            "Módulo 2: Recoleccion": ["¿Qué puerto usa PostgreSQL por defecto?", ["80", "5432", "443"], "5432"],
            "Módulo 3: Tratamiento": ["¿Qué significa OSINT?", ["Open Source Intelligence", "Operating System Info", "Office Security"], "Open Source Intelligence"],
            "Módulo 4: Análisis": ["¿Cuál es el primer paso en un análisis?", ["Identificar Activos", "Comprar Servidores", "Formatear PC"], "Identificar Activos"],
            "Módulo 5: Difusion": ["¿Qué versión de TLS es la más segura actualmente?", ["TLS 1.0", "TLS 1.2", "TLS 1.3"], "TLS 1.3"],
            "Módulo 6: Retroalimentacion": ["¿Cuál es el objetivo del hacking ético?", ["Dañar sistemas", "Mejorar la seguridad", "Robar datos"], "Mejorar la seguridad"]
        }

        seleccion = st.selectbox("Seleccione un Módulo:", list(modulos.keys()))
        
        # Mostrar Contenido y Evaluación
        st.divider()
        st.subheader(f"📖 Contenido de {seleccion}")
        st.info(f"Usted está cursando el {seleccion}. Lea cuidadosamente y responda al final.")
        
        pregunta, opciones, correcta = modulos[seleccion]
        
        with st.form(key=f"form_{seleccion}"):
            st.write(f"**Pregunta de Evaluación:** {pregunta}")
            respuesta_usuario = st.radio("Elija su respuesta:", opciones)
            btn_evaluar = st.form_submit_button("FINALIZAR Y GUARDAR")

            if btn_evaluar:
                nota = 100 if respuesta_usuario == correcta else 0
                try:
                    with engine.connect() as conn:
                        query = text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)")
                        conn.execute(query, {"f": "Agente_DIPOL", "n": nota, "m": seleccion})
                        conn.commit()
                    
                    if nota == 100:
                        st.success(f"¡Excelente! Aprobado con {nota}%")
                        st.balloons()
                    else:
                        st.error(f"Nota: {nota}%. Le recomendamos repasar el contenido.")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")

    elif seccion == "📊 Progreso":
        st.title("📊 Historial de Capacitación")
        df = pd.read_sql(text("SELECT fecha, modulo, nota FROM calificaciones ORDER BY fecha DESC"), engine)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.line_chart(df, x="fecha", y="nota")
        else:
            st.info("No hay registros disponibles.")
