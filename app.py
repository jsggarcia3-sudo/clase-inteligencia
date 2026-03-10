import streamlit as st
from sqlalchemy import text

st.title("Prueba de Conexión DIPOL")

# 1. Intentar la conexión
try:
    conn = st.connection("postgresql", type="sql")
    
    # Intentamos una consulta simple para verificar que la tabla existe y responde
    query = text("SELECT COUNT(*) FROM calificaciones")
    resultado = conn.query(query)
    
    st.success("✅ ¡CONEXIÓN ACTIVA!")
    st.write(f"Conexión establecida con el túnel de Localtonet.")
    st.metric("Registros actuales en la tabla:", resultado.iloc[0, 0])

except Exception as e:
    st.error("❌ ERROR DE CONEXIÓN")
    st.write("Causas probables:")
    st.info("""
    1. El programa **localtonet.exe** en tu PC está cerrado.
    2. El túnel en la web de Localtonet está en **'Stop'**.
    3. La URL o el Puerto en los **Secrets** de Streamlit cambiaron.
    """)
    st.exception(e)

# 2. Botón para re-intentar
if st.button("Probar conexión de nuevo"):
    st.rerun()
