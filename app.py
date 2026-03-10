import streamlit as st
from sqlalchemy import text

st.title("Prueba de Conexión DIPOL")

# 1. Intentar la conexión
try:
    conn = st.connection("postgresql", type="sql")
    
    # FORMA CORREGIDA: Usamos directamente el string o evitamos el cacheo problemático
    with conn.session as session:
        query = text("SELECT COUNT(*) FROM calificaciones")
        resultado = session.execute(query).fetchone()
    
    st.success("✅ ¡CONEXIÓN ACTIVA!")
    st.write(f"Conexión establecida con el túnel de Localtonet.")
    st.metric("Registros actuales en la tabla:", resultado[0])

except Exception as e:
    st.error("❌ ERROR DE CONEXIÓN REAL")
    st.info("Si ves este mensaje, revisa el puerto en Secrets y Localtonet.")
    st.exception(e)

# 2. Botón para re-intentar
if st.button("Probar conexión de nuevo"):
    st.rerun()
