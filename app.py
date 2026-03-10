import streamlit as st
from sqlalchemy import create_engine, text

# 🛡️ Configuración de la App
st.set_page_config(page_title="Sistema DIPOL", page_icon="🛡️")
st.title("Sistema de Evaluación - DIPOL")

# 1. Obtener credenciales de los Secrets
db_secrets = st.secrets["connections"]["postgresql"]

# 2. Crear el motor de conexión (Engine)
# Usamos pool_pre_ping para que la conexión no se caiga por inactividad
engine = create_engine(
    f"postgresql://{db_secrets['username']}:{db_secrets['password']}@{db_secrets['host']}:{db_secrets['port']}/{db_secrets['database']}",
    pool_pre_ping=True
)

# 3. Interfaz de Usuario
nombre = st.text_input("Nombre del Agente:")
nota_eval = st.number_input("Calificación Final:", min_value=0, max_value=100, step=1)

if st.button("Registrar Evaluación"):
    if nombre:
        try:
            with engine.connect() as conn:
                # --- AQUÍ ESTÁ LA CORRECCIÓN CLAVE ---
                # Usamos text() y los nombres de tus columnas: funcionario y nota
                query = text("INSERT INTO calificaciones (funcionario, nota) VALUES (:nom, :not)")
                conn.execute(query, {"nom": nombre, "not": nota_eval})
                conn.commit()
                
            st.balloons()
            st.success(f"✅ Registro de {nombre} guardado exitosamente.")
        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")
    else:
        st.warning("Por favor, ingrese el nombre del agente.")

# 4. Ver registros (Opcional para confirmar)
if st.checkbox("Ver últimos 5 registros"):
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT funcionario, nota, fecha FROM calificaciones ORDER BY id DESC LIMIT 5"))
            st.table(res.fetchall())
    except:
        st.write("Aún no hay datos para mostrar.")
