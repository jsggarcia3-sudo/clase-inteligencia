import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
st.set_page_config(page_title="Plataforma Educativa DIPOL", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #001226; }
    .stButton>button { width: 100%; border-radius: 4px; background-color: #D4AF37; color: #001226; font-weight: bold; }
    .stForm { border: 1px solid #D4AF37 !important; background-color: #002147 !important; padding: 25px; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .lectura-box { background-color: #002b55; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; color: white; margin-bottom: 20px; }
    .highlight { color: #D4AF37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'agente_nombre' not in st.session_state:
    st.session_state['agente_nombre'] = ""
if 'es_admin' not in st.session_state:
    st.session_state['es_admin'] = False
if 'modo_examen' not in st.session_state:
    st.session_state['modo_examen'] = False

def login():
    st.markdown("<h1 style='text-align: center;'>🛡️ SISTEMA DE CAPACITACIÓN DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.write("### Identificación de Funcionario")
        nombre = st.text_input("Nombre Completo (Ej: Juan Pérez)")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        
        if st.button("ACCEDER"):
            # Lógica para Administrador
            if usuario == "admin_dipol" and clave == "DIPOL2026":
                st.session_state['autenticado'] = True
                st.session_state['es_admin'] = True
                st.session_state['agente_nombre'] = nombre if nombre else "Administrador"
                st.rerun()
            # Lógica para Estudiantes
            elif nombre and usuario and clave == "ESTUDIANTE2026":
                st.session_state['autenticado'] = True
                st.session_state['es_admin'] = False
                st.session_state['agente_nombre'] = nombre
                st.rerun()
            else:
                st.error("Credenciales incorrectas o falta nombre completo.")

# 3. INTERFAZ OPERATIVA
if not st.session_state['autenticado']:
    login()
else:
    db_s = st.secrets["connections"]["postgresql"]
    pass_segura = quote_plus(db_s['password'])
    engine = create_engine(f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}", pool_pre_ping=True)

    with st.sidebar:
        st.title("📂 MENÚ")
        tipo_user = "🛡️ ADMIN" if st.session_state['es_admin'] else "👤 ESTUDIANTE"
        st.write(f"**{tipo_user}:**\n{st.session_state['agente_nombre']}")
        st.divider()
        
        opciones = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso"]
        if st.session_state['es_admin']:
            opciones.append("📈 Dashboard General")
            
        seccion = st.radio("Ir a:", opciones)
        
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    # --- LÓGICA DE MÓDULOS (Se mantiene igual con definiciones completas) ---
    if seccion == "📚 Módulos":
        st.title("📚 Módulos de Especialización")
        seleccion = st.selectbox("Seleccione un Módulo:", ["Módulo 1: Conceptualización de Inteligencia"])
        
        if seleccion == "Módulo 1: Conceptualización de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material de Lectura Completo")
                st.markdown(f"""
                <div class="lectura-box">
                    <h3>Definición de Inteligencia</h3>
                    <p>1. Es el <b>conocimiento obtenido</b> a través del procesamiento adecuado de la información, que se brinda a los responsables de tomar decisiones.</p>
                    <p>2. Es una actividad <b>multi y transdisciplinaria</b>, compleja, dinámica y necesaria en un mundo en el cual el aprovechamiento de la oportunidad del futuro, asegura el éxito.</p>
                    <p>3. Su función es la de <b>asesoramiento</b>, proporcionando el conocimiento integrado que reduzca las diversas incertidumbres, para la toma de decisión.</p>
                    <p>4. Es la capacidad de aprender o comprender. Suele ser sinónimo del intelecto (entendimiento), pero se diferencia de este por hacer hincapié en las <b>habilidades y aptitudes</b> para manejar situaciones concretas y por beneficiarse de la experiencia sensorial.</p>
                </div>
                <div class="lectura-box">
                    <h3>¿Qué es Inteligencia Policial?</h3>
                    <p>Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la <b>seguridad y convivencia ciudadana</b>, a fin de contribuir a la definición de políticas a cargo de las autoridades de la administración pública a nivel nacional, departamental y local, al diseño de estrategias institucionales y a orientar la ejecución de operaciones en cumplimiento de la misión policial.</p>
                </div>
                <div class="lectura-box">
                    <h3>Inteligencia según su nivel</h3>
                    <p><b>INTELIGENCIA ESTRATÉGICA:</b> Los líderes políticos y policiales emplean algunas áreas del conjunto de conocimientos de inteligencia para la formulación de planes y políticas orientada hacia los objetivos nacionales.</p>
                    <p><b>INTELIGENCIA OPERACIONAL:</b> Requerida para el planeamiento de operaciones dentro de un área específica. Asesora al jefe de la operación sobre el mejor empleo de las unidades y minimizar riesgos.</p>
                    <p><b>INTELIGENCIA TÁCTICA:</b> Requerida para la conducción de operaciones al nivel de equipos. Se enfoca en las capacidades del objetivo y sus posibilidades inmediatas (dinámicas).</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 INICIAR EVALUACIÓN"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.header("📝 Evaluación Final")
                with st.form(key="form_eval"):
                    p1 = st.radio("1. Función de la inteligencia:", ["Duda", "Asesoramiento para reducir incertidumbres", "Fuerza"])
                    p2 = st.radio("2. Nivel para planes nacionales:", ["Estratégica", "Operacional", "Táctica"])
                    p3 = st.radio("3. Nivel de capacidades inmediatas:", ["Operacional", "Estratégica", "Táctica"])
                    p4 = st.radio("4. Diferencia inteligencia/intelecto:", ["Ninguna", "Habilidades concretas y experiencia sensorial", "Velocidad"])
                    p5 = st.radio("5. Objetivo Inteligencia Policial:", ["Estadística", "Conocimiento para seguridad y convivencia ciudadana", "Mantenimiento"])
                    
                    if st.form_submit_button("GUARDAR NOTA"):
                        respuestas = [p1=="Asesoramiento para reducir incertidumbres", p2=="Estratégica", p3=="Táctica", p4=="Habilidades concretas y experiencia sensorial", p5=="Conocimiento para seguridad y convivencia ciudadana"]
                        nota = (sum(respuestas) / 5) * 100
                        try:
                            with engine.connect() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": seleccion})
                                conn.commit()
                            st.success(f"Nota guardada: {nota}%")
                            st.session_state['modo_examen'] = False
                        except Exception as e: st.error(f"Error: {e}")

    # --- VISTA PRIVADA: SOLO MIS NOTAS ---
    elif seccion == "📊 Mi Progreso":
        st.title("📊 Mi Historial Personal")
        query = text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC")
        df = pd.read_sql(query, engine, params={"n": st.session_state['agente_nombre']})
        if not df.empty:
            st.metric("Mi Promedio", f"{df['nota'].mean():.1f}%")
            st.dataframe(df, use_container_width=True)
        else: st.info("No tienes exámenes registrados.")

    # --- VISTA ADMIN: DASHBOARD TOTAL ---
    elif seccion == "📈 Dashboard General":
        st.title("📊 Panel de Supervisión (DIPOL)")
        df_all = pd.read_sql(text("SELECT * FROM calificaciones"), engine)
        if not df_all.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Exámenes", len(df_all))
            c2.metric("Promedio General", f"{df_all['nota'].mean():.1f}%")
            c3.metric("Agentes Evaluados", df_all['funcionario'].nunique())
            
            st.subheader("Rendimiento por Estudiante")
            df_chart = df_all.groupby('funcionario')['nota'].mean().reset_index()
            st.bar_chart(df_chart.set_index('funcionario'))
            
            st.subheader("Tabla Maestra de Calificaciones")
            st.dataframe(df_all, use_container_width=True)
