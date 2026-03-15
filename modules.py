"""
Módulo de Gestión de Contenidos Educativos
Funciones centralizadas para manejo de módulos, exámenes y evaluaciones
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ModuleError(Exception):
    """Excepción personalizada para errores de módulos"""
    pass

class ModuleManager:
    """Gestor centralizado de módulos educativos"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.modulos_disponibles = [
            "Módulo 1: Conceptualización",
            "Módulo 2: Ciclo de Inteligencia", 
            "Módulo 3: Recolección",
            "Módulo 4: Tratamiento",
            "Módulo 5: Análisis",
            "Módulo 6: Comunicación",
            "Módulo 7: Evaluación"
        ]
        
        # Definición de contenidos de módulos
        self.contenidos_modulos = self._definir_contenidos()
    
    def _definir_contenidos(self) -> Dict[str, Dict[str, Any]]:
        """Define la estructura y contenido de todos los módulos"""
        return {
            "Módulo 1: Conceptualización": {
                "titulo": "📖 Material: Conceptualización de Inteligencia",
                "contenido": self._get_contenido_modulo1,
                "examen": self._get_examen_modulo1
            },
            "Módulo 2: Ciclo de Inteligencia": {
                "titulo": "📖 Material: Ciclo de Inteligencia",
                "contenido": self._get_contenido_modulo2,
                "examen": self._get_examen_modulo2
            },
            "Módulo 3: Recolección": {
                "titulo": "📖 Material Completo: Recolección de Información",
                "contenido": self._get_contenido_modulo3,
                "examen": self._get_examen_modulo3
            },
            "Módulo 4: Tratamiento": {
                "titulo": "📖 Material: Tratamiento de la Información",
                "contenido": self._get_contenido_modulo4,
                "examen": self._get_examen_modulo4
            },
            "Módulo 5: Análisis": {
                "titulo": "🧠 Material: Análisis de la Información",
                "contenido": self._get_contenido_modulo5,
                "examen": self._get_examen_modulo5
            },
            "Módulo 6: Comunicación": {
                "titulo": "📢 Material: Comunicación de Inteligencia",
                "contenido": self._get_contenido_modulo6,
                "examen": self._get_examen_modulo6
            },
            "Módulo 7: Evaluación": {
                "titulo": "🔄 Material: Evaluar y Retroalimentar",
                "contenido": self._get_contenido_modulo7,
                "examen": self._get_examen_modulo7
            }
        }
    
    def verificar_estado_modulo(self, nombre_modulo: str, nombre_agente: str) -> Optional[float]:
        """
        Verifica si el agente ya completó el módulo
        Retorna la nota si existe, None en caso contrario
        """
        try:
            return self.db_manager.verificar_intento(nombre_agente, nombre_modulo)
        except Exception as e:
            logger.error(f"Error al verificar estado del módulo {nombre_modulo}: {e}")
            return None
    
    def mostrar_contenido_modulo(self, nombre_modulo: str):
        """Muestra el contenido educativo del módulo especificado"""
        try:
            if nombre_modulo not in self.contenidos_modulos:
                raise ModuleError(f"Módulo no encontrado: {nombre_modulo}")
            
            modulo_info = self.contenidos_modulos[nombre_modulo]
            st.header(modulo_info["titulo"])
            
            # Mostrar contenido
            if callable(modulo_info["contenido"]):
                modulo_info["contenido"]()
            
            # Verificar estado y mostrar botón de examen
            self._mostrar_estado_examen(nombre_modulo)
            
        except Exception as e:
            logger.error(f"Error al mostrar contenido del módulo {nombre_modulo}: {e}")
            st.error(f"Error al cargar el módulo: {e}")
    
    def _mostrar_estado_examen(self, nombre_modulo: str):
        """Muestra el estado del examen y botón correspondiente"""
        try:
            agente_actual = st.session_state.get('agente_nombre', '')
            nota_previa = self.verificar_estado_modulo(nombre_modulo, agente_actual)
            
            if nota_previa is None:
                if st.button(f"🚀 INICIAR EXAMEN {nombre_modulo.split(':')[0]}", 
                           key=f"btn_examen_{nombre_modulo.split(':')[1]}"):
                    st.session_state['modo_examen'] = True
                    st.rerun()
            else:
                st.success(f"✅ Módulo completado. Calificación: {nota_previa}%")
                
        except Exception as e:
            logger.error(f"Error al mostrar estado de examen: {e}")
            st.error("No se pudo verificar el estado del examen")
    
    def mostrar_examen_modulo(self, nombre_modulo: str):
        """Muestra y procesa el examen del módulo especificado"""
        try:
            if nombre_modulo not in self.contenidos_modulos:
                raise ModuleError(f"Módulo no encontrado: {nombre_modulo}")
            
            modulo_info = self.contenidos_modulos[nombre_modulo]
            st.header(f"📝 Evaluación: {nombre_modulo.split(':')[1]}")
            
            # Mostrar y procesar examen
            if callable(modulo_info["examen"]):
                modulo_info["examen"]()
            
        except Exception as e:
            logger.error(f"Error al mostrar examen del módulo {nombre_modulo}: {e}")
            st.error(f"Error al cargar el examen: {e}")
    
    def procesar_resultados_examen(self, respuestas_correctas: List[bool], 
                                  nombre_modulo: str, nombre_agente: str) -> float:
        """
        Procesa los resultados del examen y los guarda en la base de datos
        Retorna la calificación obtenida
        """
        try:
            nota = (sum(respuestas_correctas) / len(respuestas_correctas)) * 100
            
            # Guardar en base de datos
            self.db_manager.guardar_calificacion(nombre_agente, nombre_modulo, nota)
            
            logger.info(f"Examen procesado: {nombre_agente} - {nombre_modulo} - {nota}%")
            return nota
            
        except Exception as e:
            logger.error(f"Error al procesar resultados del examen: {e}")
            raise ModuleError(f"No se pudo procesar el examen: {e}")
    
    # === CONTENIDOS DE MÓDULOS ===
    
    def _get_contenido_modulo1(self):
        """Contenido del Módulo 1: Conceptualización"""
        # Definición General
        st.markdown("""
            <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
                <h3 style="color: #D4AF37; margin-top: 0;">¿Qué es Inteligencia?</h3>
                <p style="color: white; font-size: 1.05em;">Es el <b>conocimiento obtenido</b> mediante el procesamiento de información para reducir la incertidumbre en la toma de decisiones.</p>
                <ul style="color: #ecf0f1; font-size: 0.95em;">
                    <li>Es una actividad <b>multi y transdisciplinaria</b>.</li>
                    <li>Su función principal es el <b>asesoramiento</b> técnico.</li>
                    <li>Se diferencia del intelecto por enfocarse en <b>habilidades y aptitudes</b> ante situaciones concretas.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("🛡️ Inteligencia Policial")
        st.info("""Conjunto de procesos para generar conocimiento relacionado con la **seguridad y convivencia ciudadana**, contribuyendo al diseño de estrategias institucionales y operaciones de la misión policial.""")

        # Inteligencia según su nivel
        st.markdown("### 📊 Niveles de Inteligencia")
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("""
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #3498db; height: 260px;">
                <h4 style="color: #3498db; text-align: center;">Estratégica</h4>
                <p style="color: white; font-size: 0.85em;">Utilizada por líderes políticos y policiales para formular <b>planes y políticas</b> nacionales a largo plazo.</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #f1c40f; height: 260px;">
                <h4 style="color: #f1c40f; text-align: center;">Operacional</h4>
                <p style="color: white; font-size: 0.85em;">Planeamiento de operaciones en <b>áreas específicas</b>. Se concentra en localización y análisis de objetivos.</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-top: 4px solid #2ecc71; height: 260px;">
                <h4 style="color: #2ecc71; text-align: center;">Táctica</h4>
                <p style="color: white; font-size: 0.85em;">Requerida para la <b>conducción de equipos</b> en el terreno durante operaciones inmediatas.</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
    
    def _get_examen_modulo1(self):
        """Examen del Módulo 1"""
        with st.form("exam_m1"):
            q1 = st.radio("1. ¿Cuál es la función principal de la inteligencia?", 
                ["Asesoramiento para la toma de decisiones", "Realizar capturas físicas", "Publicar noticias"])
            q2 = st.radio("2. La inteligencia se diferencia del intelecto porque hace hincapié en:", 
                ["La memoria", "Habilidades y aptitudes para manejar situaciones concretas", "La velocidad de lectura"])
            q3 = st.radio("3. ¿Sobre qué áreas genera conocimiento la Inteligencia Policial?", 
                ["Solo temas financieros", "Seguridad y convivencia ciudadana", "Trámites administrativos"])
            q4 = st.radio("4. Nivel de inteligencia que ayuda a formular planes y políticas nacionales:", 
                ["Táctica", "Estratégica", "Operacional"])
            q5 = st.radio("5. La inteligencia táctica es requerida para:", 
                ["Leyes nacionales", "Conducción de operaciones a nivel de equipos", "Planificar el presupuesto anual"])

            if st.form_submit_button("FINALIZAR EXAMEN"):
                respuestas = [
                    q1 == "Asesoramiento para la toma de decisiones",
                    q2 == "Habilidades y aptitudes para manejar situaciones concretas",
                    q3 == "Seguridad y convivencia ciudadana",
                    q4 == "Estratégica",
                    q5 == "Conducción de operaciones a nivel de equipos"
                ]
                
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(respuestas, "Módulo 1", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                
                st.session_state['modo_examen'] = False
                st.rerun()
    
    def _get_contenido_modulo2(self):
        """Contenido del Módulo 2: Ciclo de Inteligencia"""
        st.markdown("""
            <div class="lectura-box" style="border-left: 5px solid #D4AF37; margin-bottom: 20px;">
                <h3 style="color: #D4AF37; margin-top: 0;">Definición Estratégica</h3>
                <p style="color: white;">Es un proceso sistemático de <b>cinco pasos</b> orientado a la generation de conocimiento útil y veraz para un decisor final. Su objetivo es transformar datos brutos en inteligencia estratégica.</p>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("🔄 Las 5 Fases del Ciclo")
        
        # Diseño de flujo de proceso con tarjetas
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.markdown("""
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #3498db; margin-bottom: 15px;">
                <h4 style="color: #3498db; margin: 0;">1. Recolectar</h4>
                <p style="color: #ecf0f1; font-size: 0.9em;">Obtención de la <b>información bruta</b> necesaria. Es la fase de búsqueda activa en el campo y bases de datos.</p>
            </div>
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #9b59b6; margin-bottom: 15px;">
                <h4 style="color: #9b59b6; margin: 0;">2. Tratar</h4>
                <p style="color: #ecf0f1; font-size: 0.9em;">Procesamiento, registro y organización de los datos. Se traduce o decodifica la información para que sea legible.</p>
            </div>
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #f1c40f; margin-bottom: 15px;">
                <h4 style="color: #f1c40f; margin: 0;">3. Analizar</h4>
                <p style="color: #ecf0f1; font-size: 0.9em;"><b>Fase crítica:</b> Transformación de datos en inteligencia mediante la valoración, integración e interpretación.</p>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown("""
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #2ecc71; margin-bottom: 15px;">
                <h4 style="color: #2ecc71; margin: 0;">4. Comunicar e Integrar</h4>
                <p style="color: #ecf0f1; font-size: 0.9em;">Difusión selectiva de los resultados al decisor mediante instrumentos formales (Informes de Inteligencia).</p>
            </div>
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #e74c3c; margin-bottom: 15px;">
                <h4 style="color: #e74c3c; margin: 0;">5. Evaluar y Retroalimentar</h4>
                <p style="color: #ecf0f1; font-size: 0.9em;">Revisión constante para asegurar que el producto cumple con los requerimientos originales del destinatario.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.info("**Importante:** El ciclo es dinámico. Un fallo en la fase de 'Tratar' puede invalidar todo el análisis posterior.")
        st.divider()
    
    def _get_examen_modulo2(self):
        """Examen del Módulo 2"""
        with st.form("exam_m2"):
            m2_q1 = st.radio("1. ¿Cuál es el objetivo final del Ciclo de Inteligencia?", 
                ["Solo recolectar datos", "Generar conocimiento útil para un decisor", "Realizar capturas"])
            m2_q2 = st.radio("2. Fase donde la información bruta se transforma en inteligencia:", 
                ["Recolectar", "Analizar", "Comunicar"])
            m2_q3 = st.radio("3. ¿En qué consiste la fase de 'Tratar'?", 
                ["Difundir el informe", "Procesamiento y organización de los datos", "Retroalimentar al jefe"])
            m2_q4 = st.radio("4. ¿Cuál es el último paso del ciclo según el material?", 
                ["Comunicar e Integrar", "Evaluar y Retroalimentar", "Tratar"])
            m2_q5 = st.radio("5. ¿A quién se le difunde el resultado del ciclo?", 
                ["Al público general", "Al destinatario final (Decisor)", "A todas las unidades"])

            if st.form_submit_button("FINALIZAR EXAMEN"):
                res_m2 = [
                    m2_q1 == "Generar conocimiento útil para un decisor",
                    m2_q2 == "Analizar",
                    m2_q3 == "Procesamiento y organización de los datos",
                    m2_q4 == "Evaluar y Retroalimentar",
                    m2_q5 == "Al destinatario final (Decisor)"
                ]
                
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(res_m2, "Módulo 2", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                
                st.session_state['modo_examen'] = False
                st.rerun()
    
    def _get_contenido_modulo3(self):
        """Contenido del Módulo 3: Recolección"""
        t1, t2, t3, t4 = st.tabs(["📌 Fundamentos y PHVA", "🕵️ Operaciones", "👥 Fuentes Humanas", "🎤 La Entrevista"])
        
        with t1:
            st.markdown("""
            <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37;">
                <h3 style="color: #D4AF37; margin-top: 0;">¿Qué es información?</h3>
                <p style="color: white;">Es un conjunto de <b>datos integrados y ordenados</b> que sirven para construir un mensaje. Es la materia prima para resolver problemas y tomar decisiones.</p>
                <p style="color: #D4AF37; font-weight: bold;">⚠️ El DATO es la unidad básica que comprende la información.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### El Ciclo PHVA en Recolección")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.write("**🔵 PLANEAR:** Establecer objetivos, identificar riesgos y planificar recursos.")
                st.write("**🟢 HACER:** Búsqueda de información, ejecutar actividades y elaborar productos.")
            with col_p2:
                st.write("**🟠 VERIFICAR:** Autoevaluación de control y gestión (seguimiento).")
                st.write("**🔴 ACTUAR:** Implementar acciones correctivas o preventivas.")

        with t2:
            st.subheader("🕵️ Operaciones de Inteligencia Policial")
            
            st.markdown("""
                <div class="lectura-box" style="margin-bottom: 25px;">
                    <h4 style="color: #D4AF37; margin-top: 0;">Fines Operacionales</h4>
                    <p style="color: white; margin: 0;">Son actividades del servicio policial orientadas a la obtención de información privilegiada. Para toda operación se requiere el <b>Empleo y uso de Medios Técnicos</b>.</p>
                </div>
            """, unsafe_allow_html=True)

        with t3:
            st.subheader("👥 Administración de Fuentes Humanas")
            st.markdown("""
                <div class="lectura-box">
                    <h4 style="color: #D4AF37; margin-top: 0;">Fases del Proceso Operativo</h4>
                    <p style="color: white;">La administración de fuentes requiere un seguimiento riguroso para garantizar la fiabilidad de la información obtenida.</p>
            </div>
        """, unsafe_allow_html=True)

        with t4:
            st.subheader("🎤 La Entrevista de Inteligencia")
            st.markdown("""
                <div class="lectura-box" style="border-left: 5px solid #e74c3c;">
                    <h4 style="color: #e74c3c; margin-top: 0;">Tipos de Entrevistador a EVITAR</h4>
                    <p style="color: white;">Procedimiento utilizado para la obtención de información de una fuente humana, mediante el intercambio de ideas y la correcta formulación de preguntas por el agente de inteligencia.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.info("**Nota Técnica:** El éxito de la entrevista radica en el **Rapport** (establecimiento de sintonía) y la escucha activa.")
        
        st.divider()
    
    def _get_examen_modulo3(self):
        """Examen del Módulo 3"""
        with st.form("exam_m3"):
            q1 = st.radio("1. ¿Qué es el Sonsacamiento?", ["Entrevista formal", "Diálogo donde la fuente no debe percatarse de la explotación", "Vigilancia fija"])
            q2 = st.radio("2. En PHVA, ¿qué implica la etapa HACER?", ["Planificar recursos", "Búsqueda de información y ejecución", "Acciones preventivas"])
            q3 = st.radio("3. Diferencia entre Infiltración y Penetración:", ["No hay diferencia", "Infiltración mete al agente; Penetración usa a alguien de adentro", "Infiltración es solo técnica"])
            q4 = st.radio("4. ¿Cuál es la unidad básica que comprende la información?", ["El mensaje", "El dato", "El informe"])
            q5 = st.radio("5. ¿Qué busca el Reconocimiento?", ["Solo vigilar", "Concretar datos de inmuebles, seguridad y entorno", "Sonsacar a la fuente"])

            if st.form_submit_button("FINALIZAR EXAMEN"):
                respuestas = [
                    q1 == "Diálogo donde la fuente no debe percatarse de la explotación",
                    q2 == "Búsqueda de información y ejecución",
                    q3 == "Infiltración mete al agente; Penetración usa a alguien de adentro",
                    q4 == "El dato",
                    q5 == "Concretar datos de inmuebles, seguridad y entorno"
                ]
                
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(respuestas, "Módulo 3", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                
                st.session_state['modo_examen'] = False
                st.rerun()
    
    # Métodos simplificados para los módulos restantes
    def _get_contenido_modulo4(self):
        """Contenido del Módulo 4"""
        st.info("Contenido del Módulo 4: Tratamiento de la Información")
        st.write("Este módulo cubre el procesamiento sistemático de datos e información recolectada...")
        st.divider()
    
    def _get_examen_modulo4(self):
        """Examen del Módulo 4"""
        with st.form("exam_m4"):
            q1 = st.radio("1. ¿Qué implica la etapa de 'Organización'?", 
                ["Captura de objetivos", "Determinar tipo de información, blanco y prioridad", "Publicar en redes sociales"])
            q2 = st.radio("2. Según la matriz 4x4, el código 'C-3' representa un porcentaje de:", 
                ["100%", "75%", "50%"])
            
            if st.form_submit_button("FINALIZAR EXAMEN"):
                respuestas = [q1 == "Determinar tipo de información, blanco y prioridad", q2 == "50%"]
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(respuestas, "Módulo 4", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                st.session_state['modo_examen'] = False
                st.rerun()
    
    def _get_contenido_modulo5(self):
        """Contenido del Módulo 5"""
        st.info("Contenido del Módulo 5: Análisis de la Información")
        st.write("Este módulo cubre el proceso de análisis y generación de conocimiento...")
        st.divider()
    
    def _get_examen_modulo5(self):
        """Examen del Módulo 5"""
        with st.form("exam_m5"):
            q1 = st.radio("1. ¿Cuál es el objeto principal del proceso de análisis?", 
                ["Recopilar la mayor cantidad de datos posible", "Generar conocimiento con base en la información disponible"])
            
            if st.form_submit_button("FINALIZAR EXAMEN"):
                respuestas = [q1 == "Generar conocimiento con base en la información disponible"]
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(respuestas, "Módulo 5", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                st.session_state['modo_examen'] = False
                st.rerun()
    
    def _get_contenido_modulo6(self):
        """Contenido del Módulo 6"""
        st.info("Contenido del Módulo 6: Comunicación de Inteligencia")
        st.write("Este módulo cubre la difusión y comunicación de productos de inteligencia...")
        st.divider()
    
    def _get_examen_modulo6(self):
        """Examen del Módulo 6"""
        with st.form("exam_m6"):
            q1 = st.radio("1. ¿Cuál es la premisa fundamental de la comunicación en inteligencia?", 
                ["Almacenar información indefinidamente", "Que la inteligencia llegue al decisor en el momento oportuno"])
            
            if st.form_submit_button("FINALIZAR EXAMEN"):
                respuestas = [q1 == "Que la inteligencia llegue al decisor en el momento oportuno"]
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(respuestas, "Módulo 6", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                st.session_state['modo_examen'] = False
                st.rerun()
    
    def _get_contenido_modulo7(self):
        """Contenido del Módulo 7"""
        st.info("Contenido del Módulo 7: Evaluación y Retroalimentación")
        st.write("Este módulo cubre la evaluación de impacto y retroalimentación del ciclo...")
        st.divider()
    
    def _get_examen_modulo7(self):
        """Examen del Módulo 7"""
        with st.form("exam_m7"):
            q1 = st.radio("1. ¿Cuál es el objetivo principal de la fase de Evaluación?", 
                ["Almacenar reportes antiguos", "Identificar oportunidades de mejoramiento del servicio"])
            
            if st.form_submit_button("FINALIZAR EXAMEN"):
                respuestas = [q1 == "Identificar oportunidades de mejoramiento del servicio"]
                agente_actual = st.session_state.get('agente_nombre', '')
                try:
                    nota = self.procesar_resultados_examen(respuestas, "Módulo 7", agente_actual)
                    st.success(f"✅ Examen completado. Calificación: {nota}%")
                except Exception as e:
                    st.error(f"Error al guardar resultados: {e}")
                st.session_state['modo_examen'] = False
                st.rerun()

# Instancia global del gestor de módulos
def get_module_manager(db_manager):
    """Retorna una instancia del gestor de módulos"""
    return ModuleManager(db_manager)
