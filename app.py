import streamlit as st
from sqlalchemy import text
import pandas as pd

# 🛡️ Configuración de Identidad Visual
st.set_page_config(page_title="Gestión de Evaluaciones - DIPOL", page_icon="⚖️", layout="wide")

# Estilo personalizado para el encabezado
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #002b5e; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema de Control de Evaluaciones DIPOL")
st.info("Conectado al nodo de base de datos local vía Localtonet")

# 1. Conexión de Red
try:
    conn = st.connection("postgresql", type="sql")
    # Verificación silenciosa
except Exception as e:
    st.error(f"Falla en el enlace: {e}")

# --- BARRA LATERAL (Métricas Rápidas) ---
with st.sidebar:
    st.image("https://www.policianacional.gob.hn/storage/app/public/logo-policia-nacional.png", width=100) # Opcional: Logo oficial
    st.header("Estadísticas Hoy")
    try:
        total_data = conn.query("SELECT COUNT(*) as total FROM calificaciones;", ttl=10)
        st.metric("Agentes Evaluados", total_data["total"][0])
    except:
        st.write("Cargando métricas...")

# --- CUERPO PRINCIPAL (Registro) ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Nuevo Registro")
    with st.form("registro_eval"):
        func_nombre = st.text_input("Nombre del Funcionario:")
        modulo_eval = st.selectbox("Módulo:", ["Inteligencia Operativa", "Ciberseguridad", "Derechos Humanos", "Análisis de Datos"])
        nota_final = st.number_input("Calificación (0-100):", min_value=0, max_value=100)
        
        btn_enviar = st.form_submit_button("Guardar en Base de Datos")

        if btn_enviar:
            if func_nombre:
                try:
                    with conn.session as session:
                        # Usamos los nombres exactos de tu tabla: funcionario, modulo, nota
                        sql = text("INSERT INTO calificaciones (funcionario, modulo, nota) VALUES (:f, :m, :n)")
                        session.execute(sql, {"f": func_nombre, "m": modulo_eval, "n": nota_final})
                        session.commit()
                        st.success(f"✅ {func_nombre} registrado.")
                        st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Ingrese el nombre del funcionario.")

# --- VISUALIZACIÓN (Dashboard) ---
with col2:
    st.subheader("📊 Historial de Calificaciones")
    try:
        # Consultamos los datos actuales
        df = conn.query("SELECT id, fecha, funcionario, modulo, nota FROM calificaciones ORDER BY fecha DESC LIMIT 10;", ttl=5)
        
        # Mostramos la tabla con un diseño limpio
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Gráfico rápido de rendimiento
        if not df.empty:
            st.divider()
            st.caption("Promedio por Módulo")
            chart_data = df.groupby("modulo")["nota"].mean()
            st.bar_chart(chart_data)
            
    except Exception as e:
        st.write("Esperando nuevos datos...")
