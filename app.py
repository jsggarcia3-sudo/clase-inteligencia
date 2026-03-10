import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL (DIPOL COLORS)
st.set_page_config(page_title="Sistema de Inteligencia - DIPOL", page_icon="🛡️", layout="wide")

# CSS personalizado: Azul Marino (#002147) y Dorado (#D4AF37)
st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background-color: #001226;
    }
    /* Estilo de los botones (Dorado Táctico) */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3em;
        background-color: #D4AF37;
        color: #001226;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFD700;
        color: #000000;
        border: 1px solid #ffffff;
    }
    /* Contenedores de login y formularios */
    .css-1r6slb0, .stForm {
        border: 1px solid #D4AF37 !important;
        background-color: #002147 !important;
        border-radius: 10px;
        padding: 20px;
    }
    /* Textos y Títulos */
    h1, h2, h3, p {
        color: #ffffff !important;
    }
    /* Input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #003366;
        color: white;
        border: 1px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def login():
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🛡️ DIRECCIÓN DE INTELIGENCIA POLICIAL</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Acceso Restringido - Operaciones Roatán</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.write("---")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        
        if st.button("ACCEDER AL PANEL"):
            # Credenciales de acceso
            if usuario == "admin" and clave == "DIPOL2026": 
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Verifique con el administrador de sistemas.")
        st.write("---")

# 3. INTERFAZ OPERATIVA (Solo si el login es exitoso)
if not st.session_state['autenticado']:
    login()
else:
    # Barra lateral institucional
    with st.sidebar:
        st.markdown("<h2 style='color: #D4AF37;'>DIPOL</h2>", unsafe_allow_html=True)
        st.write("**Agente en Servicio**")
        st.write("Sede: Bay Islands / Roatán")
        st.write("---")
        if st.button("SALIR DEL SISTEMA"):
            st.session_state['autenticado'] = False
            st.rerun()

    # --- LÓGICA DE BASE DE DATOS (MANTENIENDO LO QUE FUNCIONA) ---
    try:
        db_s = st.secrets["connections"]["postgresql"]
        pass_segura = quote_plus(db_s['password'])
        engine = create_engine(
            f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}",
            pool_pre_ping=True
        )

        st.title("📋 Registro de Evaluaciones de Personal")
        
        # Formulario de Registro
        with st.form("registro_agente", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                nombre_agente = st.text_input("Nombre Completo del Funcionario")
            with c2:
                calificacion = st.number_input("Nota Obtenida", 0, 100)
            
            enviar = st.form_submit_button("REGISTRAR EN BASE DE DATOS")
            
            if enviar and nombre_agente:
                with engine.connect() as conn:
                    query = text("INSERT INTO calificaciones (funcionario, nota) VALUES (:n, :t)")
                    conn.execute(query, {"n": nombre_agente, "t": calificacion})
                    conn.commit()
                st.success(f"Datos de {nombre_agente} sincronizados con éxito.")
                st.balloons()

        # --- DASHBOARD DE ANÁLISIS ---
        st.markdown("<h2 style='color: #D4AF37;'>📊 Análisis de Rendimiento Académico</h2>", unsafe_allow_html=True)
        
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT fecha, funcionario, nota FROM calificaciones ORDER BY fecha DESC"), conn)

        if not df.empty:
            # Métricas superiores
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Evaluados", len(df))
            with m2:
                st.metric("Promedio General", f"{df['nota'].mean():.1f}%")
            with m3:
                st.metric("Rendimiento Máximo", f"{df['nota'].max()}%")

            # Gráfica Táctica
            st.subheader("Tendencia de Resultados")
            st.line_chart(df, x="fecha", y="nota")
            
            # Tabla de registros
            st.subheader("Historial de Registros Recientes")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No se registran datos previos en la base de datos local.")

    except Exception as e:
        st.error("Error Crítico: No se pudo establecer contacto con el servidor de la base de datos.")
        st.info("Verifique que Localtonet esté activo en su estación de trabajo.")
        st.exception(e)
