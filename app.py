import streamlit as st
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus  # <--- Esto es lo nuevo para limpiar la contraseña

# 🛡️ Configuración de la App
st.set_page_config(page_title="Sistema DIPOL", page_icon="🛡️")
st.title("Sistema de Evaluación - DIPOL")

# 1. Obtener credenciales de los Secrets
db_secrets = st.secrets["connections"]["postgresql"]

# --- EL CAMBIO CLAVE ESTÁ AQUÍ ---
# Limpiamos la contraseña para que el símbolo @ no rompa la URL
password_segura = quote_plus(db_secrets['password'])

# 2. Crear el motor de conexión (Engine)
# Usamos la variable password_segura en lugar de la directa
engine = create_engine(
    f"postgresql://{db_secrets['username']}:{password_segura}@{db_secrets['host']}:{db_secrets['port']}/{db_secrets['database']}",
    pool_pre_ping=True
)
# ---------------------------------

# 3. Interfaz de Usuario
nombre = st.text_input("Nombre del Agente:")
nota_eval = st.number_input("Calificación Final:", min_value=0, max_value=100, step=1)

if st.button("Registrar Evaluación"):
    if nombre:
        try:
            with engine.connect() as conn:
                query = text("INSERT INTO calificaciones (funcionario, nota) VALUES (:nom, :not)")
                conn.execute(query, {"nom": nombre, "not": nota_eval})
                conn.commit()
                
            st.balloons()
            st.success(f"✅ Registro de {nombre} guardado exitosamente.")
        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")
    else:
        st.warning("Por favor, ingrese el nombre del agente.")

# 4. Ver registros
if st.checkbox("Ver últimos 5 registros"):
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT funcionario, nota, fecha FROM calificaciones ORDER BY id DESC LIMIT 5"))
            st.table(res.fetchall())
    except:
        st.write("Aún no hay datos para mostrar.")
