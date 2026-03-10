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
    """Verifica si el usuario ya tiene una nota registrada para ese módulo."""
    query = text("SELECT nota FROM calificaciones WHERE funcionario = :f AND modulo = :m")
    with engine.connect() as conn:
        result = conn.execute(query, {"f": nombre, "m": modulo}).fetchone()
    return result[0] if result else None

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
                        <p>1. Es el <b>conocimiento obtenido</b> a través del procesamiento adecuado de la información...</p>
                        <p>3. Su función es la de <b>asesoramiento</b>, proporcionando el conocimiento integrado...</p>
                        <br>
                        <h3>¿Qué es Inteligencia Policial?</h3>
                        <p>Conjunto de procesos mediante los cuales se obtiene, trata, evalúa y analiza la información, para generar conocimiento relacionado con la <b>seguridad y convivencia ciudadana</b>...</p>
                        <br>
                        <h3>Inteligencia según su nivel</h3>
                        <p><b>ESTRÁTEGICA | OPERACIONAL | TÁCTICA</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                nota_previa = verificar_intento(st.session_state['agente_nombre'], "Módulo 1", engine)
                if nota_previa is None:
                    if st.button("🚀 INICIAR EXAMEN M1"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else:
                    st.warning(f"Ya has completado este módulo. Calificación: {nota_previa}%")
            else:
                st.header("📝 Evaluación: Módulo 1")
                with st.form("exam_m1"):
                    q1 = st.radio("1. La función de la inteligencia es:", ["Ejecución táctica", "Asesoramiento para reducir incertidumbre", "Sanción administrativa"])
                    q2 = st.radio("2. Nivel de inteligencia para la formulación de planes y políticas nacionales:", ["Táctica", "Operacional", "Estratégica"])
                    q3 = st.radio("3. ¿A qué nivel corresponde el apoyo directo a jefes de operación en áreas específicas?", ["Operacional", "Estratégica", "Científica"])
                    if st.form_submit_button("FINALIZAR M1"):
                        res = [q1=="Asesoramiento para reducir incertidumbre", q2=="Estratégica", q3=="Operacional"]
                        nota = (sum(res)/3)*100
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 1"})
                            conn.commit()
                        st.session_state['modo_examen'] = False
                        st.rerun()

        # --- MÓDULO 2 ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material: Ciclo de Inteligencia")
                with st.expander("Ver Contenido Completo Módulo 2", expanded=True):
                    st.markdown("""
                    <div class="lectura-box">
                        <h3>Los 5 Pasos:</h3>
                        <ul>
                            <li><b>1. Recolectar</b> | <b>2. Tratar</b> | <b>3. Analizar</b> | <b>4. Comunicar</b> | <b>5. Evaluar</b></li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                
                nota_previa = verificar_intento(st.session_state['agente_nombre'], "Módulo 2", engine)
                if nota_previa is None:
                    if st.button("🚀 INICIAR EXAMEN M2"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else:
                    st.warning(f"Ya has completado este módulo. Calificación: {nota_previa}%")
            else:
                st.header("📝 Evaluación: Módulo 2")
                with st.form("exam_m2"):
                    q1 = st.radio("1. Paso donde se transforma la información en inteligencia mediante análisis:", ["Recolectar", "Analizar", "Tratar"])
                    q2 = st.radio("2. ¿Qué paso asegura la calidad mediante la revisión constante?", ["Comunicar", "Evaluar y Retroalimentar", "Tratar"])
                    q3 = st.radio("3. ¿Cuál es el primer paso operativo del ciclo?", ["Difundir", "Analizar", "Recolectar"])
                    if st.form_submit_button("FINALIZAR M2"):
                        res = [q1=="Analizar", q2=="Evaluar y Retroalimentar", q3=="Recolectar"]
                        nota = (sum(res)/3)*100
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 2"})
                            conn.commit()
                        st.session_state['modo_examen'] = False
                        st.rerun()

        # --- MÓDULO 3 ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state['modo_examen']:
                st.header("📖 Material Completo: Recolección de Información")
                t1, t2, t3, t4 = st.tabs(["📌 Fundamentos", "🕵️ Operaciones", "👥 Fuentes", "🎤 Entrevista"])
                with t1:
                    st.markdown('<div class="lectura-box"><h3>Recolección y PHVA</h3><p>PLANEAR, HACER, VERIFICAR, ACTUAR.</p></div>', unsafe_allow_html=True)
                    

[Image of the PDCA cycle diagram: Plan, Do, Check, Act]

                with t2:
                    st.write("**Vigilancia:** Observación discreta. **Sonsacamiento:** Diálogo sin que la fuente lo note.")
                with t3:
                    st.write("**Fuentes:** Abiertas, Cerradas, Humanas, Técnicas.")
                with t4:
                    st.write("**Tipos a EVITAR:** El sordo, el metralleta, el estrella.")

                nota_previa = verificar_intento(st.session_state['agente_nombre'], "Módulo 3", engine)
                if nota_previa is None:
                    if st.button("🚀 INICIAR EXAMEN M3"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else:
                    st.warning(f"Ya has completado este módulo. Calificación: {nota_previa}%")
            else:
                st.header("📝 Evaluación: Módulo 3")
                with st.form("exam_m3"):
                    c1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Vigilancia"])
                    c2 = st.radio("2. En PHVA, ¿qué implica HACER?", ["Planificar recursos", "Búsqueda de información y elaboración de productos", "Autoevaluación"])
                    c3 = st.radio("3. Diferencia entre Infiltración y Penetración:", ["Ninguna", "Infiltración mete al agente; Penetración usa a alguien de adentro", "Infiltración es abierta"])
                    c4 = st.radio("4. Unidad básica de información:", ["El mensaje", "El dato", "El informe"])
                    c5 = st.radio("5. ¿Qué busca el Reconocimiento?", ["Vigilar", "Concretar datos de propietarios, vehículos y seguridad", "Sonsacar"])
                    c6 = st.radio("6. En PHVA, VERIFICAR es:", ["Ejecutar controles", "Realizar autoevaluación de control y gestión", "Planear"])
                    c7 = st.radio("7. Entrevistador que olvida escuchar por su cuestionario:", ["Metralleta", "Sordo", "Estrella"])
                    c8 = st.radio("8. Primer paso en Administración de Fuentes Humanas:", ["Registro", "Entrenamiento", "Exploración (Búsqueda)"])
                    c9 = st.radio("9. Fin de las operaciones Estructurales:", ["Flagrancias", "Desarticulación de estructuras y ruptura de cadena criminal", "Prevención"])
                    c10 = st.radio("10. Etapa de entrevista de primer contacto:", ["Planeación", "Desarrollo", "Informe"])

                    if st.form_submit_button("FINALIZAR M3"):
                        res = [c1=="Diálogo donde la fuente no debe percatarse de la explotación", c2=="Búsqueda de información y elaboración de productos", c3=="Infiltración mete al agente; Penetración usa a alguien de adentro", c4=="El dato", c5=="Concretar datos de propietarios, vehículos y seguridad", c6=="Realizar autoevaluación de control y gestión", c7=="Sordo", c8=="Exploración (Búsqueda)", c9=="Desarticulación de estructuras y ruptura de cadena criminal", c10=="Desarrollo"]
                        nota = (sum(res) / 10) * 100
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": "Módulo 3"})
                            conn.commit()
                        st.session_state['modo_examen'] = False
                        st.rerun()

    # --- SECCIONES EXTRA ---
    elif seccion == "📊 Mi Progreso":
        st.title("Historial de Calificaciones")
        try:
            df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), engine, params={"n": st.session_state['agente_nombre']})
            st.dataframe(df, use_container_width=True)
        except: st.info("No hay registros para este usuario.")

    elif seccion == "📈 Dashboard General":
        if st.session_state['es_admin']:
            st.title("🛡️ Panel Administrativo")
            df_all = pd.read_sql(text("SELECT funcionario, modulo, nota, fecha FROM calificaciones"), engine)
            st.subheader("🔍 Buscar por Estudiante")
            estudiantes = sorted(df_all['funcionario'].unique())
            seleccion = st.selectbox("Seleccione funcionario:", ["-- Ver Todos --"] + list(estudiantes))
            if seleccion != "-- Ver Todos --":
                df_f = df_all[df_all['funcionario'] == seleccion]
                st.table(df_f)
                st.metric("Promedio Estudiante", f"{df_f['nota'].mean():.2f}%")
            else:
                st.dataframe(df_all, use_container_width=True)
            st.divider()
            st.bar_chart(df_all.groupby('modulo')['nota'].mean())
        else:
            st.warning("Acceso restringido.")
