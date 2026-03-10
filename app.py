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
    h1, h2, h3, h4 { color: #D4AF37 !important; }
    .lectura-box { background-color: #002b55; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'autenticado' not in st.session_state: st.session_state['autenticado'] = False
if 'agente_nombre' not in st.session_state: st.session_state['agente_nombre'] = ""
if 'es_admin' not in st.session_state: st.session_state['es_admin'] = False
if 'modo_examen' not in st.session_state: st.session_state['modo_examen'] = False

def login():
    st.markdown("<h1 style='text-align: center;'>🛡️ SISTEMA DE CAPACITACIÓN DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.write("### Identificación de Funcionario")
        nombre = st.text_input("Nombre Completo")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER"):
            if usuario == "admin_dipol" and clave == "DIPOL2026":
                st.session_state.update({'autenticado': True, 'es_admin': True, 'agente_nombre': nombre if nombre else "Admin"})
                st.rerun()
            elif nombre and usuario and clave == "ESTUDIANTE2026":
                st.session_state.update({'autenticado': True, 'es_admin': False, 'agente_nombre': nombre})
                st.rerun()
            else: st.error("Credenciales incorrectas.")

if not st.session_state['autenticado']:
    login()
else:
    db_s = st.secrets["connections"]["postgresql"]
    engine = create_engine(f"postgresql://{db_s['username']}:{quote_plus(db_s['password'])}@{db_s['host']}:{db_s['port']}/{db_s['database']}")

    with st.sidebar:
        st.title("📂 MENÚ")
        st.write(f"**{'🛡️ ADMIN' if st.session_state['es_admin'] else '👤 AGENTE'}:**\n{st.session_state['agente_nombre']}")
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso", "📈 Dashboard General"])
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    if seccion == "🏠 Inicio":
        st.title("🛡️ Panel de Control")
        st.info("Bienvenido. Acceda a los Módulos para estudiar el material completo.")

    elif seccion == "📚 Módulos":
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", ["Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", "Módulo 3: Recolección"])
        
        # --- MÓDULO 1 ---
        if modulo_selec == "Módulo 1: Conceptualización":
            st.header("📖 Material: Conceptualización de Inteligencia")
            with st.expander("Ver Contenido Completo Módulo 1", expanded=True):
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición de Inteligencia</h3>
                    <p>1. Es el <b>conocimiento obtenido</b> a través del procesamiento adecuado de la información, que se brinda a los responsables de tomar decisiones.</p>
                    <p>2. Es una actividad <b>multi y transdisciplinaria</b>, compleja, dinámica y necesaria en un mundo en el cual el aprovechamiento de la oportunidad del futuro, asegura el éxito.</p>
                    <p>3. Su función es la de <b>asesoramiento</b>, proporcionando el conocimiento integrado que reduzca las diversas incertidumbres, para la toma de decisión.</p>
                    <p>4. Es la capacidad de aprender o comprender. Suele ser sinónimo del intelecto (entendimiento), pero se diferencia de este por hacer hincapié en las <b>habilidades y aptitudes</b> para manejar situaciones concretas y por beneficiarse de la experiencia sensorial.</p>
                    <br>
                    <h3>¿Qué es Inteligencia Policial?</h3>
                    <p>Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la <b>seguridad y convivencia ciudadana</b>, a fin de contribuir a la definición de políticas a cargo de las autoridades de la administración pública a nivel nacional, departamental y local, al diseño de estrategias institucionales y a orientar la ejecución de operaciones en cumplimiento de la misión policial.</p>
                    <br>
                    <h3>Inteligencia según su nivel</h3>
                    <p><b>INTELIGENCIA ESTRATÉGICA:</b> Los líderes políticos y policiales emplean algunas áreas del conjunto de conocimientos de inteligencia para la formulación de planes y políticas orientada hacia los objetivos nacionales, para llegar a decisiones relacionadas con la seguridad y bienestar de la nación.</p>
                    <p><b>INTELIGENCIA OPERACIONAL:</b> Requerida para el planeamiento de operaciones dentro de un área específica. Se concentra en la recolección, identificación, localización y análisis para apoyar en el nivel operacional, asesorando al jefe de la operación sobre el mejor empleo de las unidades disponibles y minimizar los riesgos.</p>
                    <p><b>INTELIGENCIA TÁCTICA:</b> Requerida para la conducción de operaciones tácticas al nivel de equipos. Se enfoca en las capacidades del objetivo, sus posibilidades inmediatas y el ambiente. Las posibilidades inmediatas son dinámicas, tienden a variar constantemente y no permite prever situaciones a futuro mediato.</p>
                </div>
                """, unsafe_allow_html=True)

        # --- MÓDULO 2 ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            st.header("📖 Material: Ciclo de Inteligencia")
            with st.expander("Ver Contenido Completo Módulo 2", expanded=True):
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición</h3>
                    <p>Se define como una serie de <b>cinco pasos</b> orientados a la generación de conocimiento estratégico útil, verdadero y ajustado a los requerimientos de información preestablecidos por un destinatario final (decisor), a quien se difunde selectivamente el resultado plasmado en un instrumento determinado.</p>
                    <h3>Los 5 Pasos:</h3>
                    <ul>
                        <li><b>Recolectar:</b> Obtención de la información bruta necesaria para producir la inteligencia.</li>
                        <li><b>Tratar:</b> Procesamiento y organización de los datos obtenidos.</li>
                        <li><b>Analizar:</b> Transformación de la información en inteligencia mediante la valoración y el análisis.</li>
                        <li><b>Comunicar e Integrar:</b> Difusión de los resultados a los decisores para su uso.</li>
                        <li><b>Evaluar y Retroalimentar:</b> Revisión constante del proceso para asegurar la calidad.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                

        # --- MÓDULO 3 ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material Completo: Recolección de Información")
                
                t1, t2, t3, t4 = st.tabs(["📌 Fundamentos y PHVA", "🕵️ Operaciones", "👥 Fuentes Humana", "🎤 La Entrevista"])
                
                with t1:
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>Definición de Recolección</h3>
                        <p>Consiste en juntar aquellos datos o información relevante para el objetivo de nuestra investigación. Esta información, generalmente, se encuentra de forma dispersa en nuestro entorno y, por ello, debemos desarrollar técnicas precisas para acceder a ella.</p>
                        <ul>
                            <li>Definir requerimientos de información.</li>
                            <li>Identificar fuentes potenciales de información.</li>
                            <li>Diseñar y ejecutar estrategias de recolección.</li>
                            <li>Distribuir y organizar los resultados de la recolección.</li>
                            <li>Reunir y retroalimentar.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Proceso de Recolección (PHVA)", expanded=True):
                        st.write("**PLANEAR:** Es establecer los objetivos y procesos necesarios para alcanzarlos. Planificación de la recolección, Identificar y administrar los riesgos, Planificar recursos requeridos.")
                        st.write("**HACER:** Implementación y desarrollo. Búsqueda de información, Desarrollar actividades de inteligencia, Elaborar y registrar productos, Suministrar los productos, Ejecutar controles de seguridad.")
                        st.write("**VERIFICAR:** Seguimiento y medición de los procesos. Realizar autoevaluación de control y gestión.")
                        st.write("**ACTUAR:** Tomar acciones para ajustar y mejorar continuamente el desarrollo de los procesos. Implementar acciones correctivas, preventivas o de mejora.")
                    

[Image of the PDCA cycle for continuous improvement]


                with t2:
                    st.subheader("Operaciones de Inteligencia")
                    with st.expander("Operaciones Básicas", expanded=True):
                        st.write("**Reconocimiento:** Concretar y ampliar datos del propietario, residentes, vehículos, seguridad del sitio y entorno.")
                        st.write("**Verificación:** Establecer veracidad o desvirtuar información (bases de datos, llamadas, internet).")
                        st.write("**Vigilancia:** Observación continúa y discreta para establecer rutinas.")
                        st.write("**Seguimiento:** Control sobre objetivos en movimiento (A PIE o EN VEHÍCULO).")
                        st.write("**Sonsacamiento:** Diálogo donde la fuente no percibe la intención para obtener información.")
                    with st.expander("Operaciones Especializadas", expanded=True):
                        st.write("**Infiltración:** Ubicar agentes dentro de una organización mediante una cobertura.")
                        st.write("**Penetración:** Obtener colaboración permanente de alguien que ya tiene acceso al blanco.")

                with t3:
                    st.subheader("Fuentes de Información")
                    st.write("**Tipos de Fuentes:** Abiertas o Públicas, Cerradas Especializadas, Cerradas Humanas y Técnicas.")
                    with st.expander("Fases de Administración de Fuentes Humanas", expanded=True):
                        st.write("1. Exploración (Búsqueda) | 2. Aproximación (Contacto) | 3. Registro | 4. Entrenamiento (Instruir, orientar, dirigir, controlar).")

                with t4:
                    st.subheader("La Entrevista de Inteligencia")
                    st.write("**Etapas:** Planeación, Desarrollo, Terminación e Informe.")
                    with st.expander("Tipos de entrevistador a EVITAR", expanded=True):
                        st.write("* **El estrella:** Habla más que la fuente, utiliza lenguaje rebuscado, se siente superior.")
                        st.write("* **El sordo:** Se preocupa tanto por su cuestionario que olvida escuchar a la fuente.")
                        st.write("* **El metralleta:** Bombardea con preguntas sin dar tiempo a responder.")
                        st.write("* **El enredado:** Utiliza palabras difíciles o da muchas vueltas al tema.")
                        st.write("* **El improvisado:** Hace el trabajo de manera desordenada y a la carrera.")
                        st.write("* **El estrellado:** Aquel que es tímido ante la fuente.")

                if st.button("🚀 INICIAR EXAMEN M3 (10 PREGUNTAS)"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            
            else:
                st.header("📝 Evaluación: Módulo 3 (Recolección)")
                with st.form("exam_final"):
                    c1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Técnica de vigilancia fija"])
                    c2 = st.radio("2. En PHVA, ¿qué implica la etapa HACER?", ["Planificar recursos", "Búsqueda de información y elaboración de productos", "Acciones preventivas"])
                    c3 = st.radio("3. Diferencia entre Infiltración y Penetración:", ["No hay diferencia", "Infiltración mete al agente; Penetración usa a alguien de adentro", "Infiltración es técnica"])
                    c4 = st.radio("4. ¿Cuál es la unidad básica que comprende la información?", ["El mensaje", "El dato", "El informe analítico"])
                    c5 = st.radio("5. ¿Qué busca el Reconocimiento específicamente?", ["Solo vigilar", "Concretar datos de propietarios, vehículos, seguridad y entorno", "Sonsacar a la fuente"])
                    c6 = st.radio("6. En PHVA, ¿qué acción corresponde a VERIFICAR?", ["Ejecutar controles", "Realizar autoevaluación de control y gestión", "Planificar recursos"])
                    c7 = st.radio("7. Tipo de entrevistador que olvida escuchar por mirar su cuestionario:", ["El metralleta", "El sordo", "El estrella"])
                    c8 = st.radio("8. ¿Cuál es el primer paso en la Administración de Fuentes Humanas?", ["Registro", "Entrenamiento", "Exploración (Búsqueda)"])
                    c9 = st.radio("9. Las operaciones Estructurales tienen como fin:", ["Solo flagrancias", "Desarticulación de estructuras y ruptura de cadena criminal", "Fines preventivos locales"])
                    c10 = st.radio("10. ¿Qué etapa de la entrevista es el primer contacto manteniendo armonía?", ["Planeación", "Desarrollo", "Informe"])

                    if st.form_submit_button("FINALIZAR Y GUARDAR"):
                        res = [c1=="Diálogo donde la fuente no debe percatarse de la explotación", c2=="Búsqueda de información y elaboración de productos", c3=="Infiltración mete al agente; Penetración usa a alguien de adentro", c4=="El dato", c5=="Concretar datos de propietarios, vehículos, seguridad y entorno", c6=="Realizar autoevaluación de control y gestión", c7=="El sordo", c8=="Exploración (Búsqueda)", c9=="Desarticulación de estructuras y ruptura de cadena criminal", c10=="Desarrollo"]
                        nota = (sum(res) / 10) * 100
                        try:
                            with engine.connect() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 3"})
                                conn.commit()
                            st.success(f"Nota guardada: {nota}%")
                            st.session_state['modo_examen'] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error de base de datos: {e}")

    # --- SECCIONES EXTRA ---
    elif seccion == "📊 Mi Progreso":
        st.title("Historial de Calificaciones")
        try:
            df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), engine, params={"n": st.session_state['agente_nombre']})
            st.dataframe(df, use_container_width=True)
        except: st.info("No hay registros para este usuario.")

    elif seccion == "📈 Dashboard General":
        if st.session_state['es_admin']:
            st.title("Panel Administrativo")
            df_all = pd.read_sql(text("SELECT * FROM calificaciones"), engine)
            st.dataframe(df_all)
            st.bar_chart(df_all.groupby('modulo')['nota'].mean())
        else:
            st.warning("Acceso restringido.")
