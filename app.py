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
if 'modo_examen' not in st.session_state:
    st.session_state['modo_examen'] = False

def login():
    st.markdown("<h1 style='text-align: center;'>🛡️ SISTEMA DE CAPACITACIÓN DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.write("### Identificación de Funcionario")
        nombre_ingresado = st.text_input("Nombre Completo (Ej: Agente Juan Pérez)")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER"):
            if nombre_ingresado and usuario == "admin" and clave == "DIPOL2026":
                st.session_state['autenticado'] = True
                st.session_state['agente_nombre'] = nombre_ingresado
                st.rerun()
            else: st.error("Acceso Denegado. Asegúrese de ingresar su nombre y credenciales correctas.")

# 3. INTERFAZ OPERATIVA
if not st.session_state['autenticado']:
    login()
else:
    db_s = st.secrets["connections"]["postgresql"]
    pass_segura = quote_plus(db_s['password'])
    engine = create_engine(f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}", pool_pre_ping=True)

    with st.sidebar:
        st.title("📂 MENÚ")
        st.write(f"👤 **Agente:** {st.session_state['agente_nombre']}")
        st.divider()
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Progreso"])
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.session_state['modo_examen'] = False
            st.rerun()

    if seccion == "🏠 Inicio":
        st.title(f"Bienvenido, {st.session_state['agente_nombre']}")
        st.write("Seleccione 'Módulos' para comenzar su formación.")

    elif seccion == "📚 Módulos":
        st.title("📚 Módulos de Especialización")
        seleccion = st.selectbox("Seleccione un Módulo:", ["Módulo 1: Conceptualización de Inteligencia"])
        st.divider()

        if seleccion == "Módulo 1: Conceptualización de Inteligencia":
            
            # --- VISTA DE LECTURA ---
            if not st.session_state['modo_examen']:
                st.header("📖 Material de Lectura Completo")
                with st.container():
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

            # --- VISTA DE EXAMEN ---
            else:
                st.header("📝 Evaluación Final")
                if st.button("⬅️ Volver a Material de Lectura"):
                    st.session_state['modo_examen'] = False
                    st.rerun()

                with st.form(key="form_final"):
                    p1 = st.radio("1. ¿Cuál es la función principal de la inteligencia?", ["Generar duda", "Asesoramiento para reducir incertidumbres", "Ejecución de fuerza"])
                    p2 = st.radio("2. ¿Qué nivel de inteligencia emplean los líderes para planes nacionales?", ["Estratégica", "Operacional", "Táctica"])
                    p3 = st.radio("3. ¿Cuál nivel se enfoca en capacidades del objetivo y ambiente inmediato?", ["Operacional", "Estratégica", "Táctica"])
                    p4 = st.radio("4. Diferencia entre inteligencia e intelecto:", ["Ninguna", "Habilidades para manejar situaciones concretas y experiencia sensorial", "La velocidad"])
                    p5 = st.radio("5. Objetivo de la Inteligencia Policial:", ["Solo estadísticas", "Generar conocimiento para seguridad y convivencia ciudadana", "Mantenimiento de patrullas"])

                    if st.form_submit_button("FINALIZAR"):
                        aciertos = 0
                        if p1 == "Asesoramiento para reducir incertidumbres": aciertos += 1
                        if p2 == "Estratégica": aciertos += 1
                        if p3 == "Táctica": aciertos += 1
                        if p4 == "Habilidades para manejar situaciones concretas y experiencia sensorial": aciertos += 1
                        if p5 == "Generar conocimiento para seguridad y convivencia ciudadana": aciertos += 1
                        
                        nota = (aciertos / 5) * 100
                        try:
                            with engine.connect() as conn:
                                # GUARDAMOS CON EL NOMBRE DEL AGENTE DE LA SESIÓN
                                query = text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)")
                                conn.execute(query, {"f": st.session_state['agente_nombre'], "n": nota, "m": seleccion})
                                conn.commit()
                            st.success(f"Nota guardada para {st.session_state['agente_nombre']}: {nota}%")
                            st.session_state['modo_examen'] = False
                        except Exception as e: st.error(f"Error: {e}")

    elif seccion == "📊 Progreso":
        st.title("📊 Mi Progreso")
        df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC"), engine, params={"n": st.session_state['agente_nombre']})
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else: st.info("No hay registros.")
