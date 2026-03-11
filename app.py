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
if 'modulo_activo' not in st.session_state: st.session_state['modulo_activo'] = "Módulo 1: Conceptualización"
if 'nav_index' not in st.session_state: st.session_state['nav_index'] = 0

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
    # Configuración de base de datos
    db_s = st.secrets["connections"]["postgresql"]
    engine = create_engine(f"postgresql://{db_s['username']}:{quote_plus(db_s['password'])}@{db_s['host']}:{db_s['port']}/{db_s['database']}")

    # 3. BARRA LATERAL (MENÚ)
    with st.sidebar:
        st.title("📂 MENÚ")
        st.write(f"**{'🛡️ ADMIN' if st.session_state['es_admin'] else '👤 AGENTE'}:**\n{st.session_state['agente_nombre']}")
        
        opciones_nav = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso", "📈 Dashboard General"]
        seccion = st.radio("Ir a:", opciones_nav, index=st.session_state['nav_index'])
        
        # Sincronizar nav_index con la selección manual del radio
        st.session_state['nav_index'] = opciones_nav.index(seccion)

        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
            
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

        # --- CONTENIDO POR MÓDULO (IDENTACIÓN CORREGIDA) ---
        if modulo_selec == "Módulo 1: Conceptualización":
            st.header("📖 Módulo 1: Conceptualización")
            st.markdown("### Fundamentos de Inteligencia\nContenido en desarrollo...")

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
                    st.subheader("Fuentes de Información")
                    st.markdown("""
                    * **Abiertas:** Medios de comunicación, redes sociales, registros públicos.
                    * **Cerradas Especializadas:** Bases de datos restringidas, archivos técnicos.
                    * **Cerradas Humanas:** Personas que brindan información.
                    * **Técnicas:** Obtenidas por medios tecnológicos (sensores, cámaras).
                    """)
                    
                    st.markdown("### Fases de Administración de Fuentes")
                    st.success("1. Exploración | 2. Aproximación | 3. Registro | 4. Entrenamiento")

                with t4:
                    st.subheader("La Entrevista de Inteligencia")
                    st.markdown("""
                    **Etapas Críticas:**
                    1. **Planeación:** Definir qué queremos saber.
                    2. **Desarrollo:** Mantener armonía (**Rapport**) sin perder el control.
                    3. **Terminación:** Al agotar la exploración.
                    4. **Informe:** Documentar y procesar para la administración.
                    """)
                    st.error("**EVITAR:** Ser un entrevistador 'Sordo' (solo mira el papel) o 'Metralleta' (preguntas sin parar).")

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
        st.header("📊 Mi Progreso")
        try:
            with engine.connect() as conn:
                df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), conn, params={"n": st.session_state['agente_nombre']})
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else: 
                st.info("No hay registros aún.")
        except Exception as e: 
            st.info("No hay registros aún o hubo un problema de conexión.")

    elif seccion == "📈 Dashboard General":
        if st.session_state['es_admin']:
            st.title("🛡️ Panel Administrativo")
            try:
                with engine.connect() as conn:
                    df_all = pd.read_sql(text("SELECT funcionario, modulo, nota, fecha FROM calificaciones"), conn)
                
                if not df_all.empty:
                    st.dataframe(df_all, use_container_width=True)
                    st.divider()
                    st.subheader("Promedio por Módulo")
                    # Agrupamos y graficamos el promedio de notas
                    chart_data = df_all.groupby('modulo')['nota'].mean()
                    st.bar_chart(chart_data)
                else: 
                    st.info("No hay datos globales registrados.")
            except Exception as e:
                st.error("Error al acceder a la base de datos administrativa.")
        else: 
            st.warning("Acceso restringido a administradores.")
