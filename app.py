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
    .submodulo-box { background-color: #003366; padding: 15px; border-radius: 8px; border: 1px solid #D4AF37; margin-bottom: 15px; color: white; }
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
        st.info("Bienvenido. Seleccione '📚 Módulos' para acceder al contenido técnico completo.")

    elif seccion == "📚 Módulos":
        modulo = st.selectbox("Seleccione Módulo de Estudio:", ["Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", "Módulo 3: Recolección"])
        
        # --- MÓDULO 1 ---
        if modulo == "Módulo 1: Conceptualización":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Conceptualización de Inteligencia")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición de Inteligencia</h3>
                    <p>1. Conocimiento obtenido a través del procesamiento adecuado de la información...</p>
                    <p>2. Actividad multi y transdisciplinaria...</p>
                    <p>3. Su función es la de asesoramiento reduciendo incertidumbres.</p>
                </div>
                <div class="lectura-box">
                    <h3>Inteligencia según su nivel</h3>
                    <p><b>Estratégica:</b> Formulación de planes nacionales.</p>
                    <p><b>Operacional:</b> Planeamiento dentro de un área específica.</p>
                    <p><b>Táctica:</b> Conducción de equipos y capacidades inmediatas.</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Iniciar Evaluación M1"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("exam_m1"):
                    p1 = st.radio("Función de la inteligencia:", ["Asesoramiento", "Fuerza"])
                    if st.form_submit_button("Guardar Nota M1"): st.success("Guardado"); st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 2 ---
        elif modulo == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Ciclo de Inteligencia")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición</h3>
                    <p>Serie de cinco pasos para la generación de conocimiento estratégico ajustado a requerimientos del decisor.</p>
                    <p><b>Pasos:</b> Recolectar, Tratar, Analizar, Comunicar e Integrar, Evaluar y Retroalimentar.</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Iniciar Evaluación M2"): st.session_state['modo_examen']=True; st.rerun()
            else:
                with st.form("exam_m2"):
                    p1 = st.radio("¿Cuántos pasos tiene el ciclo?", ["5 pasos", "3 pasos"])
                    if st.form_submit_button("Guardar Nota M2"): st.success("Guardado"); st.session_state['modo_examen']=False; st.rerun()

        # --- MÓDULO 3 ---
        elif modulo == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material Extendido: Recolección de Información")
                
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["📌 Fundamentos y PHVA", "🕵️ Operaciones Básicas", "⚡ Operaciones Especializadas", "👥 Fuentes y Fuentes Humanas", "🎤 La Entrevista"])
                
                with tab1:
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>¿Qué es Recolección?</h3>
                        <p>Consiste en juntar datos relevantes que están dispersos en el entorno mediante técnicas precisas.</p>
                    </div>
                    <h4>Recolección bajo el Ciclo PHVA</h4>
                    <p><b>PLANEAR:</b> Establecer objetivos, administrar riesgos y planificar recursos.</p>
                    <p><b>HACER:</b> Búsqueda de información, desarrollo de actividades y registro de productos.</p>
                    <p><b>VERIFICAR:</b> Seguimiento y autoevaluación de control y gestión.</p>
                    <p><b>ACTUAR:</b> Implementar acciones correctivas y de mejora continua.</p>
                    """, unsafe_allow_html=True)
                    

                with tab2:
                    st.subheader("Submódulo: Operaciones Básicas")
                    st.markdown("""
                    <div class="submodulo-box">
                        <b>Reconocimiento:</b> Va más allá de la descripción; busca datos de propietarios, vehículos, seguridad y vías de acceso.<br><br>
                        <b>Verificación:</b> Pretende establecer la veracidad o desvirtuar una información (bases de datos, llamadas, etc).<br><br>
                        <b>Vigilancia:</b> Observación continua y discreta para establecer rutinas.<br><br>
                        <b>Seguimiento:</b> Control sobre personas o elementos en movimiento (A pie o en vehículo).<br><br>
                        <b>Sonsacamiento:</b> Diálogo donde la fuente no debe percatarse de la explotación ni de la intención.
                    </div>
                    """, unsafe_allow_html=True)

                with tab3:
                    st.subheader("Submódulo: Operaciones Especializadas")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Infiltración:**")
                        st.info("Ubicar agentes de inteligencia dentro de una organización mediante una cobertura.")
                    with col2:
                        st.write("**Penetración:**")
                        st.info("Lograr la colaboración de alguien que ya pertenece a la organización objetivo.")
                    
                    st.write("---")
                    st.write("**Niveles de Operaciones:** Estratégicas (objetivos alto valor), Estructurales (desarticulación), Impacto (flagrancias) y Comunitaria.")

                with tab4:
                    st.subheader("Administración de Fuentes Humanas")
                    st.write("Proceso de ORIENTAR, DIRIGIR y CONTROLAR la fuente.")
                    st.markdown("""
                    1. **Exploración:** Búsqueda y evaluación inicial.
                    2. **Aproximación:** Establecimiento del contacto (Entrevista/Sonsacamiento).
                    3. **Registro:** Ingreso al sistema de administración.
                    4. **Entrenamiento:** Instruir y preparar a la fuente.
                    """)

                with tab5:
                    st.subheader("La Entrevista de Inteligencia")
                    st.warning("⚠️ **Evite ser estos tipos de entrevistador:**")
                    st.write("- **El Estrella:** Se siente superior y habla más que la fuente.")
                    st.write("- **El Sordo:** Se preocupa tanto por su cuestionario que no escucha.")
                    st.write("- **El Metralleta:** No da tiempo de responder entre preguntas.")
                    st.write("- **El Enredado:** Usa términos complejos y da muchas vueltas.")
                    st.write("---")
                    st.write("**Etapas:** Planeación -> Desarrollo -> Terminación -> Informe.")

                if st.button("🚀 INICIAR EVALUACIÓN MÓDULO 3"):
                    st.session_state['modo_examen'] = True
                    st.rerun()

            else:
                st.header("📝 Evaluación Técnica M3")
                with st.form("exam_m3"):
                    p1 = st.radio("Diferencia entre Infiltración y Penetración:", ["Infiltración mete al agente; Penetración usa a alguien de adentro", "Son lo mismo"])
                    p2 = st.radio("En PHVA, ¿qué es 'Actuar'?", ["Planificar recursos", "Implementar acciones correctivas y de mejora"])
                    p3 = st.radio("¿Qué busca el Sonsacamiento?", ["Que la fuente no se percate de la explotación", "Hacer un interrogatorio directo"])
                    p4 = st.radio("Nivel de operación que busca desarticular estructuras:", ["Estructural", "Impacto"])
                    p5 = st.radio("Entrevistador que no escucha a la fuente por mirar su cuestionario:", ["El sordo", "El estrella"])
                    
                    if st.form_submit_button("Finalizar y Guardar M3"):
                        nota = (sum([p1=="Infiltración mete al agente; Penetración usa a alguien de adentro", p2=="Implementar acciones correctivas y de mejora", p3=="Que la fuente no se percate de la explotación", p4=="Estructural", p5=="El sordo"])/5)*100
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 3"})
                            conn.commit()
                        st.success(f"Nota: {nota}%"); st.session_state['modo_examen']=False; st.rerun()

    elif seccion == "📊 Mi Progreso":
        st.title("Historial Personal")
        df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC"), engine, params={"n": st.session_state['agente_nombre']})
        st.dataframe(df, use_container_width=True)
