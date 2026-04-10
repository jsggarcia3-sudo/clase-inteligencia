import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from datetime import datetime

# ============================================================
# 1. CONFIGURACIÓN INICIAL (una sola vez, antes de todo)
# ============================================================
st.set_page_config(
    page_title="Plataforma Educativa DIPOL",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 2. SESIÓN — inicializar ANTES de cualquier uso
# ============================================================
DEFAULTS = {
    "autenticado": False,
    "agente_nombre": "",
    "es_admin": False,
    "modo_examen": False,
    "modulo_activo": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# 3. CONEXIÓN A BASE DE DATOS
# ============================================================
@st.cache_resource
def get_engine():
    try:
        db_s = st.secrets["connections"]["postgresql"]
        pw = quote_plus(db_s["password"])
        url = f"postgresql://{db_s['username']}:{pw}@{db_s['host']}:{db_s['port']}/{db_s['database']}"
        return create_engine(url)
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

engine = get_engine()

# ============================================================
# 4. FUNCIONES DE DATOS
# ============================================================
@st.cache_data(ttl=60)
def cargar_datos_agente(nombre_agente):
    with engine.connect() as conn:
        q = text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC")
        return pd.read_sql(q, conn, params={"n": nombre_agente})

@st.cache_data(ttl=60)
def cargar_todo_admin():
    with engine.connect() as conn:
        q = text("SELECT funcionario, modulo, nota, fecha FROM calificaciones")
        return pd.read_sql(q, conn)

def verificar_intento(nombre, modulo):
    """Revisa si el agente ya tiene nota en un módulo. Devuelve la nota o None."""
    try:
        with engine.connect() as conn:
            q = text("SELECT nota FROM calificaciones WHERE funcionario = :f AND modulo = :m")
            row = conn.execute(q, {"f": nombre, "m": modulo}).fetchone()
        return row[0] if row else None
    except Exception:
        return None

def guardar_nota(nombre, modulo, nota):
    """Inserta la calificación en la BD. Devuelve True si tuvo éxito."""
    try:
        with engine.begin() as conn:
            q = text("INSERT INTO calificaciones (funcionario, modulo, nota, fecha) VALUES (:f, :m, :n, :d)")
            conn.execute(q, {"f": nombre, "m": modulo, "n": nota, "d": datetime.now()})
        return True
    except Exception as e:
        st.error(f"Error al guardar nota: {e}")
        return False

def calcular_nota(respuestas_correctas, total):
    return (sum(respuestas_correctas) / total) * 100

# ============================================================
# 5. CSS GLOBAL (responsive + estilos compartidos)
# ============================================================
st.markdown("""
<style>
/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .block-container { padding: 1rem 0.5rem !important; }
    .stButton > button { font-size: 0.85rem !important; padding: 10px 5px !important; }
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1rem !important; }
    [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
    [data-testid="stSidebar"] { width: 80vw !important; }
    .watermark { font-size: 40px !important; }
    div[style*="min-height: 220px"] { min-height: auto !important; padding: 15px !important; }
    [data-testid="stTabs"] { overflow-x: auto !important; }
    .stForm { padding: 15px !important; }
    [data-testid="stDataFrame"] { overflow-x: auto !important; }
}
@media (min-width: 769px) and (max-width: 1024px) {
    .block-container { padding: 1.5rem 1rem !important; }
    h1 { font-size: 1.8rem !important; }
}

/* ===== TARJETAS Y COMPONENTES ===== */
.lectura-box {
    background-color: #002b55; padding: 20px; border-radius: 10px;
    border-left: 5px solid #D4AF37; margin-bottom: 20px;
}
.lectura-box h3, .lectura-box h4 { color: #D4AF37; margin-top: 0; }
.lectura-box p, .lectura-box li { color: white; }

.ejemplo-box {
    background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 15px;
}
.ejemplo-box h3, .ejemplo-box h4 { margin-top: 0; }
.ejemplo-box p, .ejemplo-box li { color: white; font-size: 0.9em; }

.card-dark {
    background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 15px;
}
.card-dark p { color: #ecf0f1; font-size: 0.9em; }

/* ===== MARCA DE AGUA ===== */
.watermark-container {
    position: fixed; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999; pointer-events: none;
}
.watermark-inline {
    color: rgba(0, 240, 255, 0.15) !important;
    font-size: 16px; font-family: monospace;
    letter-spacing: 1px;
    transform: rotate(-30deg);
    margin: 30px; padding: 10px;
}

/* ===== MÉTRICAS ADMIN ===== */
.metric-card {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid #30363d; border-top: 4px solid #D4AF37;
    border-radius: 15px; padding: 25px 10px; text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
}
.metric-title { color: #8b949e; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px; }
.metric-value { color: #D4AF37; font-size: 3rem; font-weight: 900; margin: 0; }

/* ===== TABLA 4x4 ===== */
.t-4x4 { width: 100%; border-collapse: collapse; color: white; }
.t-4x4 th { background-color: #D4AF37; color: #000; padding: 8px; border: 1px solid #444; }
.t-4x4 td { padding: 8px; border: 1px solid #444; background-color: #002b55; font-size: 0.85em; }
.cod-cell { text-align: center; font-weight: bold; background-color: #003366 !important; width: 40px; }
.perc-100 { background-color: #2e7d32 !important; text-align: center; font-weight: bold; }
.perc-75  { background-color: #fbc02d !important; text-align: center; font-weight: bold; color: black; }
.perc-50  { background-color: #ef6c00 !important; text-align: center; font-weight: bold; }
.perc-25  { background-color: #c62828 !important; text-align: center; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


# ############################################################
#                     PANTALLA DE LOGIN
# ############################################################
def pantalla_login():
    # CSS específico del login
    st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1350&q=80");
        background-size: cover; background-position: center;
    }
    [data-testid="stForm"] {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
        border-radius: 20px; border: 1px solid rgba(255,255,255,0.1) !important;
        padding: 40px; box-shadow: 0 8px 32px rgba(0,0,0,0.37);
    }
    .stTextInput input {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important; border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #00C9FF, #92FE9D);
        color: #000 !important; font-weight: bold; border: none; border-radius: 10px;
        padding: 10px 20px; transition: 0.3s;
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 0 20px rgba(0,201,255,0.6); }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:white; font-weight:800; letter-spacing:2px; text-shadow:0 0 10px rgba(0,201,255,0.5);'>ACCESO AL SISTEMA</h1>", unsafe_allow_html=True)

    _left, center, _right = st.columns([0.5, 2, 0.5])
    with center:
        with st.form("login_form"):
            nombre = st.text_input("Nombre Completo", placeholder="Ej: Noel Viera")
            usuario = st.text_input("Usuario", placeholder="Escriba 'User' o su usuario")
            clave = st.text_input("Contraseña", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("INGRESAR AL CURSO", use_container_width=True)

            if submitted:
                # Admin
                if usuario == "Jsantos" and clave == "Inteligencia2026":
                    st.session_state.update(autenticado=True, es_admin=True, agente_nombre=nombre or "Admin")
                    st.rerun()
                # Estudiante
                elif nombre and usuario == "User" and clave == "ESTUDIANTE2026":
                    st.session_state.update(autenticado=True, es_admin=False, agente_nombre=nombre)
                    st.rerun()
                else:
                    st.error("Credenciales inválidas o campos vacíos.")

    st.caption("Sistema de Inteligencia v2.6 | Conexión Encriptada")


# ############################################################
#            CONTENIDO Y EXÁMENES DE CADA MÓDULO
# ############################################################

# ---- Helpers para evitar repetir el patrón "mostrar material → botón examen → formulario" ----

def bloque_examen(modulo_label, render_material_fn, render_exam_fn):
    """
    Patrón reutilizable:
    - Si no está en modo examen → muestra material + botón iniciar
    - Si está en modo examen → muestra formulario
    """
    if not st.session_state["modo_examen"]:
        render_material_fn()
        st.divider()
        nota_previa = verificar_intento(st.session_state["agente_nombre"], modulo_label)
        if nota_previa is None:
            if st.button(f"🚀 INICIAR EXAMEN — {modulo_label}", key=f"btn_exam_{modulo_label}"):
                st.session_state["modo_examen"] = True
                st.rerun()
        else:
            st.success(f"✅ Módulo completado. Calificación: {nota_previa}%")
    else:
        render_exam_fn(modulo_label)


def finalizar_examen(modulo_label, respuestas_bool):
    """Calcula nota, guarda y sale del modo examen."""
    nota = calcular_nota(respuestas_bool, len(respuestas_bool))
    if guardar_nota(st.session_state["agente_nombre"], modulo_label, nota):
        if nota >= 70:
            st.balloons()
            st.success(f"✅ Nota registrada: {nota:.0f}%")
        else:
            st.warning(f"⚠️ Nota: {nota:.0f}%. Se recomienda repasar el material.")
    else:
        st.info(f"Nota calculada: {nota:.0f}% (no se pudo guardar en BD)")
    st.session_state["modo_examen"] = False
    st.rerun()


# ====================== MÓDULO 1 ======================
def material_m1():
    st.header("📖 Material: Conceptualización de Inteligencia")
    st.markdown("""
    <div class="lectura-box">
        <h3>¿Qué es Inteligencia?</h3>
        <p>Es el <b>conocimiento obtenido</b> mediante el procesamiento de información para reducir la incertidumbre en la toma de decisiones.</p>
        <ul>
            <li>Es una actividad <b>multi y transdisciplinaria</b>.</li>
            <li>Su función principal es el <b>asesoramiento</b> técnico.</li>
            <li>Se diferencia del intelecto por enfocarse en <b>habilidades y aptitudes</b> ante situaciones concretas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🛡️ Inteligencia Policial")
    st.info("Conjunto de procesos para generar conocimiento relacionado con la **seguridad y convivencia ciudadana**, contribuyendo al diseño de estrategias institucionales y operaciones de la misión policial.")

    st.markdown("### 📊 Niveles de Inteligencia")
    c1, c2, c3 = st.columns(3)
    niveles = [
        ("Estratégica", "#3498db", "Utilizada por líderes políticos y policiales para formular <b>planes y políticas</b> nacionales a largo plazo."),
        ("Operacional", "#f1c40f", "Planeamiento de operaciones en <b>áreas específicas</b>. Se concentra en localización y análisis de objetivos."),
        ("Táctica", "#2ecc71", "Requerida para la <b>conducción de equipos</b> en el terreno durante operaciones inmediatas."),
    ]
    for col, (titulo, color, desc) in zip([c1, c2, c3], niveles):
        with col:
            st.markdown(f"""
            <div class="card-dark" style="border-top: 4px solid {color}; height: 260px;">
                <h4 style="color: {color}; text-align: center;">{titulo}</h4>
                <p>{desc}</p>
            </div>""", unsafe_allow_html=True)

def examen_m1(modulo_label):
    st.header("📝 Evaluación: Módulo 1")
    with st.form("exam_m1"):
        q1 = st.radio("1. ¿Cuál es la función principal de la inteligencia?",
            ["Asesoramiento para la toma de decisiones", "Realizar capturas físicas", "Publicar noticias"])
        q2 = st.radio("2. La inteligencia se diferencia del intelecto porque hace hincapié en:",
            ["La memoria", "Habilidades y aptitudes para manejar situaciones concretas", "La velocidad de lectura"])
        q3 = st.radio("3. ¿Sobre qué áreas genera conocimiento la Inteligencia Policial?",
            ["Solo temas financieros", "Seguridad y convivencia ciudadana", "Trámites administrativos"])
        q4 = st.radio("4. Nivel de inteligencia que ayuda a formular planes y políticas nacionales:",
            ["Táctica", "Estratégica", "Operacional"])
        q5 = st.radio("5. La inteligencia táctica es requerida para:",
            ["Leyes nacionales", "Conducción de operaciones a nivel de equipos", "Planificar el presupuesto anual"])
        if st.form_submit_button("FINALIZAR EXAMEN"):
            finalizar_examen(modulo_label, [
                q1 == "Asesoramiento para la toma de decisiones",
                q2 == "Habilidades y aptitudes para manejar situaciones concretas",
                q3 == "Seguridad y convivencia ciudadana",
                q4 == "Estratégica",
                q5 == "Conducción de operaciones a nivel de equipos",
            ])

# ====================== MÓDULO 2 ======================
def material_m2():
    st.header("📖 Material: Ciclo de Inteligencia")
    st.markdown("""
    <div class="lectura-box">
        <h3>Definición Estratégica</h3>
        <p>Es un proceso sistemático de <b>cinco pasos</b> orientado a la generación de conocimiento útil y veraz para un decisor final.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔄 Las 5 Fases del Ciclo")
    col1, col2 = st.columns(2)
    fases_izq = [
        ("1. Recolectar", "#3498db", "Obtención de la <b>información bruta</b> necesaria. Búsqueda activa en campo y bases de datos."),
        ("2. Tratar", "#9b59b6", "Procesamiento, registro y organización de los datos. Se traduce o decodifica la información."),
        ("3. Analizar", "#f1c40f", "<b>Fase crítica:</b> Transformación de datos en inteligencia mediante valoración, integración e interpretación."),
    ]
    fases_der = [
        ("4. Comunicar e Integrar", "#2ecc71", "Difusión selectiva de los resultados al decisor mediante instrumentos formales."),
        ("5. Evaluar y Retroalimentar", "#e74c3c", "Revisión constante para asegurar que el producto cumple con los requerimientos originales."),
    ]
    with col1:
        for titulo, color, desc in fases_izq:
            st.markdown(f'<div class="card-dark" style="border-left: 4px solid {color};"><h4 style="color:{color}; margin:0;">{titulo}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
    with col2:
        for titulo, color, desc in fases_der:
            st.markdown(f'<div class="card-dark" style="border-left: 4px solid {color};"><h4 style="color:{color}; margin:0;">{titulo}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
        st.info("**Importante:** El ciclo es dinámico. Un fallo en 'Tratar' puede invalidar todo el análisis posterior.")

def examen_m2(modulo_label):
    st.header("📝 Evaluación: Módulo 2")
    with st.form("exam_m2"):
        q1 = st.radio("1. ¿Cuál es el objetivo final del Ciclo de Inteligencia?",
            ["Solo recolectar datos", "Generar conocimiento útil para un decisor", "Realizar capturas"])
        q2 = st.radio("2. Fase donde la información bruta se transforma en inteligencia:",
            ["Recolectar", "Analizar", "Comunicar"])
        q3 = st.radio("3. ¿En qué consiste la fase de 'Tratar'?",
            ["Difundir el informe", "Procesamiento y organización de los datos", "Retroalimentar al jefe"])
        q4 = st.radio("4. ¿Cuál es el último paso del ciclo según el material?",
            ["Comunicar e Integrar", "Evaluar y Retroalimentar", "Tratar"])
        q5 = st.radio("5. ¿A quién se le difunde el resultado del ciclo?",
            ["Al público general", "Al destinatario final (Decisor)", "A todas las unidades"])
        if st.form_submit_button("FINALIZAR EXAMEN"):
            finalizar_examen(modulo_label, [
                q1 == "Generar conocimiento útil para un decisor",
                q2 == "Analizar",
                q3 == "Procesamiento y organización de los datos",
                q4 == "Evaluar y Retroalimentar",
                q5 == "Al destinatario final (Decisor)",
            ])

# ====================== MÓDULO 3 ======================
def material_m3():
    st.header("📖 Material Completo: Recolección de Información")
    t1, t2, t3, t4 = st.tabs(["📌 Fundamentos y PHVA", "🕵️ Operaciones", "👥 Fuentes Humanas", "🎤 La Entrevista"])

    with t1:
        st.markdown("""
        <div class="lectura-box">
            <h3>¿Qué es información?</h3>
            <p>Es un conjunto de <b>datos integrados y ordenados</b> que sirven para construir un mensaje. Es la materia prima para resolver problemas y tomar decisiones.</p>
            <p style="color: #D4AF37; font-weight: bold;">⚠️ El DATO es la unidad básica que comprende la información.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### El Ciclo PHVA en Recolección")
        cp1, cp2 = st.columns(2)
        with cp1:
            st.write("**🔵 PLANEAR:** Establecer objetivos, identificar riesgos y planificar recursos.")
            st.write("**🟢 HACER:** Búsqueda de información, ejecutar actividades y elaborar productos.")
        with cp2:
            st.write("**🟠 VERIFICAR:** Autoevaluación de control y gestión (seguimiento).")
            st.write("**🔴 ACTUAR:** Implementar acciones correctivas o preventivas.")

    with t2:
        st.subheader("🕵️ Operaciones de Inteligencia Policial")
        st.markdown("""
        <div class="lectura-box">
            <h4>Fines Operacionales</h4>
            <p>Son actividades del servicio policial orientadas a la obtención de información privilegiada. Para toda operación se requiere el <b>Empleo y uso de Medios Técnicos</b>.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🛠️ CLASIFICACIÓN OPERATIVA", expanded=True):
            co1, co2 = st.columns(2)
            with co1:
                st.markdown("""
                <div class="ejemplo-box" style="border-left: 5px solid #4CAF50;">
                    <h3 style="color: #4CAF50;">Básicas</h3>
                    <ul><li><b>🔍 Reconocimiento:</b> Concretar y ampliar datos previos.</li>
                    <li><b>✅ Verificación:</b> Establecer veracidad o desvirtuar.</li>
                    <li><b>🔭 Vigilancia:</b> Observación continua y discreta.</li>
                    <li><b>🚗 Seguimiento:</b> Control sobre personas o elementos en movimiento.</li>
                    <li><b>🗣️ Sonsacamiento:</b> Diálogo sutil e invisible.</li></ul>
                </div>""", unsafe_allow_html=True)
            with co2:
                st.markdown("""
                <div class="ejemplo-box" style="border-left: 5px solid #ef6c00;">
                    <h3 style="color: #ef6c00;">Especializadas</h3>
                    <ul><li><b>👤 Admón. de F.H.:</b> Dirección y control de fuentes humanas.</li>
                    <li><b>🎙️ Entrevista:</b> Intercambio de ideas para obtener información.</li>
                    <li><b>👥 Infiltración:</b> Ubicar agentes dentro de una organización.</li>
                    <li><b>🔑 Penetración:</b> Obtener colaboración permanente de alguien con acceso.</li>
                    <li><b>🎭 Caracterización y Fachada:</b> El rol y el entorno que lo respalda.</li></ul>
                </div>""", unsafe_allow_html=True)

    with t3:
        st.subheader("👥 Administración de Fuentes Humanas")
        st.markdown("""
        <div class="lectura-box">
            <h4>Fases del Proceso Operativo</h4>
            <p>La administración de fuentes requiere un seguimiento riguroso para garantizar la fiabilidad de la información.</p>
        </div>
        """, unsafe_allow_html=True)

        f1, f2 = st.columns(2)
        with f1:
            st.markdown("""
            <div class="card-dark" style="border-top: 4px solid #3498db; min-height: 300px;">
                <h4 style="color: #3498db;">1. Exploración</h4>
                <p style="color: #bdc3c7;"><i>Búsqueda de fuentes</i></p>
                <ul style="color: white; font-size: 0.9em;">
                    <li><b>Búsqueda:</b> Localización activa.</li>
                    <li><b>Forma voluntaria:</b> Presentación espontánea.</li>
                    <li><b>Evaluación y motivación:</b> Análisis de intereses.</li>
                    <li><b>Selección preliminar:</b> Filtrado inicial.</li>
                </ul>
            </div>""", unsafe_allow_html=True)
            st.markdown("""
            <div class="card-dark" style="border-top: 4px solid #e74c3c;">
                <h4 style="color: #e74c3c;">3. Registro</h4>
                <p style="color: #bdc3c7;"><i>Ingresar la fuente en:</i></p>
                <ul style="color: white;"><li>Sistema de Administración de Fuentes Humanas (Oficial).</li></ul>
            </div>""", unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class="card-dark" style="border-top: 4px solid #f1c40f; min-height: 300px;">
                <h4 style="color: #f1c40f;">2. Aproximación</h4>
                <p style="color: #bdc3c7;"><i>Establecimiento de contacto</i></p>
                <ul style="color: white; font-size: 0.9em;">
                    <li><b>La Entrevista:</b> Primer contacto formal.</li>
                    <li><b>Sonsacamiento:</b> Técnica de obtención sutil.</li>
                    <li><b>Evaluación:</b> Calificación de acceso y credibilidad.</li>
                </ul>
            </div>""", unsafe_allow_html=True)
            st.markdown("""
            <div class="card-dark" style="border-top: 4px solid #2ecc71;">
                <h4 style="color: #2ecc71;">4. Entrenamiento</h4>
                <p style="color: #bdc3c7;"><i>Preparar la fuente</i></p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; color: white; font-size: 0.9em;">
                    <div>• Instruir</div><div>• Orientar</div><div>• Dirigir</div><div>• Controlar</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with t4:
        st.subheader("🎤 La Entrevista de Inteligencia")
        st.markdown("""
        <div class="lectura-box" style="border-left: 5px solid #e74c3c;">
            <h4 style="color: #e74c3c;">Tipos de Entrevistador a EVITAR</h4>
            <p>El entrevistador debe mantener el equilibrio y el control. Evite caer en los siguientes perfiles:</p>
        </div>
        """, unsafe_allow_html=True)

        ce1, ce2 = st.columns(2)
        perfiles_izq = [
            ("🌟 El Estrella", "Se siente superior, habla más que la fuente, la interrumpe y usa lenguaje rebuscado."),
            ("🏃 El Improvisado", "Trabaja desordenado y a la carrera. Confía ciegamente en su capacidad de improvisar."),
            ("🌀 El Enredado", "Le da muchas vueltas a un tema, usa palabras difíciles que confunden la comunicación."),
        ]
        perfiles_der = [
            ("📉 El Estrellado", "Se siente menos que la fuente, es tímido, de voz baja, deja desviar el tema."),
            ("🔇 El Sordo", "Se preocupa demasiado por su cuestionario y olvida lo esencial: escuchar."),
            ("🔫 El Metralleta", "La fuente no tiene tiempo de responder porque ya le sugiere la siguiente pregunta."),
        ]
        with ce1:
            for t, d in perfiles_izq:
                st.markdown(f'<div style="background-color:#262626; padding:15px; border-radius:10px; margin-bottom:15px; border-right:4px solid #D4AF37;"><h5 style="color:#D4AF37; margin:0;">{t}</h5><p style="color:#ecf0f1; font-size:0.85em;">{d}</p></div>', unsafe_allow_html=True)
        with ce2:
            for t, d in perfiles_der:
                st.markdown(f'<div style="background-color:#262626; padding:15px; border-radius:10px; margin-bottom:15px; border-right:4px solid #D4AF37;"><h5 style="color:#D4AF37; margin:0;">{t}</h5><p style="color:#ecf0f1; font-size:0.85em;">{d}</p></div>', unsafe_allow_html=True)

        st.info("**Nota Técnica:** El éxito de la entrevista radica en el **Rapport** y la escucha activa.")

def examen_m3(modulo_label):
    st.header("📝 Evaluación: Módulo 3")
    with st.form("exam_m3"):
        q1 = st.radio("1. ¿Qué es el Sonsacamiento?",
            ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Vigilancia fija"])
        q2 = st.radio("2. En PHVA, ¿qué implica la etapa HACER?",
            ["Planificar recursos", "Búsqueda de información y ejecución", "Acciones preventivas"])
        q3 = st.radio("3. Diferencia entre Infiltración y Penetración:",
            ["No hay diferencia", "Infiltración mete al agente; Penetración usa a alguien de adentro", "Infiltración es solo técnica"])
        q4 = st.radio("4. ¿Cuál es la unidad básica que comprende la información?",
            ["El mensaje", "El dato", "El informe"])
        q5 = st.radio("5. ¿Qué busca el Reconocimiento?",
            ["Solo vigilar", "Concretar datos de inmuebles, seguridad y entorno", "Sonsacar a la fuente"])
        if st.form_submit_button("FINALIZAR EXAMEN"):
            finalizar_examen(modulo_label, [
                q1 == "Diálogo donde la fuente no debe percatarse de la explotación",
                q2 == "Búsqueda de información y ejecución",
                q3 == "Infiltración mete al agente; Penetración usa a alguien de adentro",
                q4 == "El dato",
                q5 == "Concretar datos de inmuebles, seguridad y entorno",
            ])

# ====================== MÓDULO 4 ======================
def material_m4():
    st.header("📖 Material: Tratamiento de la Información")
    tab_fund, tab_tipos, tab_comp, tab_4x4 = st.tabs(["📌 Fundamentos", "🔍 Tipos y EEI", "🛠️ Componentes", "📊 Código 4x4"])

    with tab_fund:
        st.markdown("""
        <div class="lectura-box">
            <h3>Definición</h3>
            <p>Procedimiento <b>sistemático</b> que consiste en someter todos los datos recolectados a un proceso de organización, clasificación y valoración preliminar, enmarcado en la <b>Constitución y la Jurisprudencia nacional</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("📊 Esquema de Tratamiento")
        ce1, ce2 = st.columns(2)
        with ce1:
            st.info("**Flujo de Trabajo:**\n\nInsumos ➡️ Proceso ➡️ Producto")
        with ce2:
            st.success("**Transformación:**\n\nInformación ➡️ Transformación ➡️ Inteligencia")
        st.markdown("""
        <div style="background-color: #003366; border: 2px solid #D4AF37; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: white; margin-bottom: 10px;">Ecuación de Tratamiento</h3>
            <h2 style="color: #D4AF37; margin-top: 0;">Información + Conocimiento = Decisión</h2>
        </div>
        """, unsafe_allow_html=True)

    with tab_tipos:
        ct1, ct2 = st.columns(2)
        with ct1:
            st.markdown("""
            <div class="card-dark" style="min-height: 350px;">
                <h4 style="color: #D4AF37;">💡 Tipos de Información</h4>
                <p style="color: #ccc;"><b>1. Genérica:</b> Información de contexto que ayuda a entender el entorno general.</p>
                <p style="color: #ccc;"><b>2. Específica:</b> Información puntual sobre un blanco o fenómeno, para decisiones tácticas.</p>
            </div>""", unsafe_allow_html=True)
        with ct2:
            st.markdown("""
            <div class="card-dark" style="min-height: 350px;">
                <h4 style="color: #D4AF37;">🔑 Elementos Esenciales de Información (EEI)</h4>
                <ul style="color: #ccc; font-size: 0.9em;">
                    <li><b>¿QUÉ?:</b> El hecho observado.</li>
                    <li><b>¿CUÁNDO?:</b> Temporalidad.</li>
                    <li><b>¿DÓNDE?:</b> Ubicación espacial.</li>
                    <li><b>¿CÓMO?:</b> Modus operandi.</li>
                    <li><b>¿QUIÉN?:</b> Actores y sujetos.</li>
                    <li><b>¿POR QUÉ?:</b> Causas y motivaciones.</li>
                    <li><b>¿PARA QUÉ?:</b> Objetivo final.</li>
                </ul>
            </div>""", unsafe_allow_html=True)

    with tab_comp:
        st.subheader("⚙️ Componentes del Tratamiento")
        cc1, cc2 = st.columns(2)
        with cc1:
            st.write("**📂 ORGANIZACIÓN**")
            st.caption("Determinar tipo de información, blanco y nivel de prioridad.")
            st.write("**🛡️ CLASIFICACIÓN**")
            st.caption("Origen de la fuente, estado del proceso y nivel de seguridad.")
        with cc2:
            st.write("**⚖️ VALORACIÓN**")
            st.caption("Evaluar si es oportuna, confiable y creíble.")
            st.write("**📝 REGISTRO**")
            st.caption("Ingreso cronológico, detallado y sistemático en bases de datos.")

    with tab_4x4:
        st.subheader("📋 Matriz de Evaluación 4x4")
        st.markdown("""
        <table class="t-4x4">
            <tr><th colspan="2">CONFIABILIDAD (FUENTE)</th><th colspan="2">CREDIBILIDAD (INFO)</th><th>%</th></tr>
            <tr><td class="cod-cell">A</td><td>Totalmente confiable</td><td class="cod-cell">1</td><td>Confirmada/Cierta</td><td class="perc-100">100</td></tr>
            <tr><td class="cod-cell">B</td><td>Usualmente confiable</td><td class="cod-cell">2</td><td>De primera mano</td><td class="perc-75">75</td></tr>
            <tr><td class="cod-cell">C</td><td>Dudosa/No confiable</td><td class="cod-cell">3</td><td>Corroborable</td><td class="perc-50">50</td></tr>
            <tr><td class="cod-cell">D</td><td>Desconocida/Sin historial</td><td class="cod-cell">4</td><td>No corroborable</td><td class="perc-25">25</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("---")
        cex1, cex2 = st.columns(2)
        with cex1:
            st.success("**Ejemplo A-1 (100%):** Agente infiltrado entrega grabación original.")
        with cex2:
            st.error("**Ejemplo D-4 (25%):** Llamada anónima con datos imposibles de verificar.")

def examen_m4(modulo_label):
    st.header("📝 Evaluación: Módulo 4")
    with st.form("exam_m4"):
        q1 = st.radio("1. ¿Qué implica la etapa de 'Organización'?",
            ["Captura de objetivos", "Determinar tipo de información, blanco y prioridad", "Publicar en redes sociales"])
        q2 = st.radio("2. Según la matriz 4x4, el código 'C-3' representa:",
            ["100%", "75%", "50%"])
        q3 = st.radio("3. El Tratamiento busca garantizar que el registro se enmarque en:",
            ["Revistas de prensa", "La Constitución y la Jurisprudencia nacional", "Manuales de software"])
        q4 = st.radio("4. ¿Qué elemento de los EEI responde al 'Por qué'?",
            ["Temporalidad", "Causas y motivaciones", "Ubicación"])
        q5 = st.radio("5. ¿Cuál es el producto final tras someter la Información al Proceso?",
            ["Datos crudos", "Inteligencia", "Insumos"])
        if st.form_submit_button("FINALIZAR EXAMEN"):
            finalizar_examen(modulo_label, [
                q1 == "Determinar tipo de información, blanco y prioridad",
                q2 == "50%",
                q3 == "La Constitución y la Jurisprudencia nacional",
                q4 == "Causas y motivaciones",
                q5 == "Inteligencia",
            ])

# ====================== MÓDULO 5 ======================
def material_m5():
    st.header("🧠 Material: Análisis de la Información")
    tab_est, tab_proc, tab_lca, tab_sint = st.tabs(["🔬 Estudio Especializado", "🧩 Proceso de Análisis", "⏳ Línea LCA", "💡 Síntesis"])

    with tab_est:
        st.subheader("Estudio Especializado de la Información")
        st.write("El análisis es un proceso cuyo objeto es **generar conocimiento**, con base en la información disponible.")
        st.info("""**Fases del Análisis:**
1. **Interpretación:** Dar sentido a los datos aislados.
2. **Integración:** Unir piezas para ver el cuadro completo.
3. **Hipótesis:** Plantear suposiciones técnicas fundamentadas.
4. **Conclusiones:** Resultados finales derivados del razonamiento.""")

    with tab_proc:
        st.subheader("🧩 El Proceso Analítico (Descomposición)")
        cf1, cf2, cf3 = st.columns(3)
        with cf1:
            st.markdown('<div style="text-align:center; background:#f2dede; padding:15px; border-radius:10px; min-height:180px; color:#a94442;"><h3>EL TODO</h3>🧩<br><small>Objeto de análisis completo.</small></div>', unsafe_allow_html=True)
        with cf2:
            st.markdown('<div style="text-align:center; background:#fcf8e3; padding:15px; border-radius:10px; min-height:180px; color:#8a6d3b;"><h3>ANALIZAR</h3>🔍<br><small>Descomponer. Identificar cada elemento individual.</small></div>', unsafe_allow_html=True)
        with cf3:
            st.markdown('<div style="text-align:center; background:#d9edf7; padding:15px; border-radius:10px; min-height:180px; color:#31708f;"><h3>SINTETIZAR</h3>💡<br><small>Recomponer para entender el significado final.</small></div>', unsafe_allow_html=True)
        st.caption("Analizar es descomponer el todo; sintetizar es recomponer para entender el significado final.")

    with tab_lca:
        st.subheader("⏳ LCA: Línea del Conocimiento Analítico")
        st.markdown("""
        <div style="display: flex; justify-content: space-around; align-items: center; background: linear-gradient(90deg, #2c5d63, #c0392b, #f39c12); padding: 30px; border-radius: 15px; color: white; font-weight: bold;">
            <div style="text-align: center;">PASADO<br><span style="font-weight:normal; font-size:0.8em;">Antecedentes</span></div>
            <div style="font-size: 2em;">➔</div>
            <div style="text-align: center; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px;">PRESENTE<br><span style="font-weight:normal; font-size:0.8em;">Interpretación</span></div>
            <div style="font-size: 2em;">➔</div>
            <div style="text-align: center;">FUTURO<br><span style="font-weight:normal; font-size:0.8em;">Prospectiva</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.info("La LCA transforma la memoria histórica en proyecciones mediante la interpretación técnica del presente.")

    with tab_sint:
        st.subheader("🎯 Resultados y Cursos de Acción")
        st.markdown("""El análisis genera conocimiento estratégico para:
- **Formular Hipótesis:** Suposiciones basadas en datos técnicos y evidencia.
- **Definir Escenarios:** Posibles evoluciones de un fenómeno criminal o social.
- **Cursos de Acción:** Recomendaciones específicas para la toma de decisiones.""")
        st.warning("⚠️ Sin una síntesis clara que oriente la acción, la inteligencia pierde su valor operativo.")

def examen_m5(modulo_label):
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>📝 EVALUACIÓN: MÓDULO 5</h2>", unsafe_allow_html=True)
    with st.form("examen_m5"):
        q1 = st.radio("1. ¿Cuál es el objeto principal del proceso de análisis?",
            ["Recopilar la mayor cantidad de datos posible", "Generar conocimiento con base en la información disponible",
             "Archivar antecedentes históricos", "Interceptar comunicaciones en tiempo real"], index=None)
        q2 = st.multiselect("2. Seleccione las 4 fases del Estudio Especializado:",
            ["Interpretación", "Recolección", "Integración", "Hipótesis", "Difusión", "Conclusiones"], max_selections=4)
        q3 = st.selectbox("3. ¿En qué consiste 'ANALIZAR' dentro del proceso analítico?",
            [None, "Recomponer las partes para entender el significado final",
             "Descomponer el todo e identificar cada elemento individual",
             "Ignorar las ideas secundarias para enfocarse en el todo"])
        q4 = st.radio("4. En la LCA, ¿qué transforma la memoria histórica en proyecciones?",
            ["La recolección de fuentes humanas", "La interpretación técnica del presente",
             "El almacenamiento masivo de datos", "La suerte y el azar"], index=None)
        q5 = st.radio("5. ¿Qué sucede si la inteligencia no tiene una síntesis clara?",
            ["Gana valor estratégico", "Se vuelve más confidencial",
             "Pierde su valor operativo y de orientación", "Es más fácil de interpretar"], index=None)

        if st.form_submit_button("FINALIZAR Y REGISTRAR EVALUACIÓN"):
            puntos = 0
            if q1 == "Generar conocimiento con base en la información disponible": puntos += 1
            if set(q2) == {"Interpretación", "Integración", "Hipótesis", "Conclusiones"}: puntos += 1
            if q3 == "Descomponer el todo e identificar cada elemento individual": puntos += 1
            if q4 == "La interpretación técnica del presente": puntos += 1
            if q5 == "Pierde su valor operativo y de orientación": puntos += 1
            nota = (puntos / 5) * 100
            guardar_nota(st.session_state["agente_nombre"], modulo_label, nota)
            if nota >= 70:
                st.balloons()
                st.success(f"✅ Nota: {nota:.0f}%")
            else:
                st.warning(f"⚠️ Nota: {nota:.0f}%. Se recomienda repasar.")
            st.session_state["modo_examen"] = False
            st.rerun()

    if st.button("⬅️ Cancelar y Volver al Material"):
        st.session_state["modo_examen"] = False
        st.rerun()

# ====================== MÓDULO 6 ======================
def material_m6():
    st.header("📢 Material: Comunicar e Integrar")
    st.info("La inteligencia no sirve si no llega a quien debe tomar la decisión en el momento oportuno.")
    tab_p, tab_ej, tab_seg = st.tabs(["🚀 Pasos para la Difusión", "📝 Casos Prácticos", "🔐 Seguridad en Entrega"])

    with tab_p:
        st.subheader("Procedimiento Estándar de Difusión")
        pasos = [
            ("1", "Identificar el Receptor", "Nombres, cargo y lugar de recepción pactado con el usuario."),
            ("2", "Selección del Canal", "Definir si será Virtual (correo cifrado), Físico o Entrega Exclusiva."),
            ("3", "Mecanismos de Seguridad", "Aplicación de clasificación, encriptación, codificación o embalaje."),
            ("4", "Difusión del PTI", "Entrega formal al destinatario final según el portafolio de receptores."),
            ("5", "Registro en Base de Datos", "Registro digital o planilla física (si es entrega exclusiva)."),
        ]
        for n, t, d in pasos:
            st.markdown(f"""
            <div style="background-color: #002147; border-left: 5px solid #D4AF37; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                <span style="color: #D4AF37; font-weight: bold; font-size: 1.2em;">Paso {n}: {t}</span><br>
                <span style="color: white; font-size: 0.95em;">{d}</span>
            </div>""", unsafe_allow_html=True)

    with tab_ej:
        st.subheader("Ejemplos de Aplicación")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div style="background-color: #001a33; padding: 20px; border-radius: 10px; border: 1px solid #444; min-height: 200px;">
                <h4 style="color: #D4AF37;">Ejemplo A: Canal Virtual</h4>
                <p style="font-size: 0.9em; color: white;"><b>Escenario:</b> Envío de reporte diario.<br><b>Acción:</b> Email con PDF cifrado PGP.</p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div style="background-color: #001a33; padding: 20px; border-radius: 10px; border: 1px solid #444; min-height: 200px;">
                <h4 style="color: #D4AF37;">Ejemplo B: Entrega Exclusiva</h4>
                <p style="font-size: 0.9em; color: white;"><b>Escenario:</b> Orden de captura.<br><b>Acción:</b> Sobre sellado y firma en planilla.</p></div>""", unsafe_allow_html=True)

    with tab_seg:
        st.subheader("Medidas de Protección del Producto")
        st.markdown("""<div style="background-color: #0e1117; padding: 20px; border: 1px dashed #D4AF37; border-radius: 10px;">
            <ul style="color: white; line-height: 1.8;">
                <li><b>Clasificación:</b> Marcar como <b>RESERVADO</b> o <b>SECRETO</b>.</li>
                <li><b>Encriptación:</b> Algoritmos para proteger datos digitales.</li>
                <li><b>Embalaje:</b> Sobres de seguridad físicos.</li>
                <li><b>Codificación:</b> Lenguaje convenido o alias.</li>
            </ul></div>""", unsafe_allow_html=True)

def examen_m6(modulo_label):
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>📝 EVALUACIÓN: MÓDULO 6</h2>", unsafe_allow_html=True)
    with st.form("examen_m6"):
        q1 = st.radio("1. ¿Cuál es la premisa fundamental de la comunicación en inteligencia?",
            ["Almacenar información indefinidamente", "Que la inteligencia llegue al decisor en el momento oportuno", "Publicar resultados en redes"], index=None)
        q2 = st.selectbox("2. ¿Cuál es el primer paso antes de la difusión?",
            [None, "Seleccionar el canal", "Identificar al receptor (nombre, cargo y lugar)", "Registrar en DB"])
        q3 = st.radio("3. ¿Qué medida garantiza físicamente que el producto no fue manipulado?",
            ["Encriptación de disco", "Embalaje en sobres de seguridad con cinta de evidencia", "Uso de correos personales"], index=None)
        q4 = st.radio("4. Al usar el Canal Virtual, ¿qué combinación de seguridad es correcta?",
            ["Archivo Excel abierto", "PDF protegido por contraseña y cifrado PGP", "Captura de pantalla por WhatsApp"], index=None)
        q5 = st.radio("5. ¿Qué es obligatorio tras una 'Entrega Exclusiva' física?",
            ["Destruir el documento original", "Firma obligatoria en la planilla de difusión física", "Notificar a los medios"], index=None)

        if st.form_submit_button("REGISTRAR RESULTADOS"):
            finalizar_examen(modulo_label, [
                q1 == "Que la inteligencia llegue al decisor en el momento oportuno",
                q2 == "Identificar al receptor (nombre, cargo y lugar)",
                q3 == "Embalaje en sobres de seguridad con cinta de evidencia",
                q4 == "PDF protegido por contraseña y cifrado PGP",
                q5 == "Firma obligatoria en la planilla de difusión física",
            ])

    if st.button("⬅️ Volver al Material"):
        st.session_state["modo_examen"] = False
        st.rerun()

# ====================== MÓDULO 7 ======================
def material_m7():
    st.header("🔄 Material: Evaluar y Retroalimentar")
    st.markdown("""
    <div style="background: linear-gradient(90deg, #002147, #003366); padding: 25px; border-radius: 15px; border-right: 5px solid #D4AF37; margin-bottom: 25px;">
        <h3 style="color: #D4AF37; margin-top: 0;">🎯 Objetivo de la Fase</h3>
        <p style="color: white; font-size: 1.1em;">
            Evaluar el impacto del <b>Plan Nacional (PNIP)</b>, <b>Planes Regionales</b> y los productos de inteligencia,
            asegurando que los responsables del ciclo identifiquen oportunidades reales de mejoramiento.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_act, tab_sin, tab_ej = st.tabs(["⚙️ Actividades Clave", "📊 Trazabilidad", "📝 Casos de Evaluación"])

    with tab_act:
        st.subheader("Ruta Crítica de Evaluación")
        for act in ["1. Planificar y programar la evaluación.",
                     "2. Realizar trazabilidad en SINAI.",
                     "3. Seleccionar productos para rastreo.",
                     "4. Trazabilidad de los planes de inteligencia.",
                     "5. Analizar el impacto decisional."]:
            st.markdown(f'<div style="background-color: #0e1117; padding: 12px; border-radius: 8px; border: 1px solid #444; margin-bottom: 8px; color: #D4AF37; font-weight: bold;">{act}</div>', unsafe_allow_html=True)

    with tab_sin:
        st.subheader("Trazabilidad en SINAI")
        st.info("La trazabilidad no es solo archivo; es el rastreo de acciones y decisiones tomadas basadas en nuestra inteligencia.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="lectura-box"><h4 style="color: #D4AF37;">¿Qué evaluamos?</h4><ul><li><b>Pertinencia:</b> ¿Respondió al requerimiento?</li><li><b>Oportunidad:</b> ¿Llegó a tiempo?</li><li><b>Exactitud:</b> ¿Fue veraz?</li></ul></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="lectura-box"><h4 style="color: #D4AF37;">Impacto Decisional</h4><p>Se mide si el producto generó una acción concreta: una captura, una desarticulación, o un cambio en la política de seguridad regional.</p></div>', unsafe_allow_html=True)

    with tab_ej:
        st.subheader("Ejemplos de Retroalimentación")
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="ejemplo-box" style="border-left: 4px solid #4CAF50;">
                <h4 style="color: #4CAF50;">✅ Evaluación Positiva</h4>
                <p>5 capturas exitosas. Precisión geográfica destacada.</p>
            </div>
            <div class="ejemplo-box" style="border-left: 4px solid #F44336;">
                <h4 style="color: #F44336;">⚠️ Oportunidad de Mejora</h4>
                <p>Informe llegó 15 días tarde. Reajustar tiempos de tratamiento.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def examen_m7(modulo_label):
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>📝 EVALUACIÓN: MÓDULO 7</h2>", unsafe_allow_html=True)
    with st.form("examen_m7"):
        q1 = st.radio("1. ¿Cuál es el objetivo principal de la fase de Evaluación?",
            ["Almacenar reportes antiguos", "Identificar oportunidades de mejoramiento del servicio", "Sancionar al personal"], index=None)
        q2 = st.selectbox("2. ¿En qué sistema se realiza la trazabilidad?",
            [None, "Excel Local", "Sistema SINAI", "WhatsApp Institucional"])
        q3 = st.radio("3. ¿A qué criterio nos referimos cuando evaluamos si el producto llegó a tiempo?",
            ["Exactitud", "Pertinencia", "Oportunidad"], index=None)
        q4 = st.radio("4. ¿Cómo se mide el Impacto Decisional?",
            ["Por el número de páginas", "Si generó una acción concreta (captura, cambio de política)", "Por el uso de colores en gráficas"], index=None)
        q5 = st.radio("5. ¿Qué paso sigue tras la trazabilidad general en SINAI?",
            ["Finalizar el ciclo", "Seleccionar productos específicos para rastreo detallado", "Borrar los datos para liberar espacio"], index=None)

        if st.form_submit_button("REGISTRAR RESULTADOS FINALES"):
            finalizar_examen(modulo_label, [
                q1 == "Identificar oportunidades de mejoramiento del servicio",
                q2 == "Sistema SINAI",
                q3 == "Oportunidad",
                q4 == "Si generó una acción concreta (captura, cambio de política)",
                q5 == "Seleccionar productos específicos para rastreo detallado",
            ])

    if st.button("⬅️ Volver al Material"):
        st.session_state["modo_examen"] = False
        st.rerun()


# ############################################################
#         SECCIONES PRINCIPALES POST-LOGIN
# ############################################################

# Mapeo consistente de nombres de módulos (para BD)
MODULOS = [
    {"id": "M1", "label": "Módulo 1", "titulo": "Conceptualización", "icon": "📖",
     "material": material_m1, "examen": examen_m1},
    {"id": "M2", "label": "Módulo 2", "titulo": "Ciclo de Inteligencia", "icon": "🔄",
     "material": material_m2, "examen": examen_m2},
    {"id": "M3", "label": "Módulo 3", "titulo": "Recolección", "icon": "🕵️",
     "material": material_m3, "examen": examen_m3},
    {"id": "M4", "label": "Módulo 4", "titulo": "Tratamiento", "icon": "📊",
     "material": material_m4, "examen": examen_m4},
    {"id": "M5", "label": "Módulo 5", "titulo": "Análisis", "icon": "🧠",
     "material": material_m5, "examen": examen_m5},
    {"id": "M6", "label": "Módulo 6", "titulo": "Comunicación", "icon": "📢",
     "material": material_m6, "examen": examen_m6},
    {"id": "M7", "label": "Módulo 7", "titulo": "Evaluación", "icon": "🔄",
     "material": material_m7, "examen": examen_m7},
]

def seccion_inicio():
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🛡️ SISTEMA ESTRATÉGICO DE CAPACITACIÓN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Dirección de Inteligencia Policial (DIPOL)</p>", unsafe_allow_html=True)
    st.divider()

    cols = st.columns(3)
    for i, m in enumerate(MODULOS):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #002147, #001226);
                        padding: 25px; border-radius: 15px; border: 1px solid #D4AF37;
                        text-align: center; margin-bottom: 20px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.5); min-height: 220px;">
                <div style="font-size: 3em; margin-bottom: 10px;">{m['icon']}</div>
                <h3 style="color: #D4AF37; margin: 0;">{m['label']}</h3>
                <p style="color: #ffffff; font-size: 0.9em; opacity: 0.8;">{m['titulo']}</p>
            </div>
            """, unsafe_allow_html=True)

def seccion_modulos():
    # Resetear modo_examen al cambiar de módulo
    opciones = [f"{m['label']}: {m['titulo']}" for m in MODULOS]
    seleccion = st.selectbox("Seleccione Módulo de Estudio:", opciones, key="selector_modulo")
    idx = opciones.index(seleccion)
    mod = MODULOS[idx]

    # Si el usuario cambió de módulo, salir del modo examen
    if st.session_state.get("_ultimo_modulo") != mod["label"]:
        st.session_state["modo_examen"] = False
        st.session_state["_ultimo_modulo"] = mod["label"]

    bloque_examen(mod["label"], mod["material"], mod["examen"])

def seccion_progreso():
    nombre = st.session_state["agente_nombre"]
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #001f3f, #003366); padding: 20px; border-radius: 15px;
                border-left: 8px solid #D4AF37; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0;">📊 Mi Expediente Académico</h1>
        <p style="color: #D4AF37; margin: 5px 0 0 0; font-weight: bold;">{nombre}</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        df = cargar_datos_agente(nombre)
        if not df.empty:
            st.markdown("""<style>
                [data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 3.5rem !important; font-weight: 900 !important; }
                .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
            </style>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Mi Promedio", f"{df['nota'].mean():.1f}%")
            with c2:
                st.metric("Evaluaciones", len(df))
            st.write("---")
            st.dataframe(df, column_config={
                "nota": st.column_config.ProgressColumn("Nota Final", format="%d%%", min_value=0, max_value=100),
                "modulo": "Módulo", "fecha": "Fecha"
            }, use_container_width=True, hide_index=True)
        else:
            st.info("Aún no hay evaluaciones registradas.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

def seccion_dashboard():
    if not st.session_state.get("es_admin", False):
        st.error("🚫 Acceso Denegado: Se requieren credenciales de Administrador.")
        return

    st.markdown("""
    <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-bottom: 4px solid #D4AF37; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0;">🛡️ Centro de Inteligencia Analítica</h1>
        <p style="color: #D4AF37; margin: 0; font-weight: bold;">Panel de Control y Rendimiento Académico - DIPOL</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        df_raw = cargar_todo_admin()
        if df_raw.empty:
            st.info("ℹ️ No hay registros para generar el análisis.")
            return

        df_raw["fecha"] = pd.to_datetime(df_raw["fecha"])
        df_all = df_raw.sort_values("fecha").drop_duplicates(subset=["funcionario", "modulo"], keep="last")
        df_all["fecha_display"] = df_all["fecha"].dt.strftime("%Y-%m-%d %H:%M")

        promedio = df_all["nota"].mean()
        total_eval = len(df_all)
        aprobados = len(df_all[df_all["nota"] >= 70])
        tasa_exito = (aprobados / total_eval) * 100

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><p class="metric-title">Evaluaciones</p><p class="metric-value">{total_eval}</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><p class="metric-title">Promedio</p><p class="metric-value">{promedio:.1f}%</p></div>', unsafe_allow_html=True)
        with m3:
            color_t = "#2ecc71" if tasa_exito >= 70 else "#e74c3c"
            st.markdown(f'<div class="metric-card"><p class="metric-title">Tasa Éxito</p><p class="metric-value" style="color:{color_t};">{tasa_exito:.1f}%</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><p class="metric-title">Agentes</p><p class="metric-value">{df_all["funcionario"].nunique()}</p></div>', unsafe_allow_html=True)

        tab_rend, tab_det = st.tabs(["📊 Rendimiento", "🔍 Detalle por Agente"])

        with tab_rend:
            cr1, cr2 = st.columns([1.2, 0.8])
            with cr1:
                st.subheader("Promedio por Componente Educativo")
                chart = df_all.groupby("modulo")["nota"].mean().reset_index()
                st.bar_chart(data=chart, x="modulo", y="nota", color="#D4AF37", use_container_width=True)
            with cr2:
                st.subheader("Distribución de Niveles")
                bins = [0, 69, 89, 100]
                labels = ["Insuficiente (0-69)", "Satisfactorio (70-89)", "Sobresaliente (90-100)"]
                df_all["Nivel"] = pd.cut(df_all["nota"], bins=bins, labels=labels)
                st.bar_chart(df_all["Nivel"].value_counts(), color="#2ecc71")

        with tab_det:
            cf, cd = st.columns([3, 1])
            with cf:
                search = st.text_input("🔍 Buscar funcionario...", placeholder="Nombre para filtrar")
            with cd:
                csv = df_all.to_csv(index=False).encode("utf-8")
                st.download_button("Descargar CSV", data=csv, file_name="reporte_dipol.csv", use_container_width=True)

            display = df_all if not search else df_all[df_all["funcionario"].str.contains(search, case=False)]
            st.dataframe(
                display.sort_values("fecha", ascending=False),
                column_config={
                    "nota": st.column_config.ProgressColumn("Calificación", format="%d%%", min_value=0, max_value=100),
                    "fecha_display": "Fecha", "funcionario": "Agente", "modulo": "Módulo"
                },
                column_order=("funcionario", "modulo", "nota", "fecha_display"),
                use_container_width=True, hide_index=True
            )

        st.divider()
        low = df_all[df_all["nota"] < 70]
        if not low.empty:
            with st.expander("⚠️ Personal con necesidad de refuerzo"):
                st.warning(f"{len(low)} evaluaciones por debajo del 70%.")
                st.table(low[["funcionario", "modulo", "nota"]])

    except Exception as e:
        st.error(f"❌ Error en el Dashboard: {e}")


# ############################################################
#                  FLUJO PRINCIPAL
# ############################################################

if not st.session_state["autenticado"]:
    pantalla_login()
else:
    # Marca de agua
    agente = st.session_state["agente_nombre"]
    st.markdown(f"""
    <div class="watermark-container">
        <div class="watermark-inline">{agente} — CONFIDENCIAL</div>
        <div class="watermark-inline" style="transform: rotate(30deg);">{agente} — CONFIDENCIAL</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("📂 MENÚ")
        rol = "🛡️ ADMIN" if st.session_state["es_admin"] else "👤 AGENTE"
        st.write(f"**{rol}:** {agente}")
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso", "📈 Dashboard General"])
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Contenido
    if seccion == "🏠 Inicio":
        seccion_inicio()
    elif seccion == "📚 Módulos":
        seccion_modulos()
    elif seccion == "📊 Mi Progreso":
        seccion_progreso()
    elif seccion == "📈 Dashboard General":
        seccion_dashboard()
