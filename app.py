# ... (viene del código anterior)
    
    elif seccion == "📚 Módulos":
        st.session_state['nav_index'] = 1
        lista_modulos = [
            "Módulo 1: Conceptualización", "Módulo 2: Ciclo de Inteligencia", 
            "Módulo 3: Recolección", "Módulo 4: Tratamiento", 
            "Módulo 5: Análisis", "Módulo 6: Comunicación", "Módulo 7: Evaluación"
        ]
        
        # Sincronización con la selección de Inicio
        try:
            idx_mod = lista_modulos.index(st.session_state['modulo_activo'])
        except ValueError:
            idx_mod = 0
            
        modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", lista_modulos, index=idx_mod)
        st.session_state['modulo_activo'] = modulo_selec

        st.divider()

        # =========================================================
        # ESTRUCTURA DE CONTENIDO POR MÓDULO
        # =========================================================

        # --- MÓDULO 1: CONCEPTUALIZACIÓN ---
        if modulo_selec == "Módulo 1: Conceptualización":
            st.header("📖 Módulo 1: Conceptualización")
            with st.container():
                st.markdown("""
                ### Fundamentos de Inteligencia
                [AQUÍ: Insertar texto de lectura, definiciones y leyes]
                """)
                # st.image("diagrama_m1.png") # [AQUÍ: Insertar imágenes del Módulo 1]
            
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M1")
            # [AQUÍ: Insertar st.form() con las preguntas del examen 1]

        # --- MÓDULO 2: CICLO DE INTELIGENCIA ---
        elif modulo_selec == "Módulo 2: Ciclo de Inteligencia":
            st.header("🔄 Módulo 2: Ciclo de Inteligencia")
            st.markdown("[AQUÍ: Insertar las fases del ciclo (Planeación, Búsqueda, etc.)]")
            # st.image("ciclo_inteligencia.png") # [AQUÍ: Insertar diagrama del ciclo]

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M2")
            # [AQUÍ: Insertar st.form() con las preguntas del examen 2]

        # --- MÓDULO 3: RECOLECCIÓN ---
        elif modulo_selec == "Módulo 3: Recolección":
            st.header("🕵️ Módulo 3: Recolección de Información")
            st.markdown("[AQUÍ: Contenido sobre fuentes abiertas, cerradas y humanas]")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M3")

        # --- MÓDULO 4: TRATAMIENTO ---
        elif modulo_selec == "Módulo 4: Tratamiento":
            st.header("📊 Módulo 4: Tratamiento de Datos")
            # [AQUÍ: Insertar la matriz de evaluación de fuente y contenido]
            st.image("image_3fdba2.png", caption="Matriz de Evaluación de Inteligencia")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M4")

        # --- MÓDULO 5: ANÁLISIS ---
        elif modulo_selec == "Módulo 5: Análisis":
            st.header("🧠 Módulo 5: Análisis de Inteligencia")
            # [AQUÍ: Insertar la "Línea del Conocimiento Analítico"]
            st.image("image_3fd75e.png", caption="Línea del Conocimiento Analítico")
            
            st.divider()
            st.subheader("📝 Examen de Conocimientos - M5")

        # --- MÓDULO 6: COMUNICACIÓN ---
        elif modulo_selec == "Módulo 6: Comunicación":
            st.header("📢 Módulo 6: Comunicación e Integración")
            st.markdown("[AQUÍ: Contenido sobre Difusión y documentos de inteligencia]")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M6")

        # --- MÓDULO 7: EVALUACIÓN ---
        elif modulo_selec == "Módulo 7: Evaluación":
            st.header("🔄 Módulo 7: Evaluación y Retroalimentación")
            st.markdown("[AQUÍ: Contenido sobre el impacto del producto de inteligencia]")

            st.divider()
            st.subheader("📝 Examen de Conocimientos - M7")

    elif seccion == "📊 Mi Progreso":
        # ... (continúa con el resto de tu código)
