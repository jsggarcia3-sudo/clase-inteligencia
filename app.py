import streamlit as st
from sqlalchemy import create_engine, text

st.title("🛡️ Validación de Enlace Táctico")

# Extraemos los datos de secrets manualmente para asegurar que no hay error de lectura
db_secrets = st.secrets["connections"]["postgresql"]

# Creamos la URL de conexión manualmente
db_url = f"postgresql://{db_secrets['username']}:{db_secrets['password']}@{db_secrets['host']}:{db_secrets['port']}/{db_secrets['database']}"

try:
    # Creamos un motor de conexión fresco cada vez (sin caché)
    engine = create_engine(db_url, pool_pre_ping=True)
    
    with engine.connect() as connection:
        # Prueba simple
        connection.execute(text("SELECT 1"))
        st.success(f"✅ ¡CONEXIÓN ESTABLECIDA!")
        st.info(f"Enlace activo por el puerto {db_secrets['port']}")
        
        # Intentar leer los datos
        st.subheader("Datos en PostgreSQL:")
        query = text("SELECT * FROM calificaciones ORDER BY fecha DESC LIMIT 5")
        result = connection.execute(query)
        for row in result:
            st.write(f"Funcionario: {row.funcionario} - Nota: {row.nota}")

except Exception as e:
    st.error("❌ Error de Enlace Real")
    st.write("Detalle técnico del error:")
    st.code(str(e))
    st.warning("Verifica que PostgreSQL en tu PC permita conexiones externas (archivo pg_hba.conf).")
