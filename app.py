import streamlit as st
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

st.title("🛡️ Diagnóstico de Conexión DIPOL")

# 1. Verificación de Secrets
db_s = st.secrets["connections"]["postgresql"]
st.info(f"Intentando conectar a: {db_s['host']} a través del puerto: {db_s['port']}")

try:
    pass_segura = quote_plus(db_s['password'])
    # Creamos el motor
    engine = create_engine(
        f"postgresql://{db_s['username']}:{pass_segura}@{db_s['host']}:{db_s['port']}/{db_s['database']}",
        connect_args={'connect_timeout': 5} # No esperar demasiado si falla
    )
    
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        st.success("✅ ¡ENLACE EXITOSO! PostgreSQL detectado.")
        
        # Formulario rápido
        with st.form("registro"):
            nom = st.text_input("Agente:")
            nt = st.number_input("Nota:", 0, 100)
            if st.form_submit_button("Guardar"):
                conn.execute(text("INSERT INTO calificaciones (funcionario, nota) VALUES (:n, :t)"), {"n":nom, "t":nt})
                conn.commit()
                st.balloons()

except Exception as e:
    st.error("❌ Fallo de comunicación")
    st.write("Detalle para análisis:")
    st.code(str(e))
