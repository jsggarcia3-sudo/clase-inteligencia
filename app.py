import streamlit as st

# 1. Establecer la conexión usando los Secrets (TOML)
try:
    conn = st.connection("postgresql", type="sql")
    st.success("✅ Conexión exitosa con el servidor de la DIPOL")
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
    st.info("Asegúrate de que Localtonet esté abierto y en estado 'Connected' en tu PC.")

# 2. Función para insertar la nota de la evaluación
def guardar_nota(nombre_agente, nota):
    try:
        with conn.session as session:
            # Ajusta el nombre de la tabla y columnas según tu pgAdmin
            session.execute(
                "INSERT INTO calificaciones (agente, nota) VALUES (:nombre, :nota);",
                {"nombre": nombre_agente, "nota": nota}
            )
            session.commit()
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# 3. Interfaz básica de Streamlit
st.title("Sistema de Evaluación - DIPOL")

nombre = st.text_input("Nombre del Agente:")
nota_eval = st.number_input("Calificación Final:", min_value=0, max_value=100)

if st.button("Registrar Evaluación"):
    if nombre:
        if guardar_nota(nombre, nota_eval):
            st.balloons()
            st.success(f"Nota de {nombre} guardada correctamente en la base de datos local.")
    else:
        st.warning("Por favor, ingresa el nombre del agente.")
