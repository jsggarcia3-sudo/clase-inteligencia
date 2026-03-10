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
    # Conexión a Base de Datos
    db_s = st.secrets["connections"]["postgresql"]
    engine = create_engine(f"postgresql://{db_s['username']}:{quote_plus(db_s['password'])}@{db_s['host']}:{db_s['port']}/{db_s['database']}")

    with st.sidebar:
        st.title("📂 MENÚ")
        st.write(f"**{'🛡️ ADMIN' if st.session_state['es_admin'] else '👤 AGENTE'}:**\n{st.session_state['agente_nombre']}")
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso"] + (["📈 Dashboard General"] if st.session_state['es_admin'] else []))
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    if seccion == "🏠 Inicio":
        st.title("🛡️ Panel de Control")
        st.info("Bienvenido. Seleccione '📚 Módulos' para acceder al contenido técnico completo.")

    elif seccion == "📚 Módulos":
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", ["Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", "Módulo 3: Recolección"])
        
        # --- MÓDULO 1 ---
        if modulo_selec == "Módulo 1: Conceptualización":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Conceptualización de Inteligencia")
                st.markdown("""
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
                    <p><b>INTELIGENCIA ESTRATÉGICA:</b> Los líderes políticos y policiales emplean algunas áreas del conjunto de conocimientos de inteligencia para la formulación de planes y políticas orientada hacia los objetivos nacionales, para llegar a decisiones relacionadas con la seguridad y bienestar de la nación.</p>
                    <p><b>INTELIGENCIA OPERACIONAL:</b> Requerida para el planeamiento de operaciones dentro de un área específica. Se concentra en la recolección, identificación, localización y análisis para apoyar en el nivel operacional, asesorando al jefe de la operación sobre el mejor empleo de las unidades disponibles y minimizar los riesgos.</p>
                    <p><b>INTELIGENCIA TÁCTICA:</b> Requerida para la conducción de operaciones tácticas al nivel de equipos. Se enfoca en las capacidades del objetivo, sus posibilidades inmediatas y el ambiente. Las posibilidades inmediatas son dinámicas, tienden a variar constantemente y no permite prever situaciones a futuro mediato.</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 INICIAR EVALUACIÓN M1"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m1"):
                    p1 = st.radio("Función de la inteligencia:", ["Duda", "Asesoramiento para reducir incertidumbres", "Fuerza"])
                    if st.form_submit_button("Guardar Nota M1"): st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 2 ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Ciclo de Inteligencia")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición</h3>
                    <p>Se define como una serie de <b>cinco pasos</b> orientados a la generación de conocimiento estratégico útil, verdadero y ajustado a los requerimientos de información preestablecidos por un destinatario final (decisor), a quien se difunde selectivamente el resultado plasmado en un instrumento determinado.</p>
                    <h3>Pasos:</h3>
                    <ul>
                        <li><b>Recolectar:</b> Obtención de datos relevantes.</li>
                        <li><b>Tratar:</b> Procesamiento y organización.</li>
                        <li><b>Analizar:</b> Transformación en conocimiento.</li>
                        <li><b>Comunicar e Integrar:</b> Difusión al decisor.</li>
                        <li><b>Evaluar y Retroalimentar:</b> Ajuste y mejora.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 INICIAR EVALUACIÓN M2"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m2"):
                    p1 = st.radio("¿Pasos del ciclo?", ["5 pasos", "3 pasos"])
                    if st.form_submit_button("Guardar Nota M2"): st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 3 ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Recolección de Información")
                
                with st.expander("1. Definición y Proceso de Recolección", expanded=True):
                    st.markdown("""
                    La recolección de información de inteligencia consiste en juntar aquellos datos o información relevante para el objetivo de nuestra investigación. Esta información, generalmente, se encuentra de forma dispersa en nuestro entorno y, por ello, debemos desarrollar técnicas precisas para acceder a ella.
                    * Definir requerimientos de información.
                    * Identificar fuentes potenciales de información.
                    * Diseñar y ejecutar estrategias de recolección.
                    * Distribuir y organizar los resultados de la recolección.
                    * Reunir y retroalimentar.
                    """)
                    
                    st.subheader("Recolección de Información (PHVA)")
                    st.write("**PLANEAR:** Establecer objetivos y procesos necesarios. Planificación de la recolección, Identificar y administrar riesgos, Planificar recursos.")
                    st.write("**HACER:** Implementación. Búsqueda de información, Desarrollar actividades, Elaborar y registrar productos, Suministrar productos, Controles de seguridad.")
                    st.write("**VERIFICAR:** Seguimiento y medición. Realizar autoevaluación de control y gestión.")
                    st.write("**ACTUAR:** Ajustar y mejorar continuamente. Implementar acciones correctivas, preventivas o de mejora.")

                with st.expander("2. ¿Qué es Información y Datos?"):
                    st.write("**¿Qué es información?** Conjunto de datos integrados y ordenados que sirven para construir un mensaje basado en un cierto fenómeno. Materia prima para resolver problemas.")
                    st.write("**Dato:** Es la unidad básica que comprende la información.")
                    st.subheader("Fuentes de Información")
                    st.write("* Abiertas o Públicas | Cerradas Especializadas | Cerradas Humanas | Técnicas")

                with st.expander("3. Operaciones de Inteligencia"):
                    st.markdown("""
                    **Básicas:**
                    * **Reconocimiento:** Concretar datos de propietario, residentes, vehículos y seguridad del sitio.
                    * **Verificación:** Establecer veracidad o desvirtuar información.
                    * **Vigilancia:** Observación continua y discreta para establecer rutinas.
                    * **Seguimiento:** Control sobre objetivos en movimiento (A pie / Vehículo).
                    * **Sonsacamiento:** Diálogo donde la fuente no percibe la intención del agente.
                    
                    **Especializadas:**
                    * **Infiltración:** Ubicar agentes dentro de una organización con una cobertura.
                    * **Penetración:** Obtener colaboración de una persona que ya pertenece a la organización.
                    """)

                with st.expander("4. Administración de Fuentes Humanas y Entrevista"):
                    st.write("**Fases de Admón:** Exploración -> Aproximación -> Registro -> Entrenamiento.")
                    st.subheader("Tipos de Entrevistador (A EVITAR)")
                    st.write("* **El estrella:** Habla más que la fuente. | **El sordo:** Olvida escuchar por mirar el cuestionario.")
                    st.write("* **El metralleta:** No da tiempo de responder. | **El enredado:** Usa palabras difíciles.")
                    st.write("**Etapas de Entrevista:** Planeación, Desarrollo, Terminación e Informe.")

                if st.button("🚀 INICIAR EVALUACIÓN M3"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m3"):
                    p1 = st.radio("¿Qué busca el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no nota la intención", "Vigilancia"])
                    if st.form_submit_button("FINALIZAR M3"): 
                        st.success("Nota guardada"); st.session_state['modo_examen']=False; st.rerun()

    elif seccion == "📊 Mi Progreso":
        st.title("Historial Personal")
        st.info("Aquí aparecerán sus resultados almacenados.")
