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
# --- MÓDULO DE INTELIGENCIA Y ANÁLISIS ---
st.divider()
st.header("📊 Panel de Análisis de Rendimiento")

try:
    with engine.connect() as conn:
        # 1. Extraer todos los datos para el análisis
        query_analisis = text("SELECT fecha, funcionario, nota FROM calificaciones ORDER BY fecha ASC")
        df = pd.read_sql(query_analisis, conn)

    if not df.empty:
        # Asegurar que la fecha sea leíble
        df['fecha'] = pd.to_datetime(df['fecha']).dt.date
        
        # --- FILA 1: Métricas Clave ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Evaluaciones", len(df))
        with col2:
            promedio = df['nota'].mean()
            st.metric("Promedio General", f"{promedio:.1f}%")
        with col3:
            mejor_nota = df['nota'].max()
            st.metric("Calificación Más Alta", f"{mejor_nota}%")

        # --- FILA 2: Visualización Táctica ---
        tab1, tab2 = st.tabs(["📈 Tendencia Temporal", "📋 Detalle Nominal"])
        
        with tab1:
            st.subheader("Evolución de Calificaciones")
            # Agrupamos por fecha para ver el promedio diario
            df_trend = df.groupby('fecha')['nota'].mean().reset_index()
            st.line_chart(data=df_trend, x='fecha', y='nota')
            st.caption("Muestra el promedio de rendimiento de los agentes a lo largo del tiempo.")

        with tab2:
            st.subheader("Registro Completo de Funcionarios")
            # Buscador rápido dentro de la tabla
            busqueda = st.text_input("🔍 Filtrar por nombre del funcionario:")
            if busqueda:
                df_filtrado = df[df['funcionario'].str.contains(busqueda, case=False)]
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
            else:
                st.dataframe(df.sort_values(by='fecha', ascending=False), use_container_width=True, hide_index=True)

    else:
        st.info("No hay datos suficientes para generar el dashboard todavía.")

except Exception as e:
    st.warning("El Dashboard estará disponible cuando se registren los primeros datos correctamente.")
