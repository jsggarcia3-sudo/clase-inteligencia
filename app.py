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
    .sub-seccion { border-bottom: 1px solid #D4AF37; margin-top: 20px; margin-bottom: 10px; color: #D4AF37; font-weight: bold; }
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
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso"] + (["📈 Dashboard General"] if st.session_state['es_admin'] else []))
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    # --- INICIO ---
    if seccion == "🏠 Inicio":
        st.title("🛡️ Panel Principal")
        st.write(f"Bienvenido, {st.session_state['agente_nombre']}. Seleccione un módulo para estudiar el material completo.")

    # --- MÓDULOS ---
    elif seccion == "📚 Módulos":
        modulo_selec = st.selectbox("Seleccione Módulo:", ["Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", "Módulo 3: Recolección"])
        
        # --- MÓDULO 1: CONCEPTUALIZACIÓN (TODO EL TEXTO) ---
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
                    p1 = st.radio("1. Función de la inteligencia:", ["Duda", "Asesoramiento para reducir incertidumbres", "Fuerza"])
                    p2 = st.radio("2. Nivel para planes nacionales:", ["Estratégica", "Operacional", "Táctica"])
                    if st.form_submit_button("GUARDAR M1"): st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 2: CICLO (TODO EL TEXTO) ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Ciclo de Inteligencia")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición</h3>
                    <p>Se define como una serie de <b>cinco pasos</b> orientados a la generación de conocimiento estratégico útil, verdadero y ajustado a los requerimientos de información preestablecidos por un destinatario final (decisor), a quien se difunde selectivamente el resultado plasmado en un instrumento determinado.</p>
                    <h3>Pasos:</h3>
                    <ul>
                        <li>Recolectar</li>
                        <li>Tratar</li>
                        <li>Analizar</li>
                        <li>Comunicar e Integrar</li>
                        <li>Evaluar y Retroalimentar</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 INICIAR EVALUACIÓN M2"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m2"):
                    p1 = st.radio("¿Pasos del ciclo?", ["5 pasos", "3 pasos"])
                    if st.form_submit_button("GUARDAR M2"): st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 3: RECOLECCIÓN (ESTRUCTURA COMPLETA SIN OMISIONES) ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material Completo: Recolección de Información")
                
                with st.expander("1. Definición y Proceso de Recolección", expanded=True):
                    st.markdown("""
                    La recolección de información de inteligencia consiste en juntar aquellos datos o información relevante para el objetivo de nuestra investigación. Esta información, generalmente, se encuentra de forma dispersa en nuestro entorno y, por ello, debemos desarrollar técnicas precisas para acceder a ella.
                    * Definir requerimientos de información
                    * Identificar fuentes potenciales de información
                    * Diseñar y ejecutar estrategias de recolección
                    * Distribuir y organizar los resultados de la recolección
                    * Reunir y retroalimentar
                    """)
                    
                    st.subheader("Recolección de Información (PHVA)")
                    st.write("**PLANEAR:** Establecer objetivos y procesos necesarios. Planificación, Identificar riesgos, Planificar recursos.")
                    st.write("**HACER:** Implementación. Búsqueda de información, Desarrollar actividades, Elaborar productos, Suministrar productos, Controles de seguridad.")
                    st.write("**VERIFICAR:** Seguimiento y medición. Realizar autoevaluación de control y gestión.")
                    st.write("**ACTUAR:** Ajustar y mejorar continuamente. Implementar acciones correctivas, preventivas o de mejora.")
                    

[Image of the PDCA cycle for continuous improvement]


                with st.expander("2. ¿Qué es Información y Datos?"):
                    st.write("**Información:** Conjunto de datos integrados y ordenados que sirven para construir un mensaje. Materia prima para resolver problemas y tomar decisiones.")
                    st.write("**Dato:** Es la unidad básica que comprende la información.")
                    st.subheader("Fuentes de Información")
                    st.write("* Abiertas o Públicas")
                    st.write("* Cerradas Especializadas")
                    st.write("* Cerradas Humanas")
                    st.write("* Técnicas")

                with st.expander("3. Operaciones de Inteligencia"):
                    st.write("Actividades orientadas a la obtención de información privilegiada de personas, organizaciones, objetos y hechos.")
                    st.markdown("""
                    **Básicas:**
                    * **Reconocimiento:** Parte de información previa para concretar datos (propietario, vehículos, seguridad, vías).
                    * **Verificación:** Pretende establecer veracidad a través de bases de datos, fuentes humanas, etc.
                    * **Vigilancia:** Observación continua y discreta sobre persona o lugar para establecer rutinas.
                    * **Seguimiento:** Control sobre persona o elemento en movimiento (A pie / Vehículo).
                    * **Sonsacamiento:** Diálogo donde la fuente no debe percatarse de la explotación ni de la intención.
                    
                    **Especializadas:**
                    * **Admón de F.H. / Entrevista**
                    * **Infiltración:** Ubicar agentes dentro de una organización.
                    * **Penetración:** Obtener colaboración de alguien que ya está dentro.
                    * **Caracterización y Fachada**
                    """)

                with st.expander("4. Administración de Fuentes Humanas y Entrevista"):
                    st.write("**Fases de Admón:** Exploración (Búsqueda) -> Aproximación (Contacto) -> Registro -> Entrenamiento.")
                    st.subheader("Tipos de Entrevistador (A EVITAR)")
                    st.write("* **El estrella:** Se siente superior y habla más que la fuente.")
                    st.write("* **El estrellado:** Tímido, deja desviar el tema.")
                    st.write("* **El improvisado:** No prepara nada.")
                    st.write("* **El sordo:** Solo mira su cuestionario.")
                    st.write("* **El enredado:** Usa palabras difíciles.")
                    st.write("* **El metralleta:** No deja tiempo de responder.")
                    st.write("**Etapas:** Planeación, Desarrollo, Terminación e Informe.")

                with st.expander("5. Operaciones según su Nivel"):
                    st.write("**Estratégicas:** Alto Valor, cabecillas (Nacional/Local).")
                    st.write("**Estructurales:** Desarticulación de estructuras y ruptura de cadena criminal.")
                    st.write("**Impacto:** Flagrancias y requerimientos judiciales.")
                    st.write("**Comunitaria:** Unión con comunidad y autoridades locales.")

                if st.button("🚀 INICIAR EVALUACIÓN M3"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m3"):
                    p1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no nota la intención", "Vigilancia fija"])
                    p2 = st.radio("2. En PHVA, ¿qué es 'Hacer'?", ["Planear recursos", "Búsqueda de info y elaboración de productos", "Corregir errores"])
                    p3 = st.radio("3. ¿Diferencia entre Infiltración y Penetración?", ["Infiltración mete al agente; Penetración usa a alguien de adentro", "Son iguales"])
                    if st.form_submit_button("FINALIZAR M3"): st.session_state['modo_examen']=False; st.rerun()

    # --- PROGRESO ---
    elif seccion == "📊 Mi Progreso":
        df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), engine, params={"n": st.session_state['agente_nombre']})
        st.dataframe(df, use_container_width=True)
