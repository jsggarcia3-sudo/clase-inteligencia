import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Sistema DIPOL", page_icon="🛡️")
st.title("🛡️ Registro de Evaluaciones DIPOL")

# 1. Conexión Directa
db = st.secrets["connections"]["postgresql"]
conn_url = f"postgresql://{db['username']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"

@st.cache_resource
def get_engine():
    return create_engine(conn_url, pool_pre_ping=True)

try:
    engine = get_engine()
    
    # --- Formulario de Registro ---
    with st.form("form_evaluacion"):
        nombre = st.text_input("Nombre del Funcionario:")
        nota = st.number_input("Calificación (0-100):", 0, 100)
        enviar = st.form_submit_button("Guardar Registro")
        
        if enviar and nombre:
            with engine.connect() as conn:
                # Usamos los nombres reales de tu tabla
                sql = text("INSERT INTO calificaciones (funcionario, nota) VALUES (:f, :n)")
                conn.execute(sql, {"f": nombre, "n": nota})
                conn.commit()
                st.success(f"¡Éxito! {nombre} ha sido evaluado.")
                st.balloons()

    # --- Visualización de Datos ---
    if st.checkbox("Mostrar historial reciente"):
        with engine.connect() as conn:
            query = text("SELECT funcionario, nota, fecha FROM calificaciones ORDER BY id DESC LIMIT 5")
            data = conn.execute(query).fetchall()
            st.table(data)

except Exception as e:
    st.error("Error de conexión. Verifica si Localtonet sigue conectado.")
    st.info(f"Puerto actual: {db['port']}")
