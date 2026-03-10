import streamlit as st
from sqlalchemy import text

# Configuración de la página
st.set_page_config(page_title="Sistema DIPOL", page_icon="🛡️")

st.title("Sistema de Evaluación - DIPOL")

# 1. Establecer la conexión usando los Secrets de Streamlit
try:
    # Esta función busca automáticamente el bloque [connections.postgresql] en tus Secrets
    conn = st.connection("postgresql", type="sql")
    st.success("✅ Conexión exitosa con el servidor de la DIPOL")
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
    st.info("Verifica que Localtonet esté abierto y diga 'Connected' en tu PC.")

# 2. Función para insertar los datos en PostgreSQL
def guardar_nota(nombre_agente, nota):
    try:
        with conn.session as session:
            # Ahora usamos "funcionario" para que coincida con tu pgAdmin
            query = text("INSERT INTO calificaciones (funcionario, nota) VALUES (:nombre, :nota)")
            session.execute(query, {"nombre": nombre_agente, "nota": nota})
            session.commit()
        return True
    except Exception as e:
        st.error(f"Error técnico al insertar: {e}")
        return False

# 3. Interfaz de usuario (Formulario)
with st.form("formulario_evaluacion", clear_on_submit=True):
    st.subheader("Registro de Calificación")
    nombre = st.text_input("Nombre del Agente:")
    nota_eval = st.number_input("Calificación Final:", min_value=0, max_value=100, step=1)
    
    # Botón de envío dentro del formulario
    submit_button = st.form_submit_button("Registrar Evaluación")

    if submit_button:
        if nombre:
            exito = guardar_nota(nombre, nota_eval)
            if exito:
                st.balloons()
                st.success(f"Registro completado: {nombre} ha sido guardado en la base de datos.")
        else:
            st.warning("Debe ingresar el nombre del agente para continuar.")

# 4. Visualización opcional (Para confirmar que se guardó)
if st.checkbox("Ver últimos registros"):
    try:
        df = conn.query("SELECT * FROM calificaciones ORDER BY id DESC LIMIT 5;")
        st.table(df)
    except Exception as e:
        st.write("No se pudo cargar la vista previa.")
