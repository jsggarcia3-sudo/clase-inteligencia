import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus

# 1. CONFIGURACIÓN E INSTITUCIONALIDAD (CSS)
st.set_page_config(page_title="Sistema de Inteligencia - DIPOL", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004586;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056a4;
        border: 1px solid #ffffff;
    }
    .login-box {
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #262730;
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN (LOGIN)
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def login():
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>🛡️ CONTROL DE ACCESO DIPOL</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container():
            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            usuario = st.text_input("Usuario Institucional")
            clave = st.text_input("Contraseña de Acceso", type="password")
            
            if st.button("INGRESAR AL SISTEMA"):
                # Aquí puedes definir tu usuario y clave
                if usuario == "admin" and clave == "DIPOL2026": 
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Credenciales no autorizadas. Acceso denegado.")
            st.markdown("</div>", unsafe_allow_html=True)

# 3. CONTENIDO PRINCIPAL (Si está autenticado)
if not st.session_state['autenticado']:
    login()
else:
    # --- BARRA LATERAL ---
    with st.sidebar:
        st.image("https://www.policianacional.gob.hn/storage/app/public/logo-policia.png", width=100) # Opcional: Logo PN
        st.title("Operaciones")
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    # --- CONEXIÓN A BASE DE DATOS ---
    try:
        db_s = st.secrets["connections"]["postgresql"]
        pass_segura = quote_plus(db_s['password'])
        engine = create_engine(
            f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}",
            pool_pre_ping=True
        )

        # --- SECCIÓN DE REGISTRO ---
        st.title("📋 Registro de Evaluaciones Tácticas")
        
        with st.form("form_registro", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                nombre = st.text_input("Nombre del Funcionario")
            with col_b:
                nota = st.number_input("Calificación (0-100)", 0, 100)
            
            submit = st.form_submit_button("GUARDAR EN BASE DE DATOS")
            
            if submit and nombre:
                with engine.connect() as conn:
                    query = text("INSERT INTO calificaciones (funcionario, nota) VALUES (:n, :t)")
                    conn.execute(query, {"n": nombre, "t": nota})
                    conn.commit()
                st.success(f"Registro exitoso: {nombre}")
                st.balloons()

        # --- DASHBOARD DE INTELIGENCIA ---
        st.divider()
        st.header("📊 Dashboard de Rendimiento")
        
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT fecha, funcionario, nota FROM calificaciones ORDER BY fecha DESC"), conn)

        if not df.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total de Agentes", len(df))
            m2.metric("Promedio Grupal", f"{df['nota'].mean():.1f}%")
            m3.metric("Última Nota", f"{df['nota'].iloc[0]}%")

            st.subheader("Tendencia de Resultados")
            st.line_chart(df, x="fecha", y="nota")
            
            st.subheader("Historial Completo")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Esperando primeros registros para generar análisis...")

    except Exception as e:
        st.error("Error de conexión con el servidor local.")
        st.exception(e)
