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

def verificar_intento(nombre, modulo, engine):
    try:
        query = text("SELECT nota FROM calificaciones WHERE funcionario = :f AND modulo = :m")
        with engine.connect() as conn:
            result = conn.execute(query, {"f": nombre, "m": modulo}).fetchone()
        return result[0] if result else None
    except: return None

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
            if not st.session_state['modo_examen']:
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
                        <p><b>INTELIGENCIA ESTRATÉGICA:</b> Los líderes políticos y policiales emplean algunas áreas del conjunto de conocimientos de inteligencia para la formulación de planes y políticas orientada hacia los objetivos nacionales.</p>
                        <p><b>INTELIGENCIA OPERACIONAL:</b> Requerida para el planeamiento de operaciones dentro de un área específica. Se concentra en la recolección, identificación, localización y análisis.</p>
                        <p><b>INTELIGENCIA TÁCTICA:</b> Requerida para la conducción de operaciones tácticas al nivel de equipos.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 1", engine)
                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN M1"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: st.warning(f"Examen completado. Calificación: {nota_p}%")

        # --- MÓDULO 2 ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Ciclo de Inteligencia")
                with st.expander("Ver Contenido Completo Módulo 2", expanded=True):
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>Definición</h3>
                        <p>Se define como una serie de <b>cinco pasos</b> orientados a la generación de conocimiento estratégico útil, verdadero y ajustado a los requerimientos de información preestablecidos por un destinatario final (decisor), a quien se difunde selectivamente el resultado plasmado en un instrumento determinado.</p>
                    </div>
                    <div class="lectura-box">
                        <h3>Los 5 Pasos del Ciclo:</h3>
                        <ul>
                            <li><b>Recolectar:</b> Obtención de la información bruta necesaria para producir la inteligencia.</li>
                            <li><b>Tratar:</b> Procesamiento y organización de los datos obtenidos.</li>
                            <li><b>Analizar:</b> Transformación de la información en inteligencia mediante la valoración y el análisis.</li>
                            <li><b>Comunicar e Integrar:</b> Difusión de los resultados a los decisores para su uso.</li>
                            <li><b>Evaluar y Retroalimentar:</b> Revisión constante del proceso para asegurar la calidad.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 2", engine)
                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN M2"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: st.warning(f"Examen completado. Calificación: {nota_p}%")

        # --- MÓDULO 3: RECOLECCIÓN ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material Completo: Recolección de Información")
                t1, t2, t3, t4 = st.tabs(["📌 Fundamentos y PHVA", "🕵️ Operaciones", "👥 Fuentes Humana", "🎤 La Entrevista"])
                
                with t1:
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>¿Que es información?</h3>
                        <ul>
                            <li>Conjunto de datos integrados y ordenados, que sirven para construir un mensaje basado en un cierto fenómeno o ente.</li>
                            <li>Materia prima para resolver problemas y tomar decisiones, ya que su aprovechamiento racional es la base del conocimiento.</li>
                        </ul>
                        <p><b>Dato es la unidad básica que comprende la información</b></p>
                        <p>La información está constituida por un grupo de datos ya supervisados y ordenados, que sirven para construir un mensaje basado en un cierto fenómeno. Permite resolver problemas y tomar decisiones, ya que su aprovechamiento racional es la base del conocimiento.</p>
                    </div>
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
                        st.write("**PLANEAR:** Establecer objetivos y procesos. Planificación de la recolección, Identificar riesgos, Planificar recursos.")
                        st.write("**HACER:** Implementación. Búsqueda de información, Desarrollar actividades, Elaborar productos, Ejecutar controles.")
                        st.write("**VERIFICAR:** Seguimiento. Realizar autoevaluación de control y gestión.")
                        st.write("**ACTUAR:** Mejora continua. Implementar acciones correctivas o preventivas.")

                with t2:
                    st.subheader("🕵️ Operaciones de Inteligencia")
                    st.markdown("""
                        <div class="lectura-box">
                            <h4 style='color: #D4AF37; margin-top: 0;'>Definición General</h4>
                            <p>Son actividades del servicio de policía, orientadas a la obtención de información privilegiada de personas, organizaciones, objetos y hechos que representan interés para el servicio de inteligencia policial. Para toda operación se requiere el <b>Empleo y uso de Medios Técnicos</b>.</p>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.expander("🛠️ OPERACIONES BÁSICAS", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### 🔍 Reconocimiento")
                            st.info("Actividad de inteligencia que parte de una información previamente recolectada, dirigida a concretar y ampliar los datos disponibles.")
                            st.markdown("""
                            **Desarrollo:**
                            * 👥 Grupo de trabajo y medios logísticos/tecnológicos.
                            * 🌿 Actitud natural de acuerdo al entorno.
                            * 📍 Agilidad de ubicación.
                            * 🛡️ Mantener siempre las medidas de seguridad.
                            * 📸 Realizar registros fílmicos o fotográficos.
                            * 🛣️ Conocer posibles vías de acceso del objetivo.
                            * 👤 Crear estrategias de individualización e identificación.
                            * 📝 Descripción detallada de inmuebles y personas.
                            """)
                        with col2:
                            st.markdown("### ✅ Verificación")
                            st.success("Procedimiento que pretende establecer la veracidad de los datos o desvirtuar una información.")
                            st.markdown("""
                            **Fuentes de Consulta:**
                            * 🏢 Base de datos institucionales.
                            * 🌐 Bases de datos públicas.
                            * 🤝 Agencias amigas.
                            * 💻 Internet y otros.
                            
                            **Herramientas:**
                            Llamadas telefónicas, archivos, consulta a personas y herramientas digitales.
                            """)
                        st.divider()
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            st.markdown("### 🔭 Vigilancia")
                            st.warning("*Observación continúa y discreta sobre personas, lugares o vehículos para establecer rutinas.*")
                            st.markdown("""
                            **Propósitos:**
                            * **Confirmar la ubicación** de objetivos.
                            * **Identificar vehículos/personas** que frecuentan el sitio.
                            * **Establecer cambios significativos** al lugar.
                            * **Establecer el medio de comunicación** utilizado.
                            * **Conocer las actividades** que desarrollan normalmente.
                            """)
                        with col4:
                            st.markdown("### 🚗 Seguimiento")
                            st.warning("*Actividad mediante la cual se ejerce control sobre una persona o elemento en movimiento.*")
                            st.markdown("""
                            **Propósitos:**
                            * **Identificar puntos de partida y llegada.**
                            * **Reconocer vehículos** en los que se desplaza.
                            * **Detectar posibles esquemas de seguridad.**
                            * **Conocer qué personas visita** y qué lugares frecuenta.
                            """)
                        st.divider()
                        
                        st.markdown("### 🗣️ Sonsacamiento")
                        st.markdown("> *Técnica de Inteligencia que permite la obtención de información mediante el diálogo sutil.*")
                        s1, s2 = st.columns(2)
                        with s1:
                            st.markdown("""
                            **Fase de Preparación:**
                            * **Conocimiento de la Fuente Humana.**
                            * **Identificar plenamente la misión.**
                            * **Establecer afinidad (Rapport).**
                            * **Dirección del diálogo sutil.**
                            """)
                        with s2:
                            st.markdown("""
                            **Fase de Ejecución:**
                            * **Cobertura coherente.**
                            * **Invisibilidad de intención.**
                            * **Desvirtuar sospechas.**
                            * **Continuidad sin espacios vacíos.**
                            """)

                    with st.expander("🛡️ Operaciones Especializadas", expanded=True):
                        rows = [st.columns(2), st.columns(2)]
                        content = [
                            ("Infiltración", "Ubicar agentes dentro de una organización mediante una cobertura.", "👤"),
                            ("Penetración", "Obtener colaboración permanente de alguien con acceso.", "🔑"),
                            ("Admón. de Fuentes", "Proceso de orientación, dirección y control de fuentes.", "🤝"),
                            ("Entrevista", "Obtención de información mediante intercambio de ideas.", "🎙️"),
                        ]

                        for i, (title, desc, icon) in enumerate(content):
                            with rows[i // 2][i % 2]:
                                st.subheader(f"{icon} {title}")
                                st.write(desc)
                                st.divider()

                        st.warning("**🎭 Caracterización vs Fachada:** La *caracterización* es quién dices ser; la *fachada* es el entorno físico que lo respalda.")

                with t3:
                    st.subheader("Fuentes de Información")
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>Fuentes de Información</h3>
                        <p><b>Clasificación:</b> Abiertas/Públicas, Cerradas Especializadas, Cerradas Humanas y Técnicas.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Fases de Administración de Fuentes Humanas", expanded=True):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write("#### 1. Exploración")
                            st.write("- Búsqueda / Voluntaria\n- Evaluación y motivación\n- Selección preliminar")
                            st.write("#### 2. Aproximación")
                            st.write("- La entrevista\n- Sonsacamiento\n- Evaluación")
                        with col_b:
                            st.write("#### 3. Registro")
                            st.write("- Sistema de administración de fuentes humanas")
                            st.write("#### 4. Entrenamiento")
                            st.write("- Instruir, Orientar, Dirigir y Controlar")

                with t4:
                    st.subheader("La Entrevista de Inteligencia")
                    with st.expander("Etapas de la Entrevista", expanded=True):
                        st.markdown("""
                        <div class="lectura-box">
                            <p><b>PLANEACIÓN:</b> Delimitar necesidades y objetivos.</p>
                            <p><b>DESARROLLO:</b> Conversación con armonía sin perder el control.</p>
                            <p><b>TERMINACIÓN:</b> Finalización al agotar la exploración.</p>
                            <p><b>INFORME:</b> Procesamiento para la administración.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with st.expander("Tipos de entrevistador a EVITAR", expanded=True):
                        st.write("* **El estrella:** Habla más que la fuente.\n* **El sordo:** Solo mira su cuestionario.\n* **El metralleta:** Pregunta sin parar.\n* **El enredado:** Usa palabras difíciles.\n* **El improvisado:** Desordenado.\n* **El estrellado:** Tímido.")

                nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 3", engine)
                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN M3"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: st.warning(f"Examen completado. Calificación: {nota_p}%")
            
            else:
                st.header("📝 Evaluación: Módulo 3")
                with st.form("exam_m3"):
                    c1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Vigilancia fija"])
                    c2 = st.radio("2. En PHVA, ¿qué implica la etapa HACER?", ["Planificar recursos", "Búsqueda de información y elaboración de productos", "Acciones preventivas"])
                    c3 = st.radio("3. Diferencia entre Infiltración y Penetración:", ["No hay diferencia", "Infiltración mete al agente; Penetración usa a alguien de adentro", "Infiltración es técnica"])
                    c4 = st.radio("4. ¿Cuál es la unidad básica que comprende la información?", ["El mensaje", "El dato", "El informe analítico"])
                    c5 = st.radio("5. ¿Qué busca el Reconocimiento específicamente?", ["Solo vigilar", "Concretar datos de propietarios, vehículos, seguridad y entorno", "Sonsacar"])
                    c6 = st.radio("6. En PHVA, ¿qué acción corresponde a VERIFICAR?", ["Ejecutar controles", "Realizar autoevaluación de control y gestión", "Planificar recursos"])
                    c7 = st.radio("7. Tipo de entrevistador que olvida escuchar por mirar su cuestionario:", ["El metralleta", "El sordo", "El estrella"])
                    c8 = st.radio("8. ¿Cuál es el primer paso en la Administración de Fuentes Humanas?", ["Registro", "Entrenamiento", "Exploración"])
                    c9 = st.radio("9. Las fuentes de información se clasifican en:", ["Solo Abiertas", "Abiertas, Cerradas Especializadas, Cerradas Humanas y Técnicas", "Solo Técnicas"])
                    c10 = st.radio("10. ¿Qué es información?", ["Cualquier dato suelto", "Conjunto de datos integrados y ordenados para construir un mensaje", "Un rumor"])

                    if st.form_submit_button("FINALIZAR EXAMEN"):
                        res = [c1=="Diálogo donde la fuente no debe percatarse de la explotación", c2=="Búsqueda de información y elaboración de productos", c3=="Infiltración mete al agente; Penetración usa a alguien de adentro", c4=="El dato", c5=="Concretar datos de propietarios, vehículos, seguridad y entorno", c6=="Realizar autoevaluación de control y gestión", c7=="El sordo", c8=="Exploración", c9=="Abiertas, Cerradas Especializadas, Cerradas Humanas y Técnicas", c10=="Conjunto de datos integrados y ordenados para construir un mensaje"]
                        nota = (sum(res) / 10) * 100
                        with engine.begin() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 3"})
                        st.session_state['modo_examen'] = False
                        st.rerun()

    elif seccion == "📊 Mi Progreso":
        st.title("Historial de Calificaciones")
        try:
            with engine.connect() as conn:
                df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), conn, params={"n": st.session_state['agente_nombre']})
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else: st.info("No hay registros aún.")
        except: st.info("No hay registros aún.")

    elif seccion == "📈 Dashboard General":
        if st.session_state['es_admin']:
            st.title("🛡️ Panel Administrativo")
            with engine.connect() as conn:
                df_all = pd.read_sql(text("SELECT funcionario, modulo, nota, fecha FROM calificaciones"), conn)
            st.dataframe(df_all, use_container_width=True)
            st.divider()
            if not df_all.empty:
                st.bar_chart(df_all.groupby('modulo')['nota'].mean())
        else: st.warning("Acceso restringido a administradores.")
