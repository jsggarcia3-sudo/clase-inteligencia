import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 1. CONFIGURACIÓN INICIAL (Debe ir al puro principio)
st.set_page_config(page_title="Plataforma Educativa DIPOL", page_icon="🛡️", layout="wide")

# 2. CONEXIÓN A BASE DE DATOS (Se define fuera para que la caché la vea)
# Extraemos los secretos de Streamlit
try:
    db_s = st.secrets["connections"]["postgresql"]
    # Usamos quote_plus por si la contraseña tiene caracteres especiales (@, #, $)
    pass_clean = quote_plus(db_s['password'])
    conn_str = f"postgresql://{db_s['username']}:{pass_clean}@{db_s['host']}:{db_s['port']}/{db_s['database']}"
    engine = create_engine(conn_str)
except Exception as e:
    st.error("Error al cargar credenciales de base de datos. Verifica st.secrets.")

# 3. FUNCIONES DE DATOS CON CACHÉ (Para velocidad máxima)
@st.cache_data(ttl=60)
def cargar_datos_agente(nombre_agente):
    with engine.connect() as conn:
        query = text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC")
        return pd.read_sql(query, conn, params={"n": nombre_agente})

@st.cache_data(ttl=60)
def cargar_todo_admin():
    with engine.connect() as conn:
        query = text("SELECT funcionario, modulo, nota, fecha FROM calificaciones")
        return pd.read_sql(query, conn)

# 4. ESTILOS VISUALES
st.markdown("""
    <style>
    .stApp { background-color: #001226; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #002147; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 3rem !important; font-weight: 800; }
    .stButton>button { width: 100%; border-radius: 4px; background-color: #D4AF37; color: #001226; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ffffff; color: #001226; }
    </style>
    """, unsafe_allow_html=True)

# 5. GESTIÓN DE SESIÓN
if 'autenticado' not in st.session_state: st.session_state['autenticado'] = False
if 'agente_nombre' not in st.session_state: st.session_state['agente_nombre'] = ""
if 'es_admin' not in st.session_state: st.session_state['es_admin'] = False

def login():
    st.markdown("<h1 style='text-align: center; font-size: 3em;'>🛡️ SISTEMA DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        with st.form("login_form"):
            st.write("### Identificación de Funcionario")
            nombre = st.text_input("Nombre Completo")
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("ACCEDER AL SISTEMA")
            
            if submit:
                if usuario == "admin_dipol" and clave == "DIPOL2026":
                    st.session_state.update({'autenticado': True, 'es_admin': True, 'agente_nombre': nombre if nombre else "Administrador"})
                    st.rerun()
                elif nombre and usuario and clave == "ESTUDIANTE2026":
                    st.session_state.update({'autenticado': True, 'es_admin': False, 'agente_nombre': nombre})
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas o campos vacíos.")

# 6. LÓGICA DE NAVEGACIÓN
if not st.session_state['autenticado']:
    login()
else:
    # BARRA LATERAL
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state['agente_nombre']}")
        st.write(f"Rol: {'🛡️ Administrador' if st.session_state['es_admin'] else '👮 Agente Operativo'}")
        st.divider()
        
        opciones = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso"]
        if st.session_state['es_admin']:
            opciones.append("📈 Dashboard General")
            
        seccion = st.radio("Navegación", opciones)
        
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    # --- CONTENIDO DE LAS SECCIONES ---
    if seccion == "🏠 Inicio":
        st.title("Bienvenido al Centro de Capacitación")
        st.info(f"Hola {st.session_state['agente_nombre']}, selecciona un módulo para comenzar.")

    elif seccion == "📊 Mi Progreso":
        st.markdown("<h1>📊 Mi Expediente</h1>", unsafe_allow_html=True)
        df = cargar_datos_agente(st.session_state['agente_nombre'])
        if not df.empty:
            c1, c2 = st.columns(2)
            c1.metric("Promedio", f"{df['nota'].mean():.1f}%")
            c2.metric("Evaluaciones", len(df))
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros aún.")

    elif seccion == "📈 Dashboard General":
        if st.session_state['es_admin']:
            st.title("📈 Dashboard Estratégico")
            df_all = cargar_todo_admin()
            if not df_all.empty:
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Agentes", df_all['funcionario'].nunique())
                m2.metric("Promedio Global", f"{df_all['nota'].mean():.1f}%")
                m3.metric("Exámenes Realizados", len(df_all))
                st.bar_chart(df_all.groupby('modulo')['nota'].mean())
        else:
            st.error("Área restringida.")
            
    if seccion == "🏠 Inicio":
        st.session_state['nav_index'] = 0
        
        # Encabezado de Bienvenida
        st.markdown(f"""
        <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
            <span style="color: white;">Bienvenido Agente: <b>{st.session_state['agente_nombre']}</b> | Estado: <span style="color: #4CAF50;">● En Línea</span></span>
        </div>
        """, unsafe_allow_html=True)

        # Definición de la estructura de Módulos para la Home
        modulos_home = [
            {"id": "M1", "tit": "Módulo 1", "sub": "Conceptualización", "icon": "📖", "full": "Módulo 1: Conceptualización"},
            {"id": "M2", "tit": "Módulo 2", "sub": "Ciclo de Inteligencia", "icon": "🔄", "full": "Módulo 2: Ciclo de Inteligencia"},
            {"id": "M3", "tit": "Módulo 3", "sub": "Recolección", "icon": "🕵️", "full": "Módulo 3: Recolección"},
            {"id": "M4", "tit": "Módulo 4", "sub": "Tratamiento", "icon": "📊", "full": "Módulo 4: Tratamiento"},
            {"id": "M5", "tit": "Módulo 5", "sub": "Análisis", "icon": "🧠", "full": "Módulo 5: Análisis"},
            {"id": "M6", "tit": "Módulo 6", "sub": "Comunicación", "icon": "📢", "full": "Módulo 6: Comunicación"},
            {"id": "M7", "tit": "Módulo 7", "sub": "Evaluación", "icon": "🔄", "full": "Módulo 7: Evaluación"}
        ]

        # Creación de la Grilla (3 columnas)
        cols = st.columns(3)
        for i, m in enumerate(modulos_home):
            with cols[i % 3]:
                # Diseño visual de la tarjeta
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #002147, #001226); 
                            padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; 
                            text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
                            min-height: 220px;">
                    <div style="font-size: 3em; margin-bottom: 10px;">{m['icon']}</div>
                    <h3 style="color: #D4AF37; margin: 0;">{m['tit']}</h3>
                    <p style="color: #ffffff; font-size: 0.9em; opacity: 0.8;">{m['sub']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botón funcional de ingreso
                if st.button(f"INGRESAR AL {m['id']}", key=f"btn_home_{m['id']}"):
                    st.session_state['modulo_activo'] = m['full']
                    st.session_state['nav_index'] = 1  # Forzamos el cambio de pestaña a "Módulos"
                    st.rerun()

    # --- SIGUIENTE SECCIÓN: MÓDULOS ---
    elif seccion == "📚 Módulos":
        st.session_state['nav_index'] = 1
        lista_modulos = [
            "Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", 
            "Módulo 3: Recolección", "Módulo 4: Tratamiento", 
            "Módulo 5: Análisis", "Módulo 6: Comunicación", "Módulo 7: Evaluación"
        ]
        
        try:
            idx_mod = lista_modulos.index(st.session_state['modulo_activo'])
        except ValueError:
            idx_mod = 0
            
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", lista_modulos, index=idx_mod)
        st.session_state['modulo_activo'] = modulo_selec

        st.divider()

        # --- MÓDULO 1: CONCEPTUALIZACIÓN ---
        if modulo_selec == "Módulo 1: Conceptualización":
            if not st.session_state.get('modo_examen', False):
                st.header("📖 Material: Conceptualización de Inteligencia")
                
                # Definición General con diseño destacado
                st.markdown("""
                    <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
                        <h3 style="color: #D4AF37; margin-top: 0;">¿Qué es Inteligencia?</h3>
                        <p style="color: white; font-size: 1.05em;">Es el <b>conocimiento obtenido</b> mediante el procesamiento de información para reducir la incertidumbre en la toma de decisiones.</p>
                        <ul style="color: #ecf0f1; font-size: 0.95em;">
                            <li>Es una actividad <b>multi y transdisciplinaria</b>.</li>
                            <li>Su función principal es el <b>asesoramiento</b> técnico.</li>
                            <li>Se diferencia del intelecto por enfocarse en <b>habilidades y aptitudes</b> ante situaciones concretas.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

                # Sección de Inteligencia Policial
                st.subheader("🛡️ Inteligencia Policial")
                st.info("""Conjunto de procesos para generar conocimiento relacionado con la **seguridad y convivencia ciudadana**, contribuyendo al diseño de estrategias institucionales y operaciones de la misión policial.""")

                # Inteligencia según su nivel (Diseño de tarjetas profesionales)
                st.markdown("### 📊 Niveles de Inteligencia")
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #3498db; height: 260px;">
                        <h4 style="color: #3498db; text-align: center;">Estratégica</h4>
                        <p style="color: white; font-size: 0.85em;">Utilizada por líderes políticos y policiales para formular <b>planes y políticas</b> nacionales a largo plazo.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #f1c40f; height: 260px;">
                        <h4 style="color: #f1c40f; text-align: center;">Operacional</h4>
                        <p style="color: white; font-size: 0.85em;">Planeamiento de operaciones en <b>áreas específicas</b>. Se concentra en localización y análisis de objetivos.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with c3:
                    st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #2ecc71; height: 260px;">
                        <h4 style="color: #2ecc71; text-align: center;">Táctica</h4>
                        <p style="color: white; font-size: 0.85em;">Requerida para la <b>conducción de equipos</b> en el terreno durante operaciones inmediatas.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()

                # Gestión de intentos
                try:
                    nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 1", engine)
                except:
                    nota_p = None

                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN M1"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: 
                    st.success(f"✅ Módulo completado. Calificación: {nota_p}%")

            else:
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
                        respuestas = [
                            q1 == "Asesoramiento para la toma de decisiones",
                            q2 == "Habilidades y aptitudes para manejar situaciones concretas",
                            q3 == "Seguridad y convivencia ciudadana",
                            q4 == "Estratégica",
                            q5 == "Conducción de operaciones a nivel de equipos"
                        ]
                        nota_m1 = (sum(respuestas) / len(respuestas)) * 100
                        try:
                            with engine.begin() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), 
                                           {"f": st.session_state['agente_nombre'], "n": nota_m1, "m": "Módulo 1"})
                        except:
                            st.error("Error al guardar en base de datos")
                        
                        st.session_state['modo_examen'] = False
                        st.rerun()
                        
        # --- MÓDULO 2: CICLO DE INTELIGENCIA ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            if not st.session_state.get('modo_examen', False):
                st.header("📖 Material: Ciclo de Inteligencia")
                
                st.markdown("""
                    <div class="lectura-box" style="border-left: 5px solid #D4AF37; margin-bottom: 20px;">
                        <h3 style="color: #D4AF37; margin-top: 0;">Definición Estratégica</h3>
                        <p style="color: white;">Es un proceso sistemático de <b>cinco pasos</b> orientado a la generación de conocimiento útil y veraz para un decisor final. Su objetivo es transformar datos brutos en inteligencia estratégica.</p>
                    </div>
                """, unsafe_allow_html=True)

                st.subheader("🔄 Las 5 Fases del Ciclo")
                
                
                # Diseño de flujo de proceso con tarjetas
                col_c1, col_c2 = st.columns(2)

                with col_c1:
                    st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #3498db; margin-bottom: 15px;">
                        <h4 style="color: #3498db; margin: 0;">1. Recolectar</h4>
                        <p style="color: #ecf0f1; font-size: 0.9em;">Obtención de la <b>información bruta</b> necesaria. Es la fase de búsqueda activa en el campo y bases de datos.</p>
                    </div>
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #9b59b6; margin-bottom: 15px;">
                        <h4 style="color: #9b59b6; margin: 0;">2. Tratar</h4>
                        <p style="color: #ecf0f1; font-size: 0.9em;">Procesamiento, registro y organización de los datos. Se traduce o decodifica la información para que sea legible.</p>
                    </div>
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #f1c40f; margin-bottom: 15px;">
                        <h4 style="color: #f1c40f; margin: 0;">3. Analizar</h4>
                        <p style="color: #ecf0f1; font-size: 0.9em;"><b>Fase crítica:</b> Transformación de datos en inteligencia mediante la valoración, integración e interpretación.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_c2:
                    st.markdown("""
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #2ecc71; margin-bottom: 15px;">
                        <h4 style="color: #2ecc71; margin: 0;">4. Comunicar e Integrar</h4>
                        <p style="color: #ecf0f1; font-size: 0.9em;">Difusión selectiva de los resultados al decisor mediante instrumentos formales (Informes de Inteligencia).</p>
                    </div>
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #e74c3c; margin-bottom: 15px;">
                        <h4 style="color: #e74c3c; margin: 0;">5. Evaluar y Retroalimentar</h4>
                        <p style="color: #ecf0f1; font-size: 0.9em;">Revisión constante para asegurar que el producto cumple con los requerimientos originales del destinatario.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("**Importante:** El ciclo es dinámico. Un fallo en la fase de 'Tratar' puede invalidar todo el análisis posterior.")

                st.divider()
                
                # Sistema de evaluación
                try:
                    nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 2", engine)
                except:
                    nota_p = None

                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN M2"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: 
                    st.success(f"✅ Módulo completado. Calificación obtenida: {nota_p}%")
            
            else:
                st.header("📝 Evaluación: Módulo 2")
                with st.form("exam_m2"):
                    m2_q1 = st.radio("1. ¿Cuál es el objetivo final del Ciclo de Inteligencia?", 
                        ["Solo recolectar datos", "Generar conocimiento útil para un decisor", "Realizar capturas"])
                    m2_q2 = st.radio("2. Fase donde la información bruta se transforma en inteligencia:", 
                        ["Recolectar", "Analizar", "Comunicar"])
                    m2_q3 = st.radio("3. ¿En qué consiste la fase de 'Tratar'?", 
                        ["Difundir el informe", "Procesamiento y organización de los datos", "Retroalimentar al jefe"])
                    m2_q4 = st.radio("4. ¿Cuál es el último paso del ciclo según el material?", 
                        ["Comunicar e Integrar", "Evaluar y Retroalimentar", "Tratar"])
                    m2_q5 = st.radio("5. ¿A quién se le difunde el resultado del ciclo?", 
                        ["Al público general", "Al destinatario final (Decisor)", "A todas las unidades"])

                    if st.form_submit_button("FINALIZAR EXAMEN"):
                        res_m2 = [
                            m2_q1 == "Generar conocimiento útil para un decisor",
                            m2_q2 == "Analizar",
                            m2_q3 == "Procesamiento y organización de los datos",
                            m2_q4 == "Evaluar y Retroalimentar",
                            m2_q5 == "Al destinatario final (Decisor)"
                        ]
                        nota_m2 = (sum(res_m2) / len(res_m2)) * 100
                        try:
                            with engine.begin() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), 
                                           {"f": st.session_state['agente_nombre'], "n": nota_m2, "m": "Módulo 2"})
                        except:
                            st.error("Error al guardar nota en DB")
                        
                        st.session_state['modo_examen'] = False
                        st.rerun()
                        
        # --- MÓDULO 3: RECOLECCIÓN DE INFORMACIÓN ---
        elif modulo_selec == "Módulo 3: Recolección":
            if not st.session_state.get('modo_examen', False):
                st.header("📖 Material Completo: Recolección de Información")
                t1, t2, t3, t4 = st.tabs(["📌 Fundamentos y PHVA", "🕵️ Operaciones", "👥 Fuentes Humanas", "🎤 La Entrevista"])
                
                with t1:
                    st.markdown("""
                    <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37;">
                        <h3 style="color: #D4AF37; margin-top: 0;">¿Qué es información?</h3>
                        <p style="color: white;">Es un conjunto de <b>datos integrados y ordenados</b> que sirven para construir un mensaje. Es la materia prima para resolver problemas y tomar decisiones.</p>
                        <p style="color: #D4AF37; font-weight: bold;">⚠️ El DATO es la unidad básica que comprende la información.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### El Ciclo PHVA en Recolección")
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.write("**🔵 PLANEAR:** Establecer objetivos, identificar riesgos y planificar recursos.")
                        st.write("**🟢 HACER:** Búsqueda de información, ejecutar actividades y elaborar productos.")
                    with col_p2:
                        st.write("**🟠 VERIFICAR:** Autoevaluación de control y gestión (seguimiento).")
                        st.write("**🔴 ACTUAR:** Implementar acciones correctivas o preventivas.")

                with t2:
                    st.subheader("🕵️ Operaciones de Inteligencia Policial")
                    
                    st.markdown("""
                        <div class="lectura-box" style="margin-bottom: 25px;">
                            <h4 style="color: #D4AF37; margin-top: 0;">Fines Operacionales</h4>
                            <p style="color: white; margin: 0;">Son actividades del servicio policial orientadas a la obtención de información privilegiada. Para toda operación se requiere el <b>Empleo y uso de Medios Técnicos</b>.</p>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.expander("🛠️ CLASIFICACIÓN OPERATIVA", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("""
                            <div class="ejemplo-box" style="border-left: 5px solid #4CAF50;">
                                <h3 style="color: #4CAF50;">Básicas</h3>
                                <ul style="color: white; font-size: 0.9em; line-height: 1.6;">
                                    <li><b>🔍 Reconocimiento:</b> Concretar y ampliar datos previos.</li>
                                    <li><b>✅ Verificación:</b> Establecer veracidad o desvirtuar.</li>
                                    <li><b>🔭 Vigilancia:</b> Observación continua y discreta (rutinas).</li>
                                    <li><b>🚗 Seguimiento:</b> Control sobre personas o elementos en movimiento.</li>
                                    <li><b>🗣️ Sonsacamiento:</b> Diálogo sutil e invisible.</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.markdown("""
                            <div class="ejemplo-box" style="border-left: 5px solid #ef6c00;">
                                <h3 style="color: #ef6c00;">Especializadas</h3>
                                <ul style="color: white; font-size: 0.9em; line-height: 1.6;">
                                    <li><b>👤 Admón. de F.H.:</b> Dirección y control de fuentes humanas cooperantes.</li>
                                    <li><b>🎙️ Entrevista:</b> Intercambio de ideas para obtener información específica.</li>
                                    <li><b>👥 Infiltración:</b> Ubicar agentes dentro de una organización mediante una cobertura.</li>
                                    <li><b>🔑 Penetración:</b> Obtener colaboración permanente de alguien con acceso.</li>
                                    <li><b>🎭 Caracterización y Fachada:</b> El rol y el entorno que lo respalda.</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.divider()

                with t3:
                    st.subheader("👥 Administración de Fuentes Humanas")
                    
                    st.markdown("""
                        <div class="lectura-box">
                            <h4 style="color: #D4AF37; margin-top: 0;">Fases del Proceso Operativo</h4>
                            <p style="color: white;">La administración de fuentes requiere un seguimiento riguroso para garantizar la fiabilidad de la información obtenida.</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Diseño de fases en columnas 2x2 para mayor claridad
                    f1, f2 = st.columns(2)
                    
                    with f1:
                        st.markdown("""
                        <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #3498db; height: 320px;">
                            <h4 style="color: #3498db;">1. Exploración</h4>
                            <p style="color: #bdc3c7; font-size: 0.9em;"><i>Búsqueda de fuentes</i></p>
                            <ul style="color: white; font-size: 0.9em;">
                                <li><b>Búsqueda:</b> Localización activa.</li>
                                <li><b>Forma voluntaria:</b> Presentación espontánea.</li>
                                <li><b>Evaluación y motivación:</b> Análisis de intereses.</li>
                                <li><b>Selección preliminar:</b> Filtrado inicial.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("") # Espaciador
                        
                        st.markdown("""
                        <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #e74c3c; height: 200px;">
                            <h4 style="color: #e74c3c;">3. Registro</h4>
                            <p style="color: #bdc3c7; font-size: 0.9em;"><i>Ingresar la fuente en:</i></p>
                            <ul style="color: white; font-size: 0.9em;">
                                <li>Sistema de Administración de Fuentes Humanas (Oficial).</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                    with f2:
                        st.markdown("""
                        <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #f1c40f; height: 320px;">
                            <h4 style="color: #f1c40f;">2. Aproximación</h4>
                            <p style="color: #bdc3c7; font-size: 0.9em;"><i>Establecimiento de contacto</i></p>
                            <ul style="color: white; font-size: 0.9em;">
                                <li><b>La Entrevista:</b> Primer contacto formal.</li>
                                <li><b>Sonsacamiento:</b> Técnica de obtención sutil.</li>
                                <li><b>Evaluación:</b> Calificación de acceso y credibilidad.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("") # Espaciador

                        st.markdown("""
                        <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #2ecc71; height: 200px;">
                            <h4 style="color: #2ecc71;">4. Entrenamiento</h4>
                            <p style="color: #bdc3c7; font-size: 0.9em;"><i>Preparar la fuente</i></p>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; color: white; font-size: 0.9em;">
                                <div>• Instruir</div>
                                <div>• Orientar</div>
                                <div>• Dirigir</div>
                                <div>• Controlar</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.divider()

                with t4:
                    st.subheader("🎤 La Entrevista de Inteligencia")
                    
                    st.markdown("""
                        <div class="lectura-box" style="border-left: 5px solid #e74c3c;">
                            <h4 style="color: #e74c3c; margin-top: 0;">Tipos de Entrevistador a EVITAR</h4>
                            <p style="color: white;">Procedimiento utilizado para la obtención de información de una fuente humana, mediante el intercambio de ideas y la correcta formulación de preguntas por el agente de inteligencia. Para una recolección efectiva, el entrevistador debe mantener el equilibrio y el control. Evite caer en los siguientes perfiles:</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Diseño en rejilla para los perfiles
                    col_e1, col_e2 = st.columns(2)

                    with col_e1:
                        st.markdown("""
                        <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #D4AF37;">
                            <h5 style="color: #D4AF37; margin: 0;">🌟 El Estrella</h5>
                            <p style="color: #ecf0f1; font-size: 0.85em;">Se siente superior a la fuente, habla más que él, lo interrumpe, hace largas preguntas y utiliza un lenguaje rebuscado.</p>
                        </div>
                        <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #D4AF37;">
                            <h5 style="color: #D4AF37; margin: 0;">🏃 El Improvisado</h5>
                            <p style="color: #ecf0f1; font-size: 0.85em;">Hace su trabajo desordenado y a la carrera. No prepara nada, pues confía ciegamente en su capacidad de improvisar.</p>
                        </div>
                        <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #D4AF37;">
                            <h5 style="color: #D4AF37; margin: 0;">🌀 El Enredado</h5>
                            <p style="color: #ecf0f1; font-size: 0.85em;">Le da muchas vueltas a un tema, usa palabras difíciles y complejas que confunden la comunicación.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_e2:
                        st.markdown("""
                        <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #D4AF37;">
                            <h5 style="color: #D4AF37; margin: 0;">📉 El Estrellado</h5>
                            <p style="color: #ecf0f1; font-size: 0.85em;">Se siente menos que la fuente, es tímido, de voz baja, permite hablar largo rato sin orientar y deja desviar el tema.</p>
                        </div>
                        <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #D4AF37;">
                            <h5 style="color: #D4AF37; margin: 0;">🔇 El Sordo</h5>
                            <p style="color: #ecf0f1; font-size: 0.85em;">Se preocupa demasiado por su cuestionario o por el entorno y olvida lo esencial: escuchar a la fuente.</p>
                        </div>
                        <div style="background-color: #262626; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #D4AF37;">
                            <h5 style="color: #D4AF37; margin: 0;">🔫 El Metralleta</h5>
                            <p style="color: #ecf0f1; font-size: 0.85em;">La fuente no tiene tiempo de responder porque el entrevistador ya le está sugiriendo la siguiente pregunta.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.info("**Nota Técnica:** El éxito de la entrevista radica en el **Rapport** (establecimiento de sintonía) y la escucha activa.")
                    st.divider()
                # Verifica si la función verificar_intento existe en tu código base
                try:
                    nota_p = verificar_intento(st.session_state['agente_nombre'], "Módulo 3", engine)
                except:
                    nota_p = None

                if nota_p is None:
                    if st.button("🚀 INICIAR EXAMEN MÓDULO 3"):
                        st.session_state['modo_examen'] = True
                        st.rerun()
                else: 
                    st.warning(f"Examen completado. Calificación: {nota_p}%")
            
            else:
                st.header("📝 Evaluación: Módulo 3")
                with st.form("exam_m3"):
                    q1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Vigilancia fija"])
                    q2 = st.radio("2. En PHVA, ¿qué implica la etapa HACER?", ["Planificar recursos", "Búsqueda de información y ejecución", "Acciones preventivas"])
                    q3 = st.radio("3. Diferencia entre Infiltración y Penetración:", ["No hay diferencia", "Infiltración mete al agente; Penetración usa a alguien de adentro", "Infiltración es solo técnica"])
                    q4 = st.radio("4. ¿Cuál es la unidad básica que comprende la información?", ["El mensaje", "El dato", "El informe"])
                    q5 = st.radio("5. ¿Qué busca el Reconocimiento?", ["Solo vigilar", "Concretar datos de inmuebles, seguridad y entorno", "Sonsacar a la fuente"])

                    if st.form_submit_button("FINALIZAR EXAMEN"):
                        respuestas = [
                            q1 == "Diálogo donde la fuente no debe percatarse de la explotación",
                            q2 == "Búsqueda de información y ejecución",
                            q3 == "Infiltración mete al agente; Penetración usa a alguien de adentro",
                            q4 == "El dato",
                            q5 == "Concretar datos de inmuebles, seguridad y entorno"
                        ]
                        nota_m3 = (sum(respuestas) / len(respuestas)) * 100
                        # Guardar en base de datos (asegúrate de que 'engine' esté definido)
                        try:
                            with engine.begin() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), 
                                           {"f": st.session_state['agente_nombre'], "n": nota_m3, "m": "Módulo 3"})
                        except:
                            st.write(f"Tu nota es: {nota_m3}% (Error al guardar en DB)")
                        
                        st.session_state['modo_examen'] = False
                        st.rerun()
                        
        # --- MÓDULO 4: TRATAMIENTO DE LA INFORMACIÓN (CONTENIDO COMPLETO) ---
        elif modulo_selec == "Módulo 4: Tratamiento":
            if not st.session_state.get('modo_examen', False):
                st.header("📖 Material: Tratamiento de la Información")
                
                # SISTEMA DE CUATRO PESTAÑAS - TODO INCLUIDO
                tab_cont, tab_tipos, tab_comp, tab_4x4 = st.tabs([
                    "📌 Fundamentos", 
                    "🔍 Tipos y Elementos (EEI)", 
                    "🛠️ Componentes", 
                    "📊 Código 4x4"
                ])
                
                with tab_cont:
                    st.markdown("""
                    <div style="background-color: #002147; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
                        <h3 style="color: #D4AF37; margin-top: 0;">Definición</h3>
                        <p style="color: white;">Procedimiento <b>sistemático</b> que consiste en someter todos los datos e información recolectada a un proceso de organización, clasificación y valoración preliminar, con el fin de garantizar que su registro y almacenamiento en bases de datos se enmarque en los fines de la actividad de inteligencia y contrainteligencia contenidos en la <b>Constitución y la Jurisprudencia nacional</b>.</p>
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
                    <div style="background-color: #003366; border: 2px solid #D4AF37; padding: 15px; border-radius: 10px; text-align: center;">
                        <h3 style="color: white; margin-bottom: 10px;">Ecuación de Tratamiento</h3>
                        <h2 style="color: #D4AF37; margin-top: 0;">Información + Conocimiento = Decisión</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with tab_tipos:
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.markdown("""
                        <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; min-height: 350px;">
                            <h4 style="color: #D4AF37;">💡 Tipos de Información</h4>
                            <p style="color: #ccc;"><b>1. Genérica:</b> Información de contexto que ayuda a entender el entorno general sin un objetivo inmediato.</p>
                            <p style="color: #ccc;"><b>2. Específica:</b> Información puntual y detallada sobre un blanco o fenómeno, necesaria para decisiones tácticas.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_t2:
                        st.markdown("""
                        <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; min-height: 350px;">
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
                        </div>
                        """, unsafe_allow_html=True)

                with tab_comp:
                    st.subheader("⚙️ Componentes del Tratamiento")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write("**📂 ORGANIZACIÓN**")
                        st.caption("Determinar tipo de información, blanco y nivel de prioridad.")
                        st.write("**🛡️ CLASIFICACIÓN**")
                        st.caption("Origen de la fuente, estado del proceso y nivel de seguridad (Secreto/Reservado).")
                    with c2:
                        st.write("**⚖️ VALORACIÓN**")
                        st.caption("Evaluar si es oportuna, confiable y creíble.")
                        st.write("**📝 REGISTRO**")
                        st.caption("Ingreso cronológico, detallado y sistemático en bases de datos.")

                with tab_4x4:
                    st.subheader("📋 Matriz de Evaluación 4x4")
                    st.markdown("""
                    <style>
                        .t-4x4 { width: 100%; border-collapse: collapse; color: white; }
                        .t-4x4 th { background-color: #D4AF37; color: #000; padding: 8px; border: 1px solid #444; }
                        .t-4x4 td { padding: 8px; border: 1px solid #444; background-color: #002b55; font-size: 0.85em; }
                        .cod-cell { text-align: center; font-weight: bold; background-color: #003366 !important; width: 40px; }
                        .perc-100 { background-color: #2e7d32 !important; text-align: center; font-weight: bold; }
                        .perc-75 { background-color: #fbc02d !important; text-align: center; font-weight: bold; color: black; }
                        .perc-50 { background-color: #ef6c00 !important; text-align: center; font-weight: bold; }
                        .perc-25 { background-color: #c62828 !important; text-align: center; font-weight: bold; }
                    </style>
                    <table class="t-4x4">
                        <tr>
                            <th colspan="2">CONFIABILIDAD (FUENTE)</th>
                            <th colspan="2">CREDIBILIDAD (INFO)</th>
                            <th>%</th>
                        </tr>
                        <tr><td class="cod-cell">A</td><td>Totalmente confiable</td><td class="cod-cell">1</td><td>Confirmada/Cierta</td><td class="perc-100">100</td></tr>
                        <tr><td class="cod-cell">B</td><td>Usualmente confiable</td><td class="cod-cell">2</td><td>De primera mano</td><td class="perc-75">75</td></tr>
                        <tr><td class="cod-cell">C</td><td>Dudosa/No confiable</td><td class="cod-cell">3</td><td>Corroborable</td><td class="perc-50">50</td></tr>
                        <tr><td class="cod-cell">D</td><td>Desconocida/Sin historial</td><td class="cod-cell">4</td><td>No corroborable</td><td class="perc-25">25</td></tr>
                    </table>
                    """, unsafe_allow_html=True)
                    
                    # Ejemplos visuales rápidos
                    st.markdown("---")
                    col_ex1, col_ex2 = st.columns(2)
                    with col_ex1:
                        st.success("**Ejemplo A-1 (100%):** Agente infiltrado entrega grabación original.")
                    with col_ex2:
                        st.error("**Ejemplo D-4 (25%):** Llamada anónima con datos imposibles de verificar.")

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 4"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            
            else:
                st.header("📝 Evaluación: Módulo 4")
                with st.form("exam_m4"):
                    m4_1 = st.radio("1. ¿Qué implica la etapa de 'Organización'?", 
                                   ["Captura de objetivos", "Determinar tipo de información, blanco y prioridad", "Publicar en redes sociales"])
                    m4_2 = st.radio("2. Según la matriz 4x4, el código 'C-3' representa un porcentaje de:", 
                                   ["100%", "75%", "50%"])
                    m4_3 = st.radio("3. El Tratamiento busca garantizar que el registro se enmarque en:", 
                                   ["Revistas de prensa", "La Constitución y la Jurisprudencia nacional", "Manuales de software"])
                    m4_4 = st.radio("4. ¿Qué elemento de los EEI responde al 'Por qué'?", 
                                   ["Temporalidad", "Causas y motivaciones", "Ubicación"])
                    m4_5 = st.radio("5. ¿Cuál es el producto final tras someter la Información al Proceso?", 
                                   ["Datos crudos", "Inteligencia", "Insumos"])

                    if st.form_submit_button("FINALIZAR EXAMEN"):
                        res_m4 = [
                            m4_1 == "Determinar tipo de información, blanco y prioridad",
                            m4_2 == "50%",
                            m4_3 == "La Constitución y la Jurisprudencia nacional",
                            m4_4 == "Causas y motivaciones",
                            m4_5 == "Inteligencia"
                        ]
                        nota_m4 = (sum(res_m4) / 5) * 100
                        # Aquí asumo que tienes tu conexión 'engine' configurada
                        try:
                            with engine.begin() as conn:
                                conn.execute(text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)"), 
                                           {"f": st.session_state['agente_nombre'], "n": nota_m4, "m": "Módulo 4"})
                            st.success(f"Examen enviado. Nota: {nota_m4}%")
                        except:
                            st.warning(f"Calificación calculada: {nota_m4}%. (Error de conexión a DB)")
                        
                        st.session_state['modo_examen'] = False
                        st.rerun()

        # --- MÓDULO 5: ANÁLISIS DE LA INFORMACIÓN (CONTENIDO COMPLETO) ---
        elif modulo_selec == "Módulo 5: Análisis":
            if not st.session_state.get('modo_examen', False):
                st.header("🧠 Material: Análisis de la Información")
                
                # PESTAÑAS DEL MÓDULO 5
                tab_estudio, tab_proceso, tab_lca, tab_sintesis = st.tabs([
                    "🔬 Estudio Especializado", 
                    "🧩 Proceso de Análisis", 
                    "⏳ Línea LCA",
                    "💡 Síntesis y Resultados"
                ])
                
                with tab_estudio:
                    st.subheader("Estudio Especializado de la Información")
                    st.write("El análisis es un proceso cuyo objeto es **generar conocimiento**, con base en la información disponible.")
                    
                    # Representación visual del flujo
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
                    3. **Hipótesis:** Plantear suposiciones técnicas fundamentadas.
                    4. **Conclusiones:** Resultados finales derivados del razonamiento.
                    """)

                with tab_proceso:
                    st.subheader("🧩 El Proceso Analítico (Descomposición)")
                    
                    # Panel Superior de Actividades
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
                        st.markdown('<div style="text-align:center; background:#f2dede; padding:15px; border-radius:10px; min-height:180px; color:#a94442;">'
                                    '<h3>EL TODO</h3>🧩<br><small>Objeto de análisis completo. Búsqueda de tendencias y patrones generales.</small></div>', unsafe_allow_html=True)
                    with col_f2:
                        st.markdown('<div style="text-align:center; background:#fcf8e3; padding:15px; border-radius:10px; min-height:180px; color:#8a6d3b;">'
                                    '<h3>ANALIZAR</h3>🔍<br><small>Descomponer. Identificar cada elemento individual que modifica el patrón.</small></div>', unsafe_allow_html=True)
                    with col_f3:
                        st.markdown('<div style="text-align:center; background:#d9edf7; padding:15px; border-radius:10px; min-height:180px; color:#31708f;">'
                                    '<h3>SINTETIZAR</h3>💡<br><small>Recomponer. Entender el nuevo significado de las partes sumadas.</small></div>', unsafe_allow_html=True)
                    st.caption("Analizar es descomponer el todo; sintetizar es recomponer para entender el significado final.")

                with tab_lca:
                    st.subheader("⏳ LCA: Línea del Conocimiento Analítico")
                    
                    st.markdown("""
                    <div style="display: flex; justify-content: space-around; align-items: center; background: linear-gradient(90deg, #2c5d63, #c0392b, #f39c12); padding: 30px; border-radius: 15px; color: white; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                        <div style="text-align: center;">PASADO<br><span style="font-weight:normal; font-size:0.8em;">Antecedentes<br>Memoria Histórica</span></div>
                        <div style="font-size: 2em;">➔</div>
                        <div style="text-align: center; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px;">PRESENTE<br><span style="font-weight:normal; font-size:0.8em;">Situación Actual<br>Interpretación</span></div>
                        <div style="font-size: 2em;">➔</div>
                        <div style="text-align: center;">FUTURO<br><span style="font-weight:normal; font-size:0.8em;">Proyección<br>Prospectiva</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("La LCA permite transformar la memoria histórica en proyecciones mediante la interpretación técnica del presente.")

                with tab_sintesis:
                    st.subheader("🎯 Resultados y Cursos de Acción")
                    st.markdown("""
                    El análisis genera conocimiento estratégico para:
                    * **Formular Hipótesis:** Suposiciones basadas en datos técnicos y evidencia recolectada.
                    * **Definir Escenarios:** Identificar las posibles evoluciones de un fenómeno criminal o social.
                    * **Cursos de Acción:** Recomendaciones específicas para que el mando tome decisiones acertadas.
                    """)
                    st.warning("⚠️ Sin una síntesis clara que oriente la acción, la inteligencia pierde su valor operativo.")

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 5"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.subheader("📝 Examen de Conocimientos - M5")
                # Espacio para el formulario de examen
                if st.button("⬅️ Volver al Material"):
                    st.session_state['modo_examen'] = False
                    st.rerun()
                    
        # --- MÓDULO 6: COMUNICAR E INTEGRAR (CONTENIDO COMPLETO) ---
        elif modulo_selec == "Módulo 6: Comunicación":
            if not st.session_state.get('modo_examen', False):
                st.header("📢 Material: Comunicar e Integrar")
                
                # Introducción breve
                st.info("La inteligencia no sirve si no llega a quien debe tomar la decisión en el momento oportuno.")

                tab_pasos, tab_ejemplos, tab_seguridad = st.tabs([
                    "🚀 Pasos para la Difusión", 
                    "📝 Casos Prácticos", 
                    "🔐 Seguridad en Entrega"
                ])
                
                with tab_pasos:
                    st.subheader("Procedimiento Estándar de Difusión")
                    
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
                        <div style="background-color: #001a33; padding: 20px; border-radius: 10px; border: 1px solid #444; min-height: 250px;">
                            <h4 style="color: #D4AF37;">Ejemplo A: Canal Virtual</h4>
                            <p style="font-size: 0.9em; color: white;">
                            <b>Escenario:</b> Envío de reporte diario de criminalidad.<br><br>
                            <b>Acción:</b> Se utiliza el e-mail institucional con un archivo PDF protegido por contraseña y cifrado PGP. <br><br>
                            <b>Registro:</b> Se guarda el LOG de envío en el sistema centralizado.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div style="background-color: #001a33; padding: 20px; border-radius: 10px; border: 1px solid #444; min-height: 250px;">
                            <h4 style="color: #D4AF37;">Ejemplo B: Entrega Exclusiva</h4>
                            <p style="font-size: 0.9em; color: white;">
                            <b>Escenario:</b> Orden de captura para blanco de alto valor.<br><br>
                            <b>Acción:</b> Entrega en sobre sellado con cinta de seguridad directamente al Director de Inteligencia.<br><br>
                            <b>Registro:</b> Firma obligatoria en la planilla de difusión física.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_seguridad:
                    st.subheader("Medidas de Protección del Producto")
                    
                    st.markdown("""
                    <div style="background-color: #0e1117; padding: 20px; border: 1px dashed #D4AF37; border-radius: 10px;">
                        <ul style="color: white; line-height: 1.8;">
                            <li><b>Clasificación:</b> Marcar claramente como <b>RESERVADO</b> o <b>SECRETO</b> según la ley.</li>
                            <li><b>Encriptación:</b> Uso de algoritmos para proteger datos digitales (Cifrado de disco o archivos).</li>
                            <li><b>Embalaje:</b> Uso de sobres de seguridad que evidencien manipulación física.</li>
                            <li><b>Codificación:</b> Uso de lenguaje convenido o alias para evitar lectura de terceros no autorizados.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 6"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.subheader("📝 Examen de Conocimientos - M6")
                # Aquí puedes insertar el st.form con las preguntas
                if st.button("⬅️ Volver al Material"):
                    st.session_state['modo_examen'] = False
                    st.rerun()

        elif modulo_selec == "Módulo 7: Evaluación":
            # Aquí va todo tu contenido del Módulo 7 que pasaste antes
            if not st.session_state.get('modo_examen', False):
                st.header("🔄 Material: Evaluar y Retroalimentar")
                
                st.markdown("""
                <div style="background: linear-gradient(90deg, #002147 0%, #003366 100%); padding: 25px; border-radius: 15px; border-right: 5px solid #D4AF37; margin-bottom: 25px;">
                    <h3 style="color: #D4AF37; margin-top: 0;">🎯 Objetivo de la Fase</h3>
                    <p style="color: white; font-size: 1.1em;">
                        Evaluar el impacto del <b>Plan Nacional (PNIP)</b>, <b>Planes Regionales</b> y los productos de inteligencia, 
                        asegurando que los responsables del ciclo identifiquen oportunidades reales de mejoramiento del servicio.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                tab_act, tab_sinai, tab_ejemplos = st.tabs(["⚙️ Actividades Clave", "📊 Trazabilidad y Análisis", "📝 Casos de Evaluación"])

                with tab_act:
                    st.subheader("Ruta Crítica de Evaluación")
                    actividades = [
                        "1. Planificar y programar la evaluación.",
                        "2. Realizar trazabilidad en SINAI.",
                        "3. Seleccionar productos para rastreo.",
                        "4. Trazabilidad de los planes de inteligencia.",
                        "5. Analizar el impacto decisional."
                    ]
                    for act in actividades:
                        st.markdown(f'<div style="background-color: #0e1117; padding: 12px; border-radius: 8px; border: 1px solid #444; margin-bottom: 8px; color: #D4AF37; font-weight: bold;">{act}</div>', unsafe_allow_html=True)

                with tab_sinai:
                    st.subheader("Trazabilidad en SINAI")
                    st.info("La trazabilidad no es solo archivo; es el rastreo de acciones y decisiones tomadas basadas en nuestra inteligencia.")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="lectura-box"><h4 style="color: #D4AF37;">¿Qué evaluamos?</h4><ul><li><b>Pertinencia:</b> ¿Respondió al requerimiento?</li><li><b>Oportunidad:</b> ¿Llegó a tiempo?</li><li><b>Exactitud:</b> ¿Fue veraz?</li></ul></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown('<div class="lectura-box"><h4 style="color: #D4AF37;">Impacto Decisional</h4><p>Se mide si el producto generó una acción concreta: una captura, una desarticulación, o un cambio en la política de seguridad regional.</p></div>', unsafe_allow_html=True)

                with tab_ejemplos:
                    st.subheader("Ejemplos de Retroalimentación")
                    st.markdown("""
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div class="ejemplo-box" style="border-left: 4px solid #4CAF50;">
                            <h4 style="color: #4CAF50;">✅ Evaluación Positiva</h4>
                            <p style="color: white; font-size: 0.9em;"><b>Decisión:</b> El mando ordena intervención relámpago.<br><b>Resultado:</b> 5 capturas. Se felicita al equipo por la precisión geográfica.</p>
                        </div>
                        <div class="ejemplo-box" style="border-left: 4px solid #F44336;">
                            <h4 style="color: #F44336;">⚠️ Oportunidad de Mejora</h4>
                            <p style="color: white; font-size: 0.9em;"><b>Hallazgo:</b> El informe llegó 15 días tarde.<br><b>Acción:</b> Reajustar los tiempos de tratamiento para el próximo ciclo.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 7"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.subheader("📝 Examen Módulo 7 en curso...")
                if st.button("⬅️ Volver al Material"):
                    st.session_state['modo_examen'] = False
                    st.rerun()

    elif seccion == "📊 Mi Progreso":
        st.markdown(f"""
            <div style="background: linear-gradient(90deg, #001f3f 0%, #003366 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #D4AF37; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                <h1 style="color: white; margin: 0; font-family: sans-serif;">📊 Mi Expediente Académico</h1>
                <p style="color: #D4AF37; margin: 5px 0 0 0; font-weight: bold; font-size: 1.1em;">Agente: {st.session_state['agente_nombre']}</p>
            </div>
        """, unsafe_allow_html=True)

        try:
            # Intentar cargar datos
            df = cargar_datos_agente(st.session_state['agente_nombre'])
            
            if not df.empty:
                promedio = df['nota'].mean()
                
                # --- ESTILOS DE MÉTRICAS GRANDES ---
                st.markdown("""
                    <style>
                    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 3.5rem !important; font-weight: 900 !important; }
                    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
                    </style>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Mi Promedio", f"{promedio:.1f}%")
                with col2:
                    st.metric("Evaluaciones", len(df))

                st.write("---")
                
                # Tabla Pro con Progress Bar
                st.dataframe(
                    df,
                    column_config={
                        "nota": st.column_config.ProgressColumn("Nota Final", format="%d%%", min_value=0, max_value=100),
                        "modulo": "Módulo",
                        "fecha": "Fecha"
                    },
                    use_container_width=True, hide_index=True
                )
            else:
                st.info("Aún no hay evaluaciones registradas para este agente.")

        except Exception as e:
            # Esto te dirá el error real si vuelve a fallar
            st.error(f"Error técnico de conexión: {e}")
            st.warning("Asegúrate de que la variable 'engine' esté definida al inicio del script.")
            
    elif seccion == "📈 Dashboard General":
        if st.session_state.get('es_admin', False):
            # Título con estilo institucional y profesional
            st.markdown("""
                <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-bottom: 4px solid #D4AF37; margin-bottom: 25px;">
                    <h1 style="color: white; margin: 0;">🛡️ Centro de Inteligencia Analítica</h1>
                    <p style="color: #D4AF37; margin: 0; font-weight: bold;">Panel de Control y Rendimiento Académico - DIPOL</p>
                </div>
            """, unsafe_allow_html=True)
            
            try:
                with engine.begin() as conn:
                    query = text("SELECT funcionario, modulo, nota, fecha FROM calificaciones")
                    df_all = pd.read_sql(query, conn)
                
                if not df_all.empty:
                    df_all['fecha'] = pd.to_datetime(df_all['fecha']).dt.strftime('%Y-%m-%d %H:%M')
                    
                    # --- MÉTRICAS KPI (Key Performance Indicators) ---
                    promedio = df_all['nota'].mean()
                    total_eval = len(df_all)
                    aprobados = len(df_all[df_all['nota'] >= 70])
                    porcentaje_exito = (aprobados / total_eval) * 100

                    # --- DISEÑO DE TARJETAS PRO (TAMAÑO MAXIMIZADO) ---
                    st.markdown("""
                        <style>
                        .metric-card {
                            background: linear-gradient(145deg, #0d1117, #161b22);
                            border: 1px solid #30363d;
                            border-top: 4px solid #D4AF37;
                            border-radius: 15px;
                            padding: 25px 10px;
                            text-align: center;
                            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
                            transition: transform 0.3s ease;
                        }
                        .metric-card:hover {
                            transform: scale(1.02);
                            box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
                        }
                        .metric-title {
                            color: #8b949e;
                            font-size: 1rem;
                            font-weight: bold;
                            text-transform: uppercase;
                            letter-spacing: 1.5px;
                            margin-bottom: 15px;
                        }
                        .metric-value {
                            color: #D4AF37;
                            font-size: 3.5rem; /* Tamaño aumentado */
                            font-weight: 900;
                            margin: 0;
                            font-family: 'Arial Black', Gadget, sans-serif;
                            text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.markdown(f'<div class="metric-card"><p class="metric-title">Evaluaciones</p><p class="metric-value">{total_eval}</p></div>', unsafe_allow_html=True)
                    with m2:
                        st.markdown(f'<div class="metric-card"><p class="metric-title">Promedio</p><p class="metric-value">{promedio:.1f}%</p></div>', unsafe_allow_html=True)
                    with m3:
                        color_tasa = "#2ecc71" if porcentaje_exito >= 70 else "#e74c3c"
                        st.markdown(f'<div class="metric-card"><p class="metric-title">Tasa Éxito</p><p class="metric-value" style="color: {color_tasa};">{porcentaje_exito:.1f}%</p></div>', unsafe_allow_html=True)
                    with m4:
                        st.markdown(f'<div class="metric-card"><p class="metric-title">Agentes</p><p class="metric-value">{df_all["funcionario"].nunique()}</p></div>', unsafe_allow_html=True)

                    # --- PESTAÑAS DE ANÁLISIS ---
                    tab_rend, tab_detalles = st.tabs(["📊 Análisis de Rendimiento", "🔍 Detalle por Agente"])

                    with tab_rend:
                        c1, c2 = st.columns([1.2, 0.8])
                        
                        with c1:
                            st.subheader("Promedio por Componente Educativo")
                            chart_data = df_all.groupby('modulo')['nota'].mean().reset_index()
                            # Gráfico de barras con color institucional
                            st.bar_chart(data=chart_data, x='modulo', y='nota', color="#D4AF37", use_container_width=True)
                        
                        with c2:
                            st.subheader("Distribución de Calificaciones")
                            # Clasificación de desempeño
                            bins = [0, 69, 89, 100]
                            labels = ['Insuficiente (0-69)', 'Satisfactorio (70-89)', 'Sobresaliente (90-100)']
                            df_all['Nivel'] = pd.cut(df_all['nota'], bins=bins, labels=labels)
                            dist_data = df_all['Nivel'].value_counts()
                            st.bar_chart(dist_data, color="#2ecc71")

                    with tab_detalles:
                        col_filtro, col_descarga = st.columns([3, 1])
                        with col_filtro:
                            search = st.text_input("🔍 Buscar funcionario...", placeholder="Ingrese nombre para filtrar")
                        with col_descarga:
                            st.write("📄 **Reportes**")
                            csv = df_all.to_csv(index=False).encode('utf-8')
                            st.download_button("Descargar CSV", data=csv, file_name='reporte_dipol.csv', use_container_width=True)

                        # Aplicar filtro de búsqueda si existe
                        display_df = df_all.copy()
                        if search:
                            display_df = display_df[display_df['funcionario'].str.contains(search, case=False)]
                        
                        # Tabla con barras de progreso para las notas
                        st.dataframe(
                            display_df.sort_values(by='fecha', ascending=False),
                            column_config={
                                "nota": st.column_config.ProgressColumn("Calificación", format="%d%%", min_value=0, max_value=100),
                                "fecha": "Fecha",
                                "funcionario": "Agente",
                                "modulo": "Módulo"
                            },
                            use_container_width=True,
                            hide_index=True
                        )

                    # --- ALERTAS DE SEGUIMIENTO ---
                    st.divider()
                    low_performers = df_all[df_all['nota'] < 70]
                    if not low_performers.empty:
                        with st.expander("⚠️ Alerta: Personal con necesidad de refuerzo"):
                            st.warning(f"Se identificaron {len(low_performers)} intentos fallidos. Se recomienda capacitación adicional para estos funcionarios.")
                            st.table(low_performers[['funcionario', 'modulo', 'nota']])

                else:
                    st.info("ℹ️ No hay registros en la base de datos para generar el análisis.")

            except Exception as e:
                st.error(f"❌ Error crítico en el Dashboard: {e}")
        else:
            st.error("🚫 Acceso Denegado: Esta sección requiere credenciales de Administrador.")
