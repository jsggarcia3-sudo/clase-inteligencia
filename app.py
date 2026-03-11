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
        
        # Sincronización con la selección de Inicio
        try:
            idx_mod = lista_modulos.index(st.session_state['modulo_activo'])
        except ValueError:
            idx_mod = 0
            
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", lista_modulos, index=idx_mod)
        st.session_state['modulo_activo'] = modulo_selec

        st.divider()

        # =========================================================
        # ESTRUCTURA DE CONTENIDO POR MÓDULO
        # =========================================================

        # --- MÓDULO 1: CONCEPTUALIZACIÓN ---
        if modulo_selec == "Módulo 1: Conceptualización":
            st.header("📖 Módulo 1: Conceptualización")
            with st.container():
                st.markdown("""
                ### Fundamentos de Inteligencia
                [AQUÍ: Insertar texto de lectura, definiciones y leyes]
                """)
                # st.image("diagrama_m1.png") # [AQUÍ: Insertar imágenes del Módulo 1]
            
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M1")
            # [AQUÍ: Insertar st.form() con las preguntas del examen 1]

        # --- MÓDULO 2: CICLO DE INTELIGENCIA ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            st.header("🔄 Módulo 2: Ciclo de Inteligencia")
            st.markdown("[AQUÍ: Insertar las fases del ciclo (Planeación, Búsqueda, etc.)]")
            # st.image("ciclo_inteligencia.png") # [AQUÍ: Insertar diagrama del ciclo]

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M2")
            # [AQUÍ: Insertar st.form() con las preguntas del examen 2]

        # --- MÓDULO 3: RECOLECCIÓN ---
        elif modulo_selec == "Módulo 3: Recolección":
            st.header("🕵️ Módulo 3: Recolección de Información")
            st.markdown("[AQUÍ: Contenido sobre fuentes abiertas, cerradas y humanas]")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M3")

        # --- MÓDULO 4: TRATAMIENTO ---
        elif modulo_selec == "Módulo 4: Tratamiento":
            st.header("📊 Módulo 4: Tratamiento de Datos")
            # [AQUÍ: Insertar la matriz de evaluación de fuente y contenido]
            st.image("image_3fdba2.png", caption="Matriz de Evaluación de Inteligencia")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M4")

        # --- MÓDULO 5: ANÁLISIS ---
        elif modulo_selec == "Módulo 5: Análisis":
            st.header("🧠 Módulo 5: Análisis de Inteligencia")
            # [AQUÍ: Insertar la "Línea del Conocimiento Analítico"]
            st.image("image_3fd75e.png", caption="Línea del Conocimiento Analítico")
            
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M5")

        # --- MÓDULO 6: COMUNICACIÓN ---
        elif modulo_selec == "Módulo 6: Comunicación":
            st.header("📢 Módulo 6: Comunicación e Integración")
            st.markdown("[AQUÍ: Contenido sobre Difusión y documentos de inteligencia]")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M6")

        # --- MÓDULO 7: EVALUACIÓN ---
        # --- CONTENIDO MÓDULO 7 (VERIFICADO: COMPLETO) ---
        if modulo_selec == "Módulo 7: Evaluación":
            if not st.session_state['modo_examen']:
                st.header("🔄 Material: Evaluar y Retroalimentar")
                
                # 1. OBJETIVO (Tu texto sobre PNIP y mejoramiento del servicio)
                st.markdown("""
                <div style="background: linear-gradient(90deg, #002147 0%, #003366 100%); padding: 25px; border-radius: 15px; border-right: 5px solid #D4AF37; margin-bottom: 25px;">
                    <h3 style="color: #D4AF37; margin-top: 0;">🎯 Objetivo de la Fase</h3>
                    <p style="color: white; font-size: 1.1em;">
                        Evaluar el impacto del <b>Plan Nacional (PNIP)</b>, <b>Planes Regionales</b> y los productos de inteligencia, 
                        asegurando que los responsables del ciclo identifiquen oportunidades reales de mejoramiento del servicio.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # 2. LAS 3 PESTAÑAS (Actividades, SINAI, Ejemplos)
                tab_act, tab_sinai, tab_ejemplos = st.tabs(["⚙️ Actividades Clave", "📊 Trazabilidad y Análisis", "📝 Casos de Evaluación"])

                with tab_act:
                    st.subheader("Ruta Crítica de Evaluación")
                    # Las 5 actividades fundamentales que enviaste
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
                        # Pertinencia, Oportunidad, Exactitud
                        st.markdown('<div class="lectura-box"><h4 style="color: #D4AF37;">¿Qué evaluamos?</h4><ul><li><b>Pertinencia:</b> ¿Respondió al requerimiento?</li><li><b>Oportunidad:</b> ¿Llegó a tiempo?</li><li><b>Exactitud:</b> ¿Fue veraz?</li></ul></div>', unsafe_allow_html=True)
                    with col2:
                        # Impacto Decisional
                        st.markdown('<div class="lectura-box"><h4 style="color: #D4AF37;">Impacto Decisional</h4><p>Se mide si el producto generó una acción concreta: una captura, una desarticulación, o un cambio en la política de seguridad regional.</p></div>', unsafe_allow_html=True)

                with tab_ejemplos:
                    st.subheader("Ejemplos de Retroalimentación")
                    # Los cuadros Verde (Positiva) y Rojo (Mejora)
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
