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
    .highlight { color: #D4AF37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'modo_examen' not in st.session_state:
    st.session_state['modo_examen'] = False

def login():
    st.markdown("<h1 style='text-align: center;'>🛡️ SISTEMA DE CAPACITACIÓN DIPOL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER"):
            if usuario == "admin" and clave == "DIPOL2026":
                st.session_state['autenticado'] = True
                st.rerun()
            else: st.error("Acceso Denegado")

# 3. INTERFAZ OPERATIVA
if not st.session_state['autenticado']:
    login()
else:
    db_s = st.secrets["connections"]["postgresql"]
    pass_segura = quote_plus(db_s['password'])
    engine = create_engine(f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}", pool_pre_ping=True)

    with st.sidebar:
        st.title("📂 MENÚ")
        seccion = st.radio("Ir a:", ["🏠 Inicio", "📚 Módulos", "📊 Progreso"])
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.session_state['modo_examen'] = False
            st.rerun()

    if seccion == "🏠 Inicio":
        st.title("Bienvenido al Panel Académico")
        st.write("Seleccione 'Módulos' en el menú lateral para comenzar su formación técnica.")

    elif seccion == "📚 Módulos":
        st.title("📚 Módulos de Especialización")
        
        seleccion = st.selectbox("Seleccione un Módulo:", [
            "Módulo 1: Conceptualización de Inteligencia",
            "Módulo 2: Redes y Comunicaciones",
            "Módulo 3: Inteligencia de Fuentes Abiertas",
            "Módulo 4: Análisis de Riesgos",
            "Módulo 5: Protocolo TLS/SSL",
            "Módulo 6: Ética y Ciberseguridad"
        ])

        st.divider()

        if seleccion == "Módulo 1: Conceptualización de Inteligencia":
            
            # --- VISTA DE LECTURA ---
            if not st.session_state['modo_examen']:
                st.header("📖 Material de Lectura: Conceptualización de Inteligencia")
                
                with st.container():
                    st.markdown(f"""
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
                
                if st.button("🚀 INICIAR EVALUACIÓN"):
                    st.session_state['modo_examen'] = True
                    st.rerun()

            # --- VISTA DE EXAMEN ---
            else:
                st.header("📝 Evaluación Final: Módulo 1")
                st.warning("⚠️ El contenido ha sido ocultado para la evaluación. Responda con cuidado.")
                
                if st.button("⬅️ Volver a Material de Lectura"):
                    st.session_state['modo_examen'] = False
                    st.rerun()

                with st.form(key="form_mod1_completo"):
                    p1 = st.radio("1. ¿Cuál es la función principal de la inteligencia según la definición dada?", 
                                  ["Generar incertidumbre", "Asesoramiento proporcionando conocimiento integrado que reduzca incertidumbres", "Ejecutar acciones de fuerza"])
                    
                    p2 = st.radio("2. ¿Qué nivel de inteligencia se orienta hacia los objetivos nacionales y el bienestar de la nación?", 
                                  ["Inteligencia Estratégica", "Inteligencia Operacional", "Inteligencia Táctica"])
                    
                    p3 = st.radio("3. ¿Cuál nivel de inteligencia se enfoca en las posibilidades inmediatas y dinámicas de un objetivo?", 
                                  ["Inteligencia Operacional", "Inteligencia Estratégica", "Inteligencia Táctica"])
                    
                    p4 = st.radio("4. Según el texto, ¿por qué la inteligencia se diferencia del intelecto?", 
                                  ["Porque es más compleja", "Por el hincapié en habilidades para manejar situaciones concretas y la experiencia sensorial", "No hay diferencia alguna"])
                    
                    p5 = st.radio("5. ¿Cuál es el objetivo primordial de la Inteligencia Policial?", 
                                  ["Registrar datos históricos", "Generar conocimiento para la seguridad y convivencia ciudadana y orientar operaciones", "Solo asesorar a líderes políticos"])

                    btn_evaluar = st.form_submit_button("FINALIZAR Y GUARDAR NOTA")

                    if btn_evaluar:
                        aciertos = 0
                        if p1 == "Asesoramiento proporcionando conocimiento integrado que reduzca incertidumbres": aciertos += 1
                        if p2 == "Inteligencia Estratégica": aciertos += 1
                        if p3 == "Inteligencia Táctica": aciertos += 1
                        if p4 == "Por el hincapié en habilidades para manejar situaciones concretas y la experiencia sensorial": aciertos += 1
                        if p5 == "Generar conocimiento para la seguridad y convivencia ciudadana y orientar operaciones": aciertos += 1
                        
                        nota = (aciertos / 5) * 100
                        try:
                            with engine.connect() as conn:
                                query = text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)")
                                conn.execute(query, {"f": "Agente_DIPOL", "n": nota, "m": seleccion})
                                conn.commit()
                            
                            st.success(f"Nota final guardada: {nota}%")
                            if nota >= 70: st.balloons()
                            st.session_state['modo_examen'] = False
                        except Exception as e:
                            st.error(f"Error: {e}")

    elif seccion == "📊 Progreso":
        st.title("📊 Historial de Capacitación")
        
        try:
            # Consultamos los datos de la tabla calificaciones
            with engine.connect() as conn:
                # Traemos funcionario, modulo, nota y la fecha formateada
                query = text("""
                    SELECT 
                        funcionario, 
                        modulo, 
                        nota, 
                        TO_CHAR(fecha, 'DD/MM/YYYY HH24:MI') as fecha_formateada 
                    FROM calificaciones 
                    ORDER BY fecha DESC
                """)
                df = pd.read_sql(query, conn)
            
            if not df.empty:
                # --- MÉTRICAS RÁPIDAS ---
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Exámenes", len(df))
                with col2:
                    st.metric("Promedio General", f"{df['nota'].mean():.1f}%")
                with col3:
                    # Contamos aprobados (nota >= 70)
                    aprobados = len(df[df['nota'] >= 70])
                    st.metric("Aprobados", aprobados)

                st.divider()

                # --- TABLA DE RESULTADOS ---
                st.subheader("📋 Detalle de Calificaciones")
                # Renombramos columnas para que se vean mejor en la interfaz
                df_display = df.rename(columns={
                    "fecha_formateada": "Fecha y Hora",
                    "funcionario": "Agente",
                    "modulo": "Módulo Cursado",
                    "nota": "Calificación (%)"
                })
                st.dataframe(df_display, use_container_width=True)

                # --- GRÁFICO DE RENDIMIENTO ---
                st.subheader("📈 Evolución del Aprendizaje")
                # Creamos un gráfico de barras para ver las notas por módulo
                st.bar_chart(data=df, x="modulo", y="nota")
                
            else:
                st.info("💡 Aún no hay registros en la base de datos. Realice su primer examen en la sección de 'Módulos'.")
                
        except Exception as e:
            st.error(f"❌ Error al conectar con PostgreSQL: {e}")
            st.warning("Asegúrese de que la tabla 'calificaciones' tenga las columnas: funcionario, modulo, nota y fecha.")
