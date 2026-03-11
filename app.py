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
        
        # Sincronización de navegación
        opciones_nav = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso", "📈 Dashboard General"]
        if 'nav_index' not in st.session_state: st.session_state['nav_index'] = 0
        
        seccion = st.radio("Ir a:", opciones_nav, index=st.session_state['nav_index'])
        
        if st.button("Cerrar Sesión"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
            
    if seccion == "🏠 Inicio":
        st.session_state['nav_index'] = 0
        modulos_home = [
            {"id": "M1", "tit": "Módulo 1", "sub": "Conceptualización", "icon": "📖", "full": "Módulo 1: Conceptualización"},
            {"id": "M2", "tit": "Módulo 2", "sub": "Ciclo de Inteligencia", "icon": "🔄", "full": "Módulo 2: Ciclo de Inteligencia"},
            {"id": "M3", "tit": "Módulo 3", "sub": "Recolección", "icon": "🕵️", "full": "Módulo 3: Recolección"},
            {"id": "M4", "tit": "Módulo 4", "sub": "Tratamiento", "icon": "📊", "full": "Módulo 4: Tratamiento"},
            {"id": "M5", "tit": "Módulo 5", "sub": "Análisis", "icon": "🧠", "full": "Módulo 5: Análisis"},
            {"id": "M6", "tit": "Módulo 6", "sub": "Comunicación", "icon": "📢", "full": "Módulo 6: Comunicación"},
            {"id": "M7", "tit": "Módulo 7", "sub": "Evaluación", "icon": "🔄", "full": "Módulo 7: Evaluación"}
        ]
        cols = st.columns(3)
        for i, m in enumerate(modulos_home):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #002147, #001226); padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); min-height: 220px;">
                    <div style="font-size: 3em; margin-bottom: 10px;">{m['icon']}</div>
                    <h3 style="color: #D4AF37; margin: 0;">{m['tit']}</h3>
                    <p style="color: #ffffff; font-size: 0.9em; opacity: 0.8;">{m['sub']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"INGRESAR AL {m['id']}", key=f"btn_home_{m['id']}"):
                    st.session_state['modulo_activo'] = m['full']
                    st.session_state['nav_index'] = 1 # Mueve a Módulos
                    st.rerun()

    elif seccion == "📚 Módulos":
        st.session_state['nav_index'] = 1
        lista_modulos = [
            "Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", 
            "Módulo 3: Recolección", "Módulo 4: Tratamiento", 
            "Módulo 5: Análisis", "Módulo 6: Comunicación", "Módulo 7: Evaluación"
        ]
        
        # El selectbox inicia en el módulo seleccionado desde el inicio
        idx_mod = lista_modulos.index(st.session_state['modulo_activo'])
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", lista_modulos, index=idx_mod)
        st.session_state['modulo_activo'] = modulo_selec

        if modulo_selec == "Módulo 1: Conceptualización":
            st.header("📖 Módulo 1: Conceptualización")
            pass
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            st.header("🔄 Módulo 2: Ciclo de Inteligencia")
            pass
        # ... Repetir elif para los demás módulos ...

    elif seccion == "📚 Módulos":
        st.session_state['nav_index'] = 1
        lista_modulos = [
            "Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", 
            "Módulo 3: Recolección", "Módulo 4: Tratamiento", 
            "Módulo 5: Análisis", "Módulo 6: Comunicación", "Módulo 7: Evaluación"
        ]
        
        idx_mod = lista_modulos.index(st.session_state['modulo_activo'])
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", lista_modulos, index=idx_mod)
        st.session_state['modulo_activo'] = modulo_selec

        # =========================================================
        # ESTRUCTURA DE CONTENIDO POR MÓDULO
        # =========================================================

        # --- MÓDULO 1: CONCEPTUALIZACIÓN ---
        if modulo_selec == "Módulo 1: Conceptualización":
            st.header("📖 Módulo 1: Conceptualización")
            # [AQUÍ: Insertar texto de lectura, definiciones y leyes]
            # [AQUÍ: Insertar imágenes o diagramas del Módulo 1]
            
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M1")
            # [AQUÍ: Insertar st.form() con las preguntas del examen 1]

        # --- MÓDULO 2: CICLO DE INTELIGENCIA ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            st.header("🔄 Módulo 2: Ciclo de Inteligencia")
            # [AQUÍ: Insertar las fases del ciclo (Planeación, Búsqueda, etc.)]
            # [AQUÍ: Insertar st.image() del diagrama del ciclo]

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M2")
            # [AQUÍ: Insertar st.form() con las preguntas del examen 2]

        # --- MÓDULO 3: RECOLECCIÓN ---
        elif modulo_selec == "Módulo 3: Recolección":
            st.header("🕵️ Módulo 3: Recolección de Información")
            # [AQUÍ: Contenido sobre fuentes abiertas, cerradas y humanas]

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M3")
            # [AQUÍ: Lógica de evaluación para el Módulo 3]

        # --- MÓDULO 4: TRATAMIENTO ---
        elif modulo_selec == "Módulo 4: Tratamiento":
            st.header("📊 Módulo 4: Tratamiento de Datos")
            # [AQUÍ: Insertar la matriz de evaluación de fuente y contenido]
            # Ejemplo: st.image("tu_tabla_de_evaluacion.png")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M4")

        # --- MÓDULO 5: ANÁLISIS ---
        elif modulo_selec == "Módulo 5: Análisis":
            st.header("🧠 Módulo 5: Análisis de Inteligencia")
            # [AQUÍ: Insertar la "Línea del Conocimiento Analítico"]
            # st.image("linea_analitica.png")
            
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M5")

        # --- MÓDULO 6: COMUNICACIÓN ---
        elif modulo_selec == "Módulo 6: Comunicación":
            st.header("📢 Módulo 6: Comunicación e Integración")
            # [AQUÍ: Contenido sobre Difusión y tipos de documentos de inteligencia]

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M6")
       
        elif modulo_selec == "Módulo 7: Evaluación":
            if not st.session_state['modo_examen']:
                st.header("🔄 Material: Evaluar y Retroalimentar")
                
                # Definición de Objetivos con diseño destacado
                st.markdown("""
                <div style="background: linear-gradient(90deg, #002147 0%, #003366 100%); padding: 25px; border-radius: 15px; border-right: 5px solid #D4AF37; margin-bottom: 25px;">
                    <h3 style="color: #D4AF37; margin-top: 0;">🎯 Objetivo de la Fase</h3>
                    <p style="color: white; font-size: 1.1em;">
                        Evaluar el impacto del <b>Plan Nacional (PNIP)</b>, <b>Planes Regionales</b> y los productos de inteligencia, 
                        asegurando que los responsables del ciclo identifiquen oportunidades reales de mejoramiento del servicio.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                tab_act, tab_sinai, tab_ejemplos = st.tabs([
                    "⚙️ Actividades Clave", 
                    "📊 Trazabilidad y Análisis", 
                    "📝 Casos de Evaluación"
                ])

                with tab_act:
                    st.subheader("Ruta Crítica de Evaluación")
                    st.write("El proceso se divide en 5 actividades fundamentales:")
                    
                    # Uso de columnas para mostrar el flujo de actividades
                    actividades = [
                        "1. Planificar y programar la evaluación.",
                        "2. Realizar trazabilidad en SINAI.",
                        "3. Seleccionar productos para rastreo.",
                        "4. Trazabilidad de los planes de inteligencia.",
                        "5. Analizar el impacto decisional."
                    ]
                    
                    for act in actividades:
                        st.markdown(f"""
                        <div style="background-color: #0e1117; padding: 12px; border-radius: 8px; border: 1px solid #444; margin-bottom: 8px; color: #D4AF37; font-weight: bold;">
                            {act}
                        </div>
                        """, unsafe_allow_html=True)

                with tab_sinai:
                    st.subheader("Trazabilidad en SINAI")
                    st.info("La trazabilidad no es solo archivo; es el rastreo de acciones y decisiones tomadas basadas en nuestra inteligencia.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4 style="color: #D4AF37;">¿Qué evaluamos?</h4>
                            <ul>
                                <li><b>Pertinencia:</b> ¿El producto respondió al requerimiento?</li>
                                <li><b>Oportunidad:</b> ¿Llegó a tiempo para la operación?</li>
                                <li><b>Exactitud:</b> ¿La información fue veraz?</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="lectura-box">
                            <h4 style="color: #D4AF37;">Impacto Decisional</h4>
                            <p>Se mide si el producto generó una acción concreta: una captura, una desarticulación, o un cambio en la política de seguridad regional.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab_ejemplos:
                    st.subheader("Ejemplos de Retroalimentación")
                    
                    st.markdown("""
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div class="ejemplo-box">
                            <h4 style="color: #4CAF50;">✅ Evaluación Positiva</h4>
                            <p style="color: white; font-size: 0.9em;">
                            <b>Insumo:</b> PTI sobre microtráfico en Zona Centro.<br>
                            <b>Decisión:</b> El mando ordena intervención relámpago.<br>
                            <b>Retroalimentación:</b> El producto permitió 5 capturas. Se felicita al equipo de análisis por la precisión geográfica.
                            </p>
                        </div>
                        <div class="ejemplo-box" style="border-left-color: #F44336;">
                            <h4 style="color: #F44336;">⚠️ Oportunidad de Mejora</h4>
                            <p style="color: white; font-size: 0.9em;">
                            <b>Insumo:</b> Informe estratégico trimestral.<br>
                            <b>Hallazgo:</b> La trazabilidad muestra que el informe llegó 15 días después del consejo de seguridad.<br>
                            <b>Acción:</b> Reajustar los tiempos de tratamiento para el próximo ciclo.
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()
                if st.button("🚀 INICIAR EXAMEN MÓDULO 7"):
                    st.session_state['modo_examen'] = True
                    st.rerun()

        # TERMIANA MODULO 7
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M7")
    
    elif seccion == "📊 Mi Progreso":
        st.title("Historial de Calificaciones")
        try:
            with engine.connect() as conn:
                df = pd.read_sql(text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n"), conn, params={"n": st.session_state['agente_nombre']})
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else: st.info("No hay registros aún.")
        except: st.info("No hay registros aún.")

    elif seccion == "📈 Dashboard General":
        st.session_state['nav_index'] = 3
        if st.session_state['es_admin']:
            st.title("🛡️ Panel Administrativo")
            try:
                with engine.connect() as conn:
                    df_all = pd.read_sql(text("SELECT funcionario, modulo, nota, fecha FROM calificaciones"), conn)
                if not df_all.empty:
                    st.dataframe(df_all, use_container_width=True)
                    st.divider()
                    st.bar_chart(df_all.groupby('modulo')['nota'].mean())
                else: st.info("No hay datos globales aún.")
            except: st.error("Error al cargar datos administrativos.")
        else:
            st.warning("Acceso restringido a administradores.")
