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
    .submodulo-box { background-color: #003366; padding: 15px; border-radius: 8px; border: 1px solid #D4AF37; margin-bottom: 15px; }
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
        st.write(f"Bienvenido al sistema, {st.session_state['agente_nombre']}.")
        st.info("Utilice el menú lateral para acceder a los 3 módulos disponibles.")

    # --- MÓDULOS ---
    elif seccion == "📚 Módulos":
        modulo = st.selectbox("Seleccione Módulo:", ["Módulo 1", "Módulo 2", "Módulo 3"])
        
        # --- MÓDULO 1 (RESTAURADO) ---
        if modulo == "Módulo 1":
            st.title("Módulo 1: Conceptualización")
            if not st.session_state['modo_examen']:
                st.markdown("""<div class='lectura-box'><h3>Definición de Inteligencia</h3><p>Conocimiento obtenido a través del procesamiento adecuado de la información...</p></div>""", unsafe_allow_html=True)
                if st.button("EXAMEN M1"): st.session_state['modo_examen'] = True; st.rerun()
            else:
                with st.form("m1"):
                    q1 = st.radio("Función principal:", ["Asesoramiento", "Fuerza"])
                    if st.form_submit_button("GUARDAR"): st.success("Nota guardada"); st.session_state['modo_examen']=False

        # --- MÓDULO 2 (RESTAURADO) ---
        elif modulo == "Módulo 2":
            st.title("Módulo 2: Ciclo de Inteligencia")
            if not st.session_state['modo_examen']:
                st.markdown("""<div class='lectura-box'><h3>Los 5 Pasos</h3><p>1. Recolectar, 2. Tratar, 3. Analizar, 4. Comunicar, 5. Evaluar.</p></div>""", unsafe_allow_html=True)
                if st.button("EXAMEN M2"): st.session_state['modo_examen'] = True; st.rerun()
            else:
                with st.form("m2"):
                    q1 = st.radio("¿Cuántos pasos?", ["3", "5"])
                    if st.form_submit_button("GUARDAR"): st.success("Nota guardada"); st.session_state['modo_examen']=False

        # --- MÓDULO 3: RECOLECCIÓN (NUEVO COMPLETO) ---
        elif modulo == "Módulo 3":
            st.title("Módulo 3: Recolección de Información")
            
            if not st.session_state['modo_examen']:
                tab1, tab2, tab3, tab4 = st.tabs(["📖 Fundamentos", "🔄 Proceso PHVA", "🕵️ Operaciones", "👥 Fuentes y Humana"])
                
                with tab1:
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>Definición</h3>
                        <p>Consiste en juntar aquellos datos o información relevante para el objetivo de nuestra investigación, que generalmente se encuentra dispersa.</p>
                        <ul>
                            <li>Definir requerimientos.</li>
                            <li>Identificar fuentes potenciales.</li>
                            <li>Diseñar estrategias de recolección.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tab2:
                    st.subheader("Ciclo PHVA en Recolección")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**PLANEAR:** Establecer objetivos, riesgos y recursos.")
                        st.markdown("**HACER:** Búsqueda, desarrollo de actividades y registro de productos.")
                    with col2:
                        st.markdown("**VERIFICAR:** Seguimiento, medición y autoevaluación.")
                        st.markdown("**ACTUAR:** Acciones correctivas y mejora continua.")

                with tab3:
                    st.subheader("Submódulo: Operaciones de Inteligencia")
                    st.write("Actividades orientadas a la obtención de información privilegiada.")
                    
                    with st.expander("🔍 Básicas: Reconocimiento, Verificación y Vigilancia"):
                        st.write("**Reconocimiento:** Concretar y ampliar datos previos (vías, seguridad, entorno).")
                        st.write("**Verificación:** Establecer veracidad o desvirtuar información.")
                        st.write("**Vigilancia:** Observación continua y discreta (rutinas).")
                        st.write("**Seguimiento:** Control sobre objetivos en movimiento (a pie o vehículo).")
                        st.write("**Sonsacamiento:** Obtención de info mediante diálogo sin que la fuente lo note.")
                    
                    with st.expander("⚡ Especializadas: Infiltración y Penetración"):
                        st.write("**Infiltración:** Ubicar agentes dentro de la organización.")
                        st.write("**Penetración:** Lograr colaboración de alguien que ya está dentro.")

                with tab4:
                    st.subheader("Fuentes y Entrevista")
                    st.write("**Fuentes:** Abiertas (Públicas), Cerradas (Especializadas/Técnicas) y Humanas.")
                    st.info("Tipos de Entrevistador a evitar: El estrella, El estrellado, El improvisado, El sordo, El enredado y El metralleta.")

                if st.button("🚀 INICIAR EVALUACIÓN MÓDULO 3"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            
            else:
                st.header("📝 Examen Técnico: Recolección")
                with st.form("exam_m3"):
                    p1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no percibe la explotación", "Tortura"])
                    p2 = st.radio("2. En PHVA, ¿qué significa 'Hacer'?", ["Planear recursos", "Búsqueda y elaboración de productos", "Mejora continua"])
                    p3 = st.radio("3. Diferencia entre Infiltración y Penetración:", ["No hay diferencia", "Infiltración mete a alguien; Penetración usa a alguien de adentro", "Infiltración es técnica; Penetración es humana"])
                    p4 = st.radio("4. ¿Qué busca el Reconocimiento?", ["Solo fotos", "Profundizar en datos de propietarios, vehículos y entorno", "Sonsacar"])
                    p5 = st.radio("5. ¿Cuál es un tipo de entrevistador deficiente?", ["El metralleta", "El analista", "El recolector"])
                    
                    if st.form_submit_button("ENVIAR RESULTADOS M3"):
                        r = [p1=="Diálogo donde la fuente no percibe la explotación", p2=="Búsqueda y elaboración de productos", p3=="Infiltración mete a alguien; Penetración usa a alguien de adentro", p4=="Profundizar en datos de propietarios, vehículos y entorno", p5=="El metralleta"]
                        nota = (sum(r)/5)*100
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 3"})
                            conn.commit()
                        st.success(f"Nota: {nota}%"); st.session_state['modo_examen']=False; st.rerun()

    # --- PROGRESO ---
    elif seccion == "📊 Mi Progreso":
        st.title("Historial de Notas")
        df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), engine, params={"n": st.session_state['agente_nombre']})
        st.table(df)
