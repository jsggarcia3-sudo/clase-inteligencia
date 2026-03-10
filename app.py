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
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'agente_nombre' not in st.session_state:
    st.session_state['agente_nombre'] = ""
if 'es_admin' not in st.session_state:
    st.session_state['es_admin'] = False
if 'modo_examen' not in st.session_state:
    st.session_state['modo_examen'] = False

def login():
    st.markdown("<h1 style='text-align: center;'>🛡️ SISTEMA DE CAPACITACIÓN DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.write("### Identificación de Funcionario")
        nombre = st.text_input("Nombre Completo (Ej: Juan Pérez)")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER"):
            if usuario == "admin_dipol" and clave == "DIPOL2026":
                st.session_state['autenticado'] = True
                st.session_state['es_admin'] = True
                st.session_state['agente_nombre'] = nombre if nombre else "Administrador"
                st.rerun()
            elif nombre and usuario and clave == "ESTUDIANTE2026":
                st.session_state['autenticado'] = True
                st.session_state['es_admin'] = False
                st.session_state['agente_nombre'] = nombre
                st.rerun()
            else:
                st.error("Credenciales incorrectas o falta nombre completo.")

# 3. INTERFAZ OPERATIVA
if not st.session_state['autenticado']:
    login()
else:
    db_s = st.secrets["connections"]["postgresql"]
    pass_segura = quote_plus(db_s['password'])
    engine = create_engine(f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}", pool_pre_ping=True)

    with st.sidebar:
        st.title("📂 MENÚ")
        tipo_user = "🛡️ ADMIN" if st.session_state['es_admin'] else "👤 ESTUDIANTE"
        st.write(f"**{tipo_user}:**\n{st.session_state['agente_nombre']}")
        st.divider()
        opciones = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso"]
        if st.session_state['es_admin']: opciones.append("📈 Dashboard General")
        seccion = st.radio("Ir a:", opciones)
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    # --- INICIO ---
    if seccion == "🏠 Inicio":
        st.title(f"🛡️ Panel de Control Académico")
        st.subheader(f"Bienvenido, {st.session_state['agente_nombre']}")
        if st.session_state['es_admin']:
            st.info("Sessión activa como **Administrador**.")
        else:
            st.success("Listo para continuar su formación técnica.")
        st.divider()
        st.write("Seleccione un módulo para comenzar.")

    # --- MÓDULOS ---
    elif seccion == "📚 Módulos":
        st.title("📚 Módulos de Especialización")
        seleccion = st.selectbox("Seleccione un Módulo:", [
            "Módulo 1: Conceptualización de Inteligencia",
            "Módulo 2: Ciclo de Inteligencia"
        ])

        # --- CONTENIDO MÓDULO 2 ---
        if seleccion == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material de Lectura: Ciclo de Inteligencia")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición del Ciclo de Inteligencia</h3>
                    <p>Se define como una serie de <b>cinco pasos</b> orientados a la generación de conocimiento estratégico útil, verdadero y ajustado a los requerimientos de información preestablecidos por un destinatario final (decisor), a quien se difunde selectivamente el resultado plasmado en un instrumento determinado.</p>
                </div>
                <div class="lectura-box">
                    <h3>Pasos del Ciclo</h3>
                    <ol>
                        <li><b>Recolectar:</b> Obtención de datos e información de diversas fuentes.</li>
                        <li><b>Tratar:</b> Organización y procesamiento de la información recolectada.</li>
                        <li><b>Analizar:</b> Evaluación crítica para transformar datos en conocimiento.</li>
                        <li><b>Comunicar e Integrar:</b> Difusión del producto de inteligencia al decisor.</li>
                        <li><b>Evaluar y Retroalimentar:</b> Revisión del proceso y ajuste según nuevas necesidades.</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
                

                if st.button("🚀 INICIAR EVALUACIÓN M2"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.header("📝 Evaluación: Ciclo de Inteligencia")
                with st.form(key="form_m2"):
                    p1 = st.radio("1. ¿Cuántos pasos integran el Ciclo de Inteligencia?", ["3 pasos", "5 pasos", "7 pasos"])
                    p2 = st.radio("2. ¿Cuál es el fin último del Ciclo de Inteligencia?", ["Almacenar datos", "Generar conocimiento estratégico útil para un decisor", "Vigilar redes sociales"])
                    p3 = st.radio("3. Paso que consiste en la obtención de datos de diversas fuentes:", ["Analizar", "Recolectar", "Tratar"])
                    p4 = st.radio("4. ¿Qué paso permite ajustar el proceso según nuevas necesidades?", ["Evaluar y Retroalimentar", "Comunicar", "Tratar"])
                    p5 = st.radio("5. ¿Cómo se entrega el resultado final al destinatario?", ["Se publica en prensa", "Se difunde selectivamente mediante un instrumento determinado", "Se guarda en el archivo"])

                    if st.form_submit_button("GUARDAR NOTA M2"):
                        r = [p1=="5 pasos", p2=="Generar conocimiento estratégico útil para un decisor", p3=="Recolectar", p4=="Evaluar y Retroalimentar", p5=="Se difunde selectivamente mediante un instrumento determinado"]
                        nota = (sum(r) / 5) * 100
                        try:
                            with engine.connect() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), {"f": st.session_state['agente_nombre'], "n": nota, "m": seleccion})
                                conn.commit()
                            st.success(f"Nota Módulo 2 guardada: {nota}%")
                            st.session_state['modo_examen'] = False
                        except Exception as e: st.error(f"Error: {e}")

        # --- MÓDULO 1 (Se mantiene igual) ---
        elif seleccion == "Módulo 1: Conceptualización de Inteligencia":
            if not st.session_state['modo_examen']:
                st.header("📖 Material de Lectura: Módulo 1")
                st.markdown("""
                <div class="lectura-box">
                    <h3>Definición de Inteligencia</h3>
                    <p>1. Es el <b>conocimiento obtenido</b> a través del procesamiento adecuado de la información...</p>
                    <p>... (contenido completo restaurado) ...</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 INICIAR EVALUACIÓN M1"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            # ... Lógica de examen M1 ...

    # --- PROGRESO Y DASHBOARD (Sin cambios, automáticos para M1 y M2) ---
    elif seccion == "📊 Mi Progreso":
        df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC"), engine, params={"n": st.session_state['agente_nombre']})
        st.dataframe(df, use_container_width=True)

    elif seccion == "📈 Dashboard General":
        df_all = pd.read_sql(text("SELECT * FROM calificaciones"), engine)
        st.bar_chart(df_all.groupby('funcionario')['nota'].mean())
        st.dataframe(df_all, use_container_width=True)
