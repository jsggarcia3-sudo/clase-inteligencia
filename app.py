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

# --- 1. CONFIGURACIÓN INICIAL DE ESTADO ---
if 'modulo_activo' not in st.session_state:
    st.session_state['modulo_activo'] = None

# --- 2. SIDEBAR (Aquí se define la variable 'seccion') ---
with st.sidebar:
    st.title("📂 MENÚ")
    opciones = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso", "📈 Dashboard General"]
    
    # Manejo de redirección dinámica
    if 'seccion_ir' in st.session_state:
        # Buscamos el índice de la sección a la que queremos saltar
        try:
            indice_defecto = opciones.index(st.session_state['seccion_ir'])
        except ValueError:
            indice_defecto = 0
        del st.session_state['seccion_ir']
    else:
        indice_defecto = 0

    # DEFINICIÓN CRÍTICA: Aquí nace la variable 'seccion'
    seccion = st.radio("Ir a:", opciones, index=indice_defecto)

# --- 3. CUERPO PRINCIPAL (Fuera del Sidebar) ---

if seccion == "🏠 Inicio":
    # --- CSS PARA ESTILO TECNOLÓGICO ---
    st.markdown("""
    <style>
    .card-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px; padding: 25px; text-align: center;
        transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        min-height: 220px; display: flex; flex-direction: column; justify-content: center;
    }
    .card-container:hover {
        border: 1px solid #D4AF37; transform: translateY(-5px);
        background: rgba(212, 175, 55, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🛡️ CORE INTELLIGENCE SYSTEM</h1>", unsafe_allow_html=True)
    
    # Definición de Módulos
    modulos_home = [
        {"id": "M1", "tit": "Módulo 1", "sub": "Conceptualización", "icon": "📖", "full": "Módulo 1: Conceptualización"},
        {"id": "M2", "tit": "Módulo 2", "sub": "Ciclo de Inteligencia", "icon": "🔄", "full": "Módulo 2: Ciclo de Inteligencia"},
        {"id": "M3", "tit": "Módulo 3", "sub": "Recolección", "icon": "🕵️", "full": "Módulo 3: Recolección"},
        {"id": "M4", "tit": "Módulo 4", "sub": "Tratamiento", "icon": "📊", "full": "Módulo 4: Tratamiento"},
        {"id": "M5", "tit": "Módulo 5", "sub": "Análisis", "icon": "🧠", "full": "Módulo 5: Análisis"},
        {"id": "M6", "tit": "Módulo 6", "sub": "Comunicación", "icon": "📢", "full": "Módulo 6: Comunicación"},
        {"id": "M7", "tit": "Módulo 7", "sub": "Evaluación", "icon": "🔄", "full": "Módulo 7: Evaluación"}
    ]

    cols = st.columns(3)
    for i, m in enumerate(modulos_home):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card-container">
                <div style="font-size: 3em; margin-bottom: 10px;">{m['icon']}</div>
                <h4 style="color: #D4AF37; margin: 0;">{m['tit']}</h4>
                <p style="color: white; font-size: 0.8em; opacity: 0.7;">{m['sub']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"ACCEDER {m['id']}", key=f"btn_h_{m['id']}", use_container_width=True):
                st.session_state['modulo_activo'] = m['full']
                st.session_state['seccion_ir'] = "📚 Módulos"
                st.rerun()

elif seccion == "📚 Módulos":
    modulo_selec = st.session_state.get('modulo_activo', None)

    if modulo_selec is None:
        st.info("Seleccione un módulo en el Inicio o use el menú lateral.")
    else:
        if st.button("⬅️ VOLVER AL PANEL"):
            st.session_state['modulo_activo'] = None
            st.rerun()

        # --- CONTENIDO DINÁMICO ---
        if modulo_selec == "Módulo 5: Análisis":
            st.header("🧠 Módulo 5: Análisis de Inteligencia")
            
            # Integración de tu imagen "Línea del conocimiento analítico"
            st.subheader("La Línea del Conocimiento Analítico")
            st.image("image_4199d8.png", use_container_width=True)
            
            with st.expander("📝 Explicación Técnica de la Gráfica", expanded=True):
                st.markdown("""
                El análisis de inteligencia no es estático, se mueve en una línea temporal:
                * **Pasado:** Se basa en **Antecedentes** y la **Memoria Histórica**.
                * **Presente:** Se enfoca en la **Situación Actual** mediante la **Interpretación**.
                * **Futuro:** Busca la **Proyección** para anticipar escenarios.
                """)

elif seccion == "📚 Módulos":
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", ["Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", "Módulo 3: Recolección", "Módulo 4: Tratamiento", "Módulo 5: Análisis", "Módulo 6: Comunicación", "Módulo 7: Evaluación"])

             
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

        # --- MÓDULO 3 ---
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

       # --- MÓDULO 4: TRATAMIENTO DE LA INFORMACIÓN ---
        elif modulo_selec == "Módulo 4: Tratamiento":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Tratamiento de la Información")
                
                # SISTEMA DE CUATRO PESTAÑAS - TODO INCLUIDO
                tab_cont, tab_tipos, tab_comp, tab_4x4 = st.tabs([
                    "📌 Fundamentos", 
                    "🔍 Tipos y Elementos (EEI)", 
                    "🛠️ Componentes", 
                    "📊 Código 4x4"
                ])
                
                with tab_cont:
                    with st.expander("Ver Contenido Completo Módulo 4", expanded=True):
                        st.markdown("""
                        <div class="lectura-box">
                            <h3>Definición</h3>
                            <p>Procedimiento <b>sistemático</b> que consiste en someter todos los datos e información recolectada a un proceso de organización, clasificación y valoración preliminar, con el fin de garantizar que su registro y almacenamiento en bases de datos se enmarque en los fines de la actividad de inteligencia y contrainteligencia contenidos en la <b>Constitución y la Jurisprudencia nacional</b>.</p>
                        </div>
                        <div class="lectura-box">
                            <h3>Procedimiento y Finalidad</h3>
                            <p>Consiste en organizar la información con el fin de determinar la <b>utilidad</b> de la misma y su <b>pertinencia</b> a los objetivos o la misión. Una adecuada organización de la información:</p>
                            <ul>
                                <li>Evita la saturación.</li>
                                <li>Coadyuva a resolver en forma efectiva las prioridades.</li>
                                <li>Garantiza el desarrollo normal de los procesos operacionales.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                        st.subheader("📊 Esquema de Tratamiento")
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            st.info("**Flujo de Trabajo:**\n\nInsumos ➡️ Proceso ➡️ Producto")
                        with col_e2:
                            st.success("**Transformación:**\n\nInformación ➡️ Transformación ➡️ Inteligencia")
                        
                        st.divider()
                        st.markdown("""
                        <div class="lectura-box" style="background-color: #003366; border: 2px solid #D4AF37;">
                            <h3 style="text-align: center;">Ecuación de Tratamiento</h3>
                            <h2 style="text-align: center; color: #D4AF37;">Información + Conocimiento = Decisión</h2>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_tipos:
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4>💡 Tipos de Información</h4>
                            <p><b>1. Genérica:</b> Es la información de contexto o referencia que no tiene un objetivo específico inmediato pero ayuda a entender el entorno general.</p>
                            <p><b>2. Específica:</b> Información puntual y detallada sobre un blanco, organización o fenómeno particular, necesaria para la toma de decisiones tácticas u operativas.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_t2:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4>🔑 Elementos Esenciales de Información (EEI)</h4>
                            <p>Son las preguntas fundamentales que el analista debe responder para convertir el dato en conocimiento útil:</p>
                            <ul>
                                <li><b>¿QUÉ?:</b> El hecho o fenómeno observado.</li>
                                <li><b>¿CUÁNDO?:</b> Temporalidad y cronología.</li>
                                <li><b>¿DÓNDE?:</b> Ubicación geográfica o espacial.</li>
                                <li><b>¿CÓMO?:</b> El modus operandi o método.</li>
                                <li><b>¿QUIÉN?:</b> Actores, sujetos y organizaciones.</li>
                                <li><b>¿POR QUÉ?:</b> Causas y motivaciones.</li>
                                <li><b>¿PARA QUÉ?:</b> El objetivo o finalidad del hecho.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_comp:
                    st.subheader("⚙️ Componentes del Tratamiento de Información")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4>📂 ORGANIZACIÓN</h4>
                            <ul>
                                <li><b>Tipo de información:</b> Determinar si es técnica, humana o abierta.</li>
                                <li><b>Blanco:</b> Identificar el objetivo al que pertenece.</li>
                                <li><b>Prioridad:</b> Urgencia de la información.</li>
                            </ul>
                        </div>
                        <div class="lectura-box">
                            <h4>🛡️ CLASIFICACIÓN</h4>
                            <ul>
                                <li><b>Origen:</b> De dónde proviene la información.</li>
                                <li><b>Estado:</b> Fase actual del procesamiento (Preliminar/Final).</li>
                                <li><b>Nivel de Seg.:</b> Restricción según sensibilidad (Secreto, Reservado).</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4>⚖️ VALORACIÓN</h4>
                            <ul>
                                <li><b>Oportuna:</b> Si el dato llega en el momento útil.</li>
                                <li><b>Confiable:</b> Según el historial de la fuente.</li>
                                <li><b>Creíble:</b> Si el contenido tiene lógica y coherencia.</li>
                            </ul>
                        </div>
                        <div class="lectura-box">
                            <h4>📝 REGISTRO</h4>
                            <ul>
                                <li><b>Cronológico:</b> Ordenado por fecha y hora.</li>
                                <li><b>Detallado:</b> Incluye todos los pormenores.</li>
                                <li><b>Sistemático:</b> Bajo formatos y protocolos estandarizados.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_4x4:
                    st.subheader("📋 Matriz de Evaluación 4x4")
                    st.write("Sistema estandarizado para proveer seguridad y establecer la autenticidad y precisión de la información.")
                    
                    st.markdown("""
                    <style>
                        .t-4x4 { width: 100%; border-collapse: collapse; color: white; margin-top: 10px;}
                        .t-4x4 th { background-color: #D4AF37; color: #001226; padding: 10px; border: 1px solid #444; text-align: center; }
                        .t-4x4 td { padding: 10px; border: 1px solid #444; background-color: #002b55; font-size: 0.85em; vertical-align: middle; }
                        .perc-100 { background-color: #4CAF50 !important; font-weight: bold; text-align: center; color: white; width: 60px; }
                        .perc-75 { background-color: #FFEB3B !important; color: black !important; font-weight: bold; text-align: center; width: 60px; }
                        .perc-50 { background-color: #FF9800 !important; font-weight: bold; text-align: center; color: white; width: 60px; }
                        .perc-25 { background-color: #F44336 !important; font-weight: bold; text-align: center; color: white; width: 60px; }
                        .cod-cell { text-align: center; font-weight: bold; background-color: #003366 !important; width: 40px; font-size: 1.1em !important; }
                        .ejemplo-box { background-color: #0e1117; padding: 15px; border-radius: 5px; border-left: 5px solid #D4AF37; margin-top: 10px; }
                    </style>
                    <table class="t-4x4">
                        <tr>
                            <th colspan="2">CONFIABILIDAD DE LA FUENTE</th>
                            <th colspan="2">CREDIBILIDAD DE LA INFORMACIÓN</th>
                            <th>%</th>
                        </tr>
                        <tr>
                            <td class="cod-cell">A</td>
                            <td>Sin duda de autenticidad o fuente confiable en casos anteriores.</td>
                            <td class="cod-cell">1</td>
                            <td>Información conocida y confirmada como cierta sin duda.</td>
                            <td class="perc-100">100</td>
                        </tr>
                        <tr>
                            <td class="cod-cell">B</td>
                            <td>Información ha resultado cierta en la mayoría de los casos.</td>
                            <td class="cod-cell">2</td>
                            <td>Información conocida de primera mano por la fuente.</td>
                            <td class="perc-75">75</td>
                        </tr>
                        <tr>
                            <td class="cod-cell">C</td>
                            <td>Información en el pasado NO ha resultado cierta en la mayoría de los casos.</td>
                            <td class="cod-cell">3</td>
                            <td>No es de primera mano, pero puede ser corroborada por fuentes alternas.</td>
                            <td class="perc-50">50</td>
                        </tr>
                        <tr>
                            <td class="cod-cell">D</td>
                            <td>Fuentes no utilizadas o dudas sobre su autenticidad.</td>
                            <td class="cod-cell">4</td>
                            <td>No es de primera mano y NO puede ser corroborada por ningún medio.</td>
                            <td class="perc-25">25</td>
                        </tr>
                    </table>
                    """, unsafe_allow_html=True)

                    st.divider()
                    st.subheader("💡 Ejemplos Prácticos de Clasificación")
                    
                    col_ex1, col_ex2 = st.columns(2)
                    
                    with col_ex1:
                        st.markdown("""
                        <div class="ejemplo-box">
                            <h4 style="color: #4CAF50;">Nivel A-1 (100%)</h4>
                            <p><b>Escenario:</b> Un agente encubierto con historial impecable entrega un video original de una reunión ilícita grabada hace una hora.</p>
                            <small><i>La fuente es confiable (A) y la prueba es irrefutable (1).</i></small>
                        </div>
                        <div class="ejemplo-box">
                            <h4 style="color: #FFEB3B;">Nivel B-2 (75%)</h4>
                            <p><b>Escenario:</b> Un informante que suele dar datos reales reporta que vio personalmente la llegada de un cargamento sospechoso.</p>
                            <small><i>La fuente es usualmente cierta (B) y lo vio de primera mano (2).</i></small>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_ex2:
                        st.markdown("""
                        <div class="ejemplo-box">
                            <h4 style="color: #FF9800;">Nivel C-3 (50%)</h4>
                            <p><b>Escenario:</b> Una persona con historial de mentiras afirma que escuchó un rumor sobre un bloqueo; el dato coincide con un post en redes.</p>
                            <small><i>Fuente dudosa (C), información de "oídas" pero corroborable externamente (3).</i></small>
                        </div>
                        <div class="ejemplo-box">
                            <h4 style="color: #F44336;">Nivel D-4 (25%)</h4>
                            <p><b>Escenario:</b> Una llamada anónima sin antecedentes alerta sobre una amenaza, pero no hay ninguna otra prueba que lo respalde.</p>
                            <small><i>Fuente desconocida (D) y dato imposible de verificar (4).</i></small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.caption("Nota: El analista debe priorizar siempre la búsqueda de corroboración para elevar los niveles C y D.")

                # --- Lógica de Examen M4 ---
                nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 4", engine)
                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN M4"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: st.warning(f"Examen completado. Calificación: {nota_p}%")
            
            else:
                st.header("📝 Evaluación: Módulo 4")
                with st.form("exam_m4"):
                    m4_1 = st.radio("1. ¿Qué implica la etapa de 'Organización'?", ["Captura de objetivos", "Determinar tipo de información, blanco y prioridad", "Publicar en redes sociales"])
                    m4_2 = st.radio("2. Según la matriz 4x4, el código 'C-3' representa un porcentaje de:", ["100%", "75%", "50%"])
                    m4_3 = st.radio("3. ¿Cuál es el objetivo primordial del Tratamiento?", ["Hacer archivos grandes", "Garantizar que el registro se enmarque en la Constitución y Jurisprudencia", "Sonsacar fuentes"])
                    m4_4 = st.radio("4. ¿Qué elemento de los EEI responde al 'Por qué'?", ["Temporalidad", "Causas y motivaciones", "Ubicación"])
                    m4_5 = st.radio("5. ¿Qué significa que una información sea 'Específica'?", ["Contexto general", "Puntual y detallada sobre un blanco o fenómeno", "Un rumor sin fundamento"])

                    if st.form_submit_button("FINALIZAR EXAMEN"):
                        res_m4 = [
                            m4_1 == "Determinar tipo de información, blanco y prioridad",
                            m4_2 == "50%",
                            m4_3 == "Garantizar que el registro se enmarque en la Constitución y Jurisprudencia",
                            m4_4 == "Causas y motivaciones",
                            m4_5 == "Puntual y detallada sobre un blanco o fenómeno"
                        ]
                        nota_m4 = (sum(res_m4) / 5) * 100
                        with engine.begin() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota_m4, "m": "Módulo 4"})
                        st.session_state['modo_examen'] = False
                        st.rerun()

    # --- MÓDULO 5: ANÁLISIS DE LA INFORMACIÓN ---
        elif modulo_selec == "Módulo 5: Análisis":
            if not st.session_state['modo_examen']:
                st.header("🧠 Material: Análisis de la Información")
                
                # PESTAÑAS DEL MÓDULO 5 (Corregidas para coincidir con el contenido)
                tab_estudio, tab_proceso, tab_lca, tab_sintesis = st.tabs([
                    "🔬 Estudio Especializado", 
                    "🧩 Proceso de Análisis", 
                    "⏳ Línea LCA",
                    "💡 Síntesis y Resultados"
                ])
                
                with tab_estudio:
                    st.subheader("Estudio Especializado de la Información")
                    st.write("El análisis es un proceso cuyo objeto es **generar conocimiento**, con base en la información disponible.")
                    
                    # Representación visual del flujo (Basado en imagen 1)
                    st.markdown("""
                    <div style="display: flex; align-items: center; justify-content: center; background-color: #001f3f; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37;">
                        <div style="background-color: #0056b3; color: white; padding: 20px; border-radius: 5px; text-align: center; font-weight: bold; width: 25%;">
                            ESTUDIO ESPECIALIZADO DE INFORMACIÓN
                        </div>
                        <div style="width: 50%; padding: 0 20px;">
                            <div style="background-color: #a9a9a9; color: #1a1a1a; margin: 5px; padding: 8px; border-radius: 3px; text-align: center; font-weight: bold; clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);">INTERPRETACIÓN</div>
                            <div style="background-color: #a9a9a9; color: #1a1a1a; margin: 5px; padding: 8px; border-radius: 3px; text-align: center; font-weight: bold; clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);">INTEGRACIÓN</div>
                            <div style="background-color: #a9a9a9; color: #1a1a1a; margin: 5px; padding: 8px; border-radius: 3px; text-align: center; font-weight: bold; clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);">HIPÓTESIS</div>
                            <div style="background-color: #a9a9a9; color: #1a1a1a; margin: 5px; padding: 8px; border-radius: 3px; text-align: center; font-weight: bold; clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);">CONCLUSIONES</div>
                        </div>
                        <div style="background-color: #f0f0f0; color: #333; padding: 20px; border-radius: 5px; text-align: center; font-weight: bold; width: 25%; border: 2px dashed #0056b3;">
                            GENERAR CONOCIMIENTO A PARTIR DE LA INFORMACIÓN
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("""
                    **Fases del Análisis:**
                    1. **Interpretación:** Dar sentido a los datos aislados.
                    2. **Integración:** Unir piezas para ver el cuadro completo.
                    3. **Hipótesis:** Plantear suposiciones técnicas.
                    4. **Conclusiones:** Resultados finales.
                    """)

                with tab_proceso:
                    st.subheader("🧩 El Proceso Analítico (Descomposición)")
                    
                    # Panel Superior de Actividades (Basado en imagen 3)
                    st.markdown("""
                    <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                        <div style="display: flex; justify-content: center; gap: 15px;">
                            <div style="background: white; border: 1px solid #999; padding: 5px 15px; color: #002b55; font-weight: bold;">Seleccionar</div>
                            <div style="background: white; border: 1px solid #999; padding: 5px 15px; color: #002b55; font-weight: bold;">Clasificar</div>
                            <div style="background: white; border: 1px solid #999; padding: 5px 15px; color: #002b55; font-weight: bold;">Organizar</div>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 15px; margin-top: 10px;">
                            <div style="background: #e9ecef; border: 1px solid #999; padding: 5px 15px; color: #333;">Identificar</div>
                            <div style="background: #e9ecef; border: 1px solid #999; padding: 5px 15px; color: #333;">Temas</div>
                            <div style="background: #e9ecef; border: 1px solid #999; padding: 5px 15px; color: #333;">Ideas</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        st.markdown('<div style="text-align:center; background:#f2dede; padding:10px; border-radius:10px; height:200px;">'
                                    '<b>EL TODO</b><br>🧩<br><small>Objeto de análisis. Tendencias y patrones.</small></div>', unsafe_allow_html=True)
                    with col_f2:
                        st.markdown('<div style="text-align:center; background:#fcf8e3; padding:10px; border-radius:10px; height:200px;">'
                                    '<b>ANALIZAR</b><br>🔍<br><small>Descomponer. Identificar el elemento que modifica el patrón.</small></div>', unsafe_allow_html=True)
                    with col_f3:
                        st.markdown('<div style="text-align:center; background:#d9edf7; padding:10px; border-radius:10px; height:200px;">'
                                    '<b>SINTETIZAR</b><br>💡<br><small>Recomponer. Significado de las partes sumadas.</small></div>', unsafe_allow_html=True)
                    st.caption("Analizar es descomponer el todo; sintetizar es recomponer para entender el significado final.")

                with tab_lca:
                    st.subheader("⏳ LCA: Línea del Conocimiento Analítico")
                    # Visual de reloj de arena (Basado en imagen 4)
                    st.markdown("""
                    <div style="display: flex; justify-content: space-around; align-items: center; background: linear-gradient(90deg, #2c5d63, #c0392b, #f39c12); padding: 30px; border-radius: 15px; color: white; font-weight: bold;">
                        <div style="text-align: center;">PASADO<br><small>Antecedentes<br>Memoria Histórica</small></div>
                        <div style="font-size: 2em;">➡️</div>
                        <div style="text-align: center; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px;">PRESENTE<br><small>Situación Actual<br>Interpretación</small></div>
                        <div style="font-size: 2em;">➡️</div>
                        <div style="text-align: center;">FUTURO<br><small>Proyección<br>Prospectiva</small></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("La LCA permite transformar la memoria histórica en proyecciones de futuro mediante la interpretación del presente.")

                with tab_sintesis:
                    st.subheader("🎯 Resultados y Cursos de Acción")
                    st.markdown("""
                    El análisis genera conocimiento para:
                    * **Formular Hipótesis:** Suposiciones basadas en datos técnicos.
                    * **Definir Escenarios:** Posibles evoluciones del fenómeno.
                    * **Cursos de Acción:** Recomendaciones estratégicas para el mando.
                    """)
                    st.warning("⚠️ Recuerda: Sin síntesis, no hay inteligencia útil.")

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 5"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
# --- MÓDULO 6: COMUNICAR E INTEGRAR ---
        elif modulo_selec == "Módulo 6: Comunicación":
            if not st.session_state['modo_examen']:
                st.header("📢 Material: Comunicar e Integrar")
                
                tab_pasos, tab_ejemplos, tab_seguridad = st.tabs([
                    "🚀 Pasos para la Difusión", 
                    "📝 Casos Prácticos", 
                    "🔐 Seguridad en Entrega"
                ])
                
                with tab_pasos:
                    st.subheader("Procedimiento Estándar de Difusión")
                    st.write("La inteligencia no sirve si no llega a quien debe tomar la decisión en el momento oportuno.")
                    
                    # Diseño de pasos en cascada
                    pasos = [
                        {"n": "1", "t": "Identificar el Receptor", "d": "Nombres, cargo y lugar de recepción pactado con el usuario."},
                        {"n": "2", "t": "Selección del Canal", "d": "Definir si será Virtual (correo cifrado), Físico o Entrega Exclusiva."},
                        {"n": "3", "t": "Mecanismos de Seguridad", "d": "Aplicación de clasificación, encriptación, codificación o embalaje."},
                        {"n": "4", "t": "Difusión del PTI", "d": "Entrega formal al destinatario final según el portafolio de receptores."},
                        {"n": "5", "t": "Registro en Base de Datos", "d": "Registro digital o planilla física (si es entrega exclusiva)."}
                    ]
                    
                    for p in pasos:
                        st.markdown(f"""
                        <div style="background-color: #002147; border-left: 5px solid #D4AF37; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                            <span style="color: #D4AF37; font-weight: bold; font-size: 1.2em;">Paso {p['n']}: {p['t']}</span><br>
                            <span style="color: white; font-size: 0.95em;">{p['d']}</span>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_ejemplos:
                    st.subheader("Ejemplos de Aplicación")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        <div class="ejemplo-box">
                            <h4 style="color: #D4AF37;">Ejemplo A: Canal Virtual</h4>
                            <p style="font-size: 0.9em; color: white;">
                            <b>Escenario:</b> Envío de reporte diario de criminalidad.<br>
                            <b>Acción:</b> Se utiliza el e-mail institucional con un archivo PDF protegido por contraseña y cifrado PGP. <br>
                            <b>Registro:</b> Se guarda el LOG de envío en el sistema centralizado.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="ejemplo-box">
                            <h4 style="color: #D4AF37;">Ejemplo B: Entrega Exclusiva</h4>
                            <p style="font-size: 0.9em; color: white;">
                            <b>Escenario:</b> Orden de captura para blanco de alto valor.<br>
                            <b>Acción:</b> Entrega en sobre sellado con cinta de seguridad directamente al Director de Inteligencia.<br>
                            <b>Registro:</b> Firma obligatoria en la planilla de difusión física.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_seguridad:
                    st.subheader("Medidas de Protección del Producto")
                    
                    st.markdown("""
                    <div style="background-color: #0e1117; padding: 20px; border: 1px dashed #D4AF37; border-radius: 10px;">
                        <ul style="color: white;">
                            <li><b>Clasificación:</b> Marcar claramente como RESERVADO o SECRETO.</li>
                            <li><b>Encriptación:</b> Uso de algoritmos para proteger datos digitales.</li>
                            <li><b>Embalaje:</b> Uso de sobres de seguridad que evidencien manipulación.</li>
                            <li><b>Codificación:</b> Uso de lenguaje convenido para evitar lectura de terceros.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 6"):
                    st.session_state['modo_examen'] = True
                    st.rerun()

    # --- MÓDULO 7: EVALUAR Y RETROALIMENTAR ---
        elif modulo_selec == "Módulo 7: Evaluación":
            if not st.session_state['modo_examen']:
                st.header("🔄 Material: Evaluar y Retroalimentar")
                
                # Definición de Objetivos con diseño destacado
                st.markdown("""
                <div style="background: linear-gradient(90deg, #002147 0%, #003366 100%); padding: 25px; border-radius: 15px; border-right: 5px solid #D4AF37; margin-bottom: 25px;">
                    <h3 style="color: #D4AF37; margin-top: 0;">🎯 Objetivo de la Fase</h3>
                    <p style="color: white; font-size: 1.1em;">
                        Evaluar el impacto del <b>Plan Nacional (PNIP)</b>, <b>Planes Regionales</b> y los productos de inteligencia, 
                        asegurando que los responsables del ciclo identifiquen oportunidades reales de mejoramiento del servicio.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                tab_act, tab_sinai, tab_ejemplos = st.tabs([
                    "⚙️ Actividades Clave", 
                    "📊 Trazabilidad y Análisis", 
                    "📝 Casos de Evaluación"
                ])

                with tab_act:
                    st.subheader("Ruta Crítica de Evaluación")
                    st.write("El proceso se divide en 5 actividades fundamentales:")
                    
                    # Uso de columnas para mostrar el flujo de actividades
                    actividades = [
                        "1. Planificar y programar la evaluación.",
                        "2. Realizar trazabilidad en SINAI.",
                        "3. Seleccionar productos para rastreo.",
                        "4. Trazabilidad de los planes de inteligencia.",
                        "5. Analizar el impacto decisional."
                    ]
                    
                    for act in actividades:
                        st.markdown(f"""
                        <div style="background-color: #0e1117; padding: 12px; border-radius: 8px; border: 1px solid #444; margin-bottom: 8px; color: #D4AF37; font-weight: bold;">
                            {act}
                        </div>
                        """, unsafe_allow_html=True)

                with tab_sinai:
                    st.subheader("Trazabilidad en SINAI")
                    st.info("La trazabilidad no es solo archivo; es el rastreo de acciones y decisiones tomadas basadas en nuestra inteligencia.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4 style="color: #D4AF37;">¿Qué evaluamos?</h4>
                            <ul>
                                <li><b>Pertinencia:</b> ¿El producto respondió al requerimiento?</li>
                                <li><b>Oportunidad:</b> ¿Llegó a tiempo para la operación?</li>
                                <li><b>Exactitud:</b> ¿La información fue veraz?</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4 style="color: #D4AF37;">Impacto Decisional</h4>
                            <p>Se mide si el producto generó una acción concreta: una captura, una desarticulación, o un cambio en la política de seguridad regional.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_ejemplos:
                    st.subheader("Ejemplos de Retroalimentación")
                    
                    st.markdown("""
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div class="ejemplo-box">
                            <h4 style="color: #4CAF50;">✅ Evaluación Positiva</h4>
                            <p style="color: white; font-size: 0.9em;">
                            <b>Insumo:</b> PTI sobre microtráfico en Zona Centro.<br>
                            <b>Decisión:</b> El mando ordena intervención relámpago.<br>
                            <b>Retroalimentación:</b> El producto permitió 5 capturas. Se felicita al equipo de análisis por la precisión geográfica.
                            </p>
                        </div>
                        <div class="ejemplo-box" style="border-left-color: #F44336;">
                            <h4 style="color: #F44336;">⚠️ Oportunidad de Mejora</h4>
                            <p style="color: white; font-size: 0.9em;">
                            <b>Insumo:</b> Informe estratégico trimestral.<br>
                            <b>Hallazgo:</b> La trazabilidad muestra que el informe llegó 15 días después del consejo de seguridad.<br>
                            <b>Acción:</b> Reajustar los tiempos de tratamiento para el próximo ciclo.
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 7"):
                    st.session_state['modo_examen'] = True
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
