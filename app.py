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
        st.info("Bienvenido. Seleccione '📚 Módulos' para acceder al contenido técnico.")

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
                    <p>Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la <b>seguridad y convivencia ciudadana</b>...</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 INICIAR EVALUACIÓN M1"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m1"):
                    p1 = st.radio("Función de la inteligencia:", ["Asesoramiento", "Fuerza"])
                    if st.form_submit_button("Guardar Nota M1"): st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 2 ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Ciclo de Inteligencia")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición y Pasos</h3>
                    <p>Serie de <b>cinco pasos</b> orientados a la generación de conocimiento estratégico útil, verdadero y ajustado a los requerimientos del decisor.</p>
                    <ul><li>Recolectar, Tratar, Analizar, Comunicar e Integrar, Evaluar y Retroalimentar.</li></ul>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 INICIAR EVALUACIÓN M2"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("ex_m2"):
                    p1 = st.radio("¿Cuántos pasos tiene el ciclo?", ["5 pasos", "3 pasos"])
                    if st.form_submit_button("Guardar Nota M2"): st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 3: RECOLECCIÓN (LECTURA COMPLETA Y EXAMEN DE 10 PREGUNTAS) ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material Completo: Recolección de Información")
                
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
                    st.write("**PLANEAR:** Establecer objetivos y procesos. Planificación, riesgos y recursos.")
                    st.write("**HACER:** Búsqueda, desarrollo de actividades, elaboración y suministro de productos, controles de seguridad.")
                    st.write("**VERIFICAR:** Seguimiento y medición, autoevaluación de control y gestión.")
                    st.write("**ACTUAR:** Ajustar y mejorar, acciones correctivas o preventivas.")

                with st.expander("2. ¿Qué es Información y Datos?"):
                    st.write("**Información:** Conjunto de datos integrados y ordenados que sirven para construir un mensaje. Materia prima para resolver problemas.")
                    st.write("**Dato:** Unidad básica que comprende la información.")
                    st.subheader("Fuentes de Información")
                    st.write("* Abiertas (Públicas), Cerradas Especializadas, Cerradas Humanas y Técnicas.")

                with st.expander("3. Operaciones de Inteligencia"):
                    st.markdown("""
                    **Operaciones Básicas:**
                    * **Reconocimiento:** Concretar datos de inmuebles, personas, vehículos y seguridad.
                    * **Verificación:** Establecer veracidad o desvirtuar información.
                    * **Vigilancia:** Observación continua y discreta para establecer rutinas.
                    * **Seguimiento:** Control sobre objetivos en movimiento (A pie / Vehículo).
                    * **Sonsacamiento:** Diálogo donde la fuente no percibe la intención del agente.
                    
                    **Operaciones Especializadas:**
                    * **Infiltración:** Ubicar agentes dentro de una organización.
                    * **Penetración:** Obtener colaboración de alguien que ya está dentro.
                    """)

                with st.expander("4. Administración de Fuentes Humanas y Entrevista"):
                    st.write("**Fases Admón:** Exploración -> Aproximación -> Registro -> Entrenamiento.")
                    st.subheader("Tipos de Entrevistador (A EVITAR)")
                    st.write("- **El estrella:** Se siente superior. | **El sordo:** Olvida escuchar.")
                    st.write("- **El metralleta:** Bombardea preguntas. | **El enredado:** Lenguaje complejo.")
                    st.write("- **El improvisado:** No prepara nada. | **El estrellado:** Tímido.")

                if st.button("🚀 INICIAR EXAMEN DE RECOLECCIÓN (10 PREGUNTAS)"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.header("📝 Evaluación: Módulo 3 (Recolección)")
                with st.form("ex_m3_final"):
                    c1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Tortura psicológica"])
                    c2 = st.radio("2. En el ciclo PHVA, ¿qué implica PLANEAR?", ["Búsqueda de información", "Establecer objetivos, riesgos y recursos", "Acciones correctivas"])
                    c3 = st.radio("3. ¿Cuál es la diferencia entre Infiltración y Penetración?", ["No hay diferencia", "Infiltración mete al agente; Penetración usa a alguien que ya está dentro", "Infiltración es técnica; Penetración es humana"])
                    c4 = st.radio("4. ¿Cuál es la unidad básica que comprende la información?", ["El mensaje", "El dato", "El informe"])
                    c5 = st.radio("5. ¿Qué busca el Reconocimiento específicamente?", ["Solo vigilar", "Concretar datos de propietarios, vehículos, seguridad y entorno", "Sonsacar a la fuente"])
                    c6 = st.radio("6. En PHVA, ¿qué acción corresponde a VERIFICAR?", ["Ejecutar controles", "Realizar autoevaluación de control y gestión", "Planificar recursos"])
                    c7 = st.radio("7. Tipo de entrevistador que habla más que la fuente y se siente superior:", ["El metralleta", "El estrella", "El sordo"])
                    c8 = st.radio("8. ¿Cuál es el primer paso en la Administración de Fuentes Humanas?", ["Registro", "Entrenamiento", "Exploración (Búsqueda)"])
                    c9 = st.radio("9. Las operaciones Estructurales tienen como fin:", ["Solo flagrancias", "Desarticulación de estructuras y ruptura de cadena criminal", "Fines comunitarios"])
                    c10 = st.radio("10. ¿Qué etapa de la entrevista busca mantener armonía sin perder el control?", ["Planeación", "Desarrollo", "Informe"])

                    if st.form_submit_button("FINALIZAR Y GUARDAR CALIFICACIÓN"):
                        res = [c1=="Diálogo donde la fuente no debe percatarse de la explotación", c2=="Establecer objetivos, riesgos y recursos", c3=="Infiltración mete al agente; Penetración usa a alguien que ya está dentro", c4=="El dato", c5=="Concretar datos de propietarios, vehículos, seguridad y entorno", c6=="Realizar autoevaluación de control y gestión", c7=="El estrella", c8=="Exploración (Búsqueda)", c9=="Desarticulación de estructuras y ruptura de cadena criminal", c10=="Desarrollo"]
                        nota = (sum(res) / 10) * 100
                        try:
                            with engine.connect() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 3: Recolección"})
                                conn.commit()
                            st.success(f"Evaluación finalizada. Su nota es: {nota}%")
                            st.session_state['modo_examen'] = False
                        except Exception as e: st.error(f"Error al guardar: {e}")

    elif seccion == "📊 Mi Progreso":
        st.title("Historial Personal")
        df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), engine, params={"n": st.session_state['agente_nombre']})
        st.dataframe(df, use_container_width=True)
