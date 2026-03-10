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

# Estado para controlar si se muestra la lectura o el examen
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
        
        # Reiniciar modo examen si el usuario cambia de sección
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

        # --- LÓGICA DEL MÓDULO 1 ---
        if seleccion == "Módulo 1: Conceptualización de Inteligencia":
            
            # --- VISTA DE LECTURA (Solo si NO está en modo examen) ---
            if not st.session_state['modo_examen']:
                st.header("📖 Material de Lectura: Conceptualización de Inteligencia")
                
                with st.container():
                    st.markdown(f"""
                    <div class="lectura-box">
                        <h3>Definición de Inteligencia</h3>
                        <p>1. Es el <b>conocimiento obtenido</b> a través del procesamiento adecuado de la información...</p>
                        <p>2. Es una actividad <b>multi y transdisciplinaria</b>...</p>
                        <p>3. Su función es el <b>asesoramiento</b>, proporcionando conocimiento integrado...</p>
                        <p>4. Diferencia con intelecto: hincapié en <b>habilidades concretas</b>.</p>
                    </div>
                    
                    <div class="lectura-box">
                        <h3>¿Qué es Inteligencia Policial?</h3>
                        <p>Conjunto de procesos para generar conocimiento relacionado con la <b>seguridad y convivencia ciudadana</b>.</p>
                    </div>

                    <div class="lectura-box">
                        <h3>Inteligencia según su nivel</h3>
                        <ul>
                            <li><b class="highlight">ESTRATÉGICA:</b> Planes y políticas nacionales.</li>
                            <li><b class="highlight">OPERACIONAL:</b> Planeamiento en áreas específicas y minimizar riesgos.</li>
                            <li><b class="highlight">TÁCTICA:</b> Operaciones de equipos y ambiente inmediato.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info("⚠️ Al iniciar la evaluación, el material de lectura desaparecerá.")
                if st.button("🚀 INICIAR EVALUACIÓN"):
                    st.session_state['modo_examen'] = True
                    st.rerun()

            # --- VISTA DE EXAMEN (Solo si está en modo examen) ---
            else:
                st.header("📝 Evaluación Final: Módulo 1")
                st.warning("El material de lectura ha sido ocultado para esta evaluación.")
                
                # Botón opcional para rendirse o volver a leer
                if st.button("⬅️ Volver a Material de Lectura (Cancela examen)"):
                    st.session_state['modo_examen'] = False
                    st.rerun()

                with st.form(key="form_mod1_completo"):
                    p1 = st.radio("1. ¿Cuál es la función principal de la inteligencia?", 
                                  ["Generar incertidumbre", "Asesoramiento para reducir incertidumbres en la toma de decisión", "Ejecutar operaciones tácticas sin análisis"])
                    
                    p2 = st.radio("2. ¿Qué nivel de inteligencia emplean los líderes para la formulación de planes y políticas nacionales?", 
                                  ["Inteligencia Operacional", "Inteligencia Táctica", "Inteligencia Estratégica"])
                    
                    p3 = st.radio("3. ¿Cuál nivel de inteligencia se enfoca en las capacidades del objetivo y su ambiente inmediato?", 
                                  ["Inteligencia Táctica", "Inteligencia Operacional", "Inteligencia Estratégica"])
                    
                    p4 = st.radio("4. ¿Qué diferencia a la inteligencia del intelecto según el texto?", 
                                  ["Son exactamente lo mismo", "El énfasis en habilidades para manejar situaciones concretas", "Que la inteligencia no usa la experiencia sensorial"])
                    
                    p5 = st.radio("5. La Inteligencia Operacional es requerida principalmente para:", 
                                  ["Definir políticas de administración pública", "El planeamiento de operaciones en áreas específicas y minimizar riesgos", "Estudiar la historia de la criminalidad"])

                    btn_evaluar = st.form_submit_button("FINALIZAR Y GUARDAR NOTA")

                    if btn_evaluar:
                        aciertos = 0
                        if p1 == "Asesoramiento para reducir incertidumbres en la toma de decisión": aciertos += 1
                        if p2 == "Inteligencia Estratégica": aciertos += 1
                        if p3 == "Inteligencia Táctica": aciertos += 1
                        if p4 == "El énfasis en habilidades para manejar situaciones concretas": aciertos += 1
                        if p5 == "El planeamiento de operaciones en áreas específicas y minimizar riesgos": aciertos += 1
                        
                        nota = (aciertos / 5) * 100
                        
                        try:
                            with engine.connect() as conn:
                                query = text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)")
                                conn.execute(query, {"f": "Agente_DIPOL", "n": nota, "m": seleccion})
                                conn.commit()
                            
                            st.success(f"¡Examen completado! Nota: {nota}%")
                            if nota >= 70: st.balloons()
                            
                            # Salir del modo examen al terminar
                            st.session_state['modo_examen'] = False
                            st.info("Regresando a la vista principal. Puede ver su progreso en el panel correspondiente.")
                            
                        except Exception as e:
                            st.error(f"Error al conectar con la base de datos: {e}")

        else:
            # Asegurar que el modo examen se resetee si cambia a un módulo sin contenido
            st.session_state['modo_examen'] = False
            st.info(f"El contenido para el {seleccion} se cargará próximamente.")

    elif seccion == "📊 Progreso":
        st.session_state['modo_examen'] = False
        st.title("📊 Historial de Capacitación")
        # ... (Resto del código de progreso se mantiene igual)
