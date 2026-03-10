import streamlit as st
from sqlalchemy import text

st.set_page_config(page_title="Enlace DIPOL", page_icon="🛡️")

# Botón para limpiar conexión si el puerto cambia
if st.sidebar.button("🔄 Refrescar Enlace"):
    st.cache_resource.clear()
    st.rerun()

st.title("🛡️ Validación de Enlace Táctico")

@st.cache_resource(ttl=3600)
def conectar_db():
    return st.connection("postgresql", type="sql")

try:
    conn = conectar_db()
    with conn.session as session:
        # Consulta rápida para validar que el túnel responde
        session.execute(text("SELECT 1"))
    st.success(f"✅ Conexión establecida por el puerto 5843")
    
    # Mostrar datos para confirmar
    df = conn.query("SELECT * FROM calificaciones ORDER BY fecha DESC LIMIT 3;")
    st.dataframe(df)

except Exception as e:
    st.error("❌ Error de Enlace")
    st.warning("El puerto en la web de Localtonet y en los Secrets de Streamlit debe coincidir.")
    st.info(f"Puerto actual configurado: 5843")
