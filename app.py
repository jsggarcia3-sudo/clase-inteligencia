import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------

st.set_page_config(
    page_title="Plataforma Educativa DIPOL",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #001226; }
.stButton>button {
width:100%;
border-radius:6px;
background-color:#D4AF37;
color:#001226;
font-weight:bold;
}
.stForm{
border:1px solid #D4AF37;
background-color:#002147;
padding:25px;
border-radius:10px;
}
h1,h2,h3,h4{color:#D4AF37 !important;}
.lectura-box{
background:#002b55;
padding:20px;
border-radius:10px;
border-left:5px solid #D4AF37;
color:white;
margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONEXIÓN BASE DE DATOS
# ---------------------------------------------------------

@st.cache_resource
def conectar_bd():

    db = st.secrets["connections"]["postgresql"]

    engine = create_engine(
        f"postgresql://{db['username']}:{quote_plus(db['password'])}@{db['host']}:{db['port']}/{db['database']}"
    )

    return engine

engine = conectar_bd()

# ---------------------------------------------------------
# SESIÓN
# ---------------------------------------------------------

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if "admin" not in st.session_state:
    st.session_state.admin = False

if "modulo" not in st.session_state:
    st.session_state.modulo = None

if "examen" not in st.session_state:
    st.session_state.examen = False

# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

def login():

    st.title("🛡️ SISTEMA DE CAPACITACIÓN DIPOL")

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        nombre = st.text_input("Nombre completo")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")

        if st.button("ACCEDER"):

            if usuario == "admin_dipol" and clave == "DIPOL2026":

                st.session_state.autenticado = True
                st.session_state.admin = True
                st.session_state.usuario = nombre or "Administrador"
                st.rerun()

            elif clave == "ESTUDIANTE2026" and nombre != "":

                st.session_state.autenticado = True
                st.session_state.usuario = nombre
                st.session_state.admin = False
                st.rerun()

            else:
                st.error("Credenciales incorrectas")

# ---------------------------------------------------------
# FUNCIONES
# ---------------------------------------------------------

def guardar_nota(nombre, modulo, nota):

    try:

        with engine.begin() as conn:

            conn.execute(text("""
            INSERT INTO calificaciones(funcionario,modulo,nota,fecha)
            VALUES(:f,:m,:n,NOW())
            """),
            {"f":nombre,"m":modulo,"n":nota})

    except Exception as e:
        st.error("Error guardando nota")


def obtener_historial(nombre):

    try:

        with engine.connect() as conn:

            df = pd.read_sql(text("""
            SELECT modulo,nota,fecha
            FROM calificaciones
            WHERE funcionario=:n
            ORDER BY fecha DESC
            """),conn,params={"n":nombre})

            return df

    except:
        return pd.DataFrame()

# ---------------------------------------------------------
# LOGIN SCREEN
# ---------------------------------------------------------

if not st.session_state.autenticado:
    login()
    st.stop()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title("📂 MENÚ")

    st.write(f"Usuario: **{st.session_state.usuario}**")

    seccion = st.radio("Ir a:",[
        "Inicio",
        "Módulos",
        "Mi progreso",
        "Dashboard"
    ])

    if st.button("Cerrar sesión"):

        for k in list(st.session_state.keys()):
            del st.session_state[k]

        st.rerun()

# ---------------------------------------------------------
# INICIO
# ---------------------------------------------------------

if seccion == "Inicio":

    st.title("Panel de Control")

    st.info("Bienvenido al sistema de capacitación en Inteligencia Policial.")

# ---------------------------------------------------------
# MODULOS
# ---------------------------------------------------------

elif seccion == "Módulos":

    modulos = [
        "Módulo 1",
        "Módulo 2",
        "Módulo 3",
        "Módulo 4",
        "Módulo 5",
        "Módulo 6",
        "Módulo 7"
    ]

    if st.session_state.modulo is None:

        st.title("Módulos de Capacitación")

        cols = st.columns(3)

        for i,m in enumerate(modulos):

            with cols[i%3]:

                st.markdown(f"""
                <div style="background:#002147;padding:20px;border-radius:10px;text-align:center">
                <h3>{m}</h3>
                </div>
                """,unsafe_allow_html=True)

                if st.button(f"Abrir {m}",key=m):

                    st.session_state.modulo = m
                    st.rerun()

    else:

        modulo = st.session_state.modulo

        if st.button("⬅️ Volver"):
            st.session_state.modulo = None
            st.rerun()

        st.header(modulo)

        if not st.session_state.examen:

            st.markdown("""
            <div class="lectura-box">
            Material educativo del módulo.
            </div>
            """,unsafe_allow_html=True)

            if st.button("Iniciar examen"):
                st.session_state.examen = True
                st.rerun()

        else:

            with st.form("examen"):

                p1 = st.radio("1. Pregunta ejemplo?",["A","B","C"])
                p2 = st.radio("2. Pregunta ejemplo?",["A","B","C"])

                if st.form_submit_button("Finalizar"):

                    correctas = 0

                    if p1=="A":
                        correctas+=1
                    if p2=="B":
                        correctas+=1

                    nota = (correctas/2)*100

                    guardar_nota(
                        st.session_state.usuario,
                        modulo,
                        nota
                    )

                    st.success(f"Nota obtenida: {nota}")

                    st.session_state.examen = False
                    st.rerun()

# ---------------------------------------------------------
# PROGRESO
# ---------------------------------------------------------

elif seccion == "Mi progreso":

    st.title("Historial académico")

    df = obtener_historial(st.session_state.usuario)

    if df.empty:
        st.info("Sin registros aún")
    else:
        st.dataframe(df,use_container_width=True)

# ---------------------------------------------------------
# DASHBOARD ADMIN
# ---------------------------------------------------------

elif seccion == "Dashboard":

    if not st.session_state.admin:
        st.warning("Solo administradores")
        st.stop()

    st.title("Panel administrativo")

    try:

        with engine.connect() as conn:

            df = pd.read_sql(text("""
            SELECT funcionario,modulo,nota,fecha
            FROM calificaciones
            """),conn)

        st.dataframe(df,use_container_width=True)

        if not df.empty:

            st.subheader("Promedio por módulo")

            chart = df.groupby("modulo")["nota"].mean()

            st.bar_chart(chart)

    except:
        st.error("Error cargando datos")
