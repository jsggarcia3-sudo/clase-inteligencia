"""
Aplicación Principal Optimizada - Plataforma Educativa DIPOL
Versión refactorizada con arquitectura modular y mejor manejo de errores
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Importaciones de módulos personalizados
from database import db_manager, DatabaseError
from auth import auth_manager, AuthenticationError, initialize_session
from modules import get_module_manager
from config import config

# Configuración de logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

class AppError(Exception):
    """Excepción personalizada para errores de la aplicación"""
    pass

class DIPOLApp:
    """Clase principal de la aplicación DIPOL"""
    
    def __init__(self):
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.module_manager = get_module_manager(self.db_manager)
        self._initialize_app()
    
    def _initialize_app(self):
        """Inicializa la configuración principal de la aplicación"""
        try:
            # Configuración de página
            st.set_page_config(
                page_title=config.APP_TITLE,
                page_icon=config.APP_ICON,
                layout=config.APP_LAYOUT,
                initial_sidebar_state="collapsed"
            )
            
            # Cargar estilos CSS
            self._load_styles()
            
            # Inicializar estado de sesión
            initialize_session()
            
            logger.info("Aplicación inicializada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar la aplicación: {e}")
            raise AppError(f"No se pudo inicializar la aplicación: {e}")
    
    def _load_styles(self):
        """Carga los estilos CSS desde archivo externo"""
        try:
            with open(config.CSS_FILE, 'r', encoding='utf-8') as f:
                css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            logger.info("Estilos CSS cargados exitosamente")
        except FileNotFoundError:
            logger.warning(f"Archivo CSS no encontrado: {config.CSS_FILE}")
        except Exception as e:
            logger.error(f"Error al cargar estilos CSS: {e}")
    
    def run(self):
        """Punto de entrada principal de la aplicación"""
        try:
            # Verificar autenticación
            if not self.auth_manager.is_authenticated():
                self._show_login()
            else:
                self._show_main_app()
                
        except Exception as e:
            logger.error(f"Error en ejecución principal: {e}")
            st.error(f"Error crítico en la aplicación: {e}")
    
    def _show_login(self):
        """Muestra la interfaz de login"""
        try:
            st.markdown("<h1 class='login-title'>ACCESO AL SISTEMA</h1>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([0.5, 2, 0.5])
            
            with col2:
                with st.form("login_form"):
                    nombre = st.text_input("Nombre Completo", placeholder="Ej: Noel Viera")
                    usuario = st.text_input("Usuario", placeholder="Escriba 'User' o su usuario")
                    clave = st.text_input("Contraseña", type="password", placeholder="••••••••")

                    submitted = st.form_submit_button("INGRESAR AL DASHBOARD", use_container_width=True)

                    if submitted:
                        self._process_login(usuario, clave, nombre)

                st.caption("Sistema de Inteligencia v2.6 | Conexión Encriptada")
                
        except Exception as e:
            logger.error(f"Error en interfaz de login: {e}")
            st.error("Error al mostrar la interfaz de login")
    
    def _process_login(self, usuario: str, clave: str, nombre: str):
        """Procesa el intento de login"""
        try:
            if self.auth_manager.login_user(usuario, clave, nombre):
                st.success("Login exitoso")
                st.rerun()
            else:
                st.error("Credenciales inválidas o campos vacíos")
                
        except AuthenticationError as e:
            logger.error(f"Error de autenticación: {e}")
            st.error("Error en el proceso de autenticación")
        except Exception as e:
            logger.error(f"Error inesperado en login: {e}")
            st.error("Error inesperado durante el login")
    
    def _show_main_app(self):
        """Muestra la aplicación principal después del login"""
        try:
            # Marca de agua del usuario
            agente_actual = self.auth_manager.get_current_user()
            st.markdown(f"<div class='watermark'>{agente_actual}</div>", unsafe_allow_html=True)
            
            # Sidebar
            self._show_sidebar()
            
            # Contenido principal
            self._show_main_content()
            
        except Exception as e:
            logger.error(f"Error en aplicación principal: {e}")
            st.error("Error al cargar la aplicación principal")
    
    def _show_sidebar(self):
        """Muestra el sidebar con navegación"""
        try:
            with st.sidebar:
                st.title("📂 MENÚ")
                st.caption("☰ Desliza para cerrar")
                
                # Información del usuario
                nombre_display = self.auth_manager.get_current_user()
                rol_display = '🛡️ ADMIN' if self.auth_manager.is_admin() else '👤 AGENTE'
                st.write(f"**{rol_display}:**\n{nombre_display}")
                
                # Navegación
                secciones = ["🏠 Inicio", "📚 Módulos", "📊 Mi Progreso", "📈 Dashboard General"]
                seccion = st.radio("Ir a:", secciones, key="menu_seccion")
                
                st.divider()
                
                # Botón de logout
                if st.button("🚪 Cerrar Sesión", use_container_width=True):
                    self._process_logout()
                    
        except Exception as e:
            logger.error(f"Error en sidebar: {e}")
            st.error("Error al cargar el menú de navegación")
    
    def _process_logout(self):
        """Procesa el logout del usuario"""
        try:
            self.auth_manager.logout_user()
            st.rerun()
        except Exception as e:
            logger.error(f"Error en logout: {e}")
            st.error("Error al cerrar sesión")
    
    def _show_main_content(self):
        """Muestra el contenido principal según la sección seleccionada"""
        try:
            menu_seccion = st.session_state.get('menu_seccion', '🏠 Inicio')
            
            if menu_seccion == "🏠 Inicio":
                self._show_home()
            elif menu_seccion == "📚 Módulos":
                self._show_modules()
            elif menu_seccion == "📊 Mi Progreso":
                self._show_progress()
            elif menu_seccion == "📈 Dashboard General":
                self._show_dashboard()
            else:
                st.warning("Sección no reconocida")
                
        except Exception as e:
            logger.error(f"Error en contenido principal: {e}")
            st.error("Error al cargar el contenido")
    
    def _show_home(self):
        """Muestra la página de inicio"""
        try:
            st.markdown("""
                <h1 style='text-align: center; color: #D4AF37;'>🛡️ SISTEMA ESTRATÉGICO DE CAPACITACIÓN</h1>
                <p style='text-align: center; color: white; font-size: 1.2em;'>Dirección de Inteligencia Policial (DIPOL)</p>
            """, unsafe_allow_html=True)
            st.divider()

            cols = st.columns([1, 1, 1])
            
            def ir_a_modulo(nombre_modulo):
                st.session_state.menu_seccion = "📚 Módulos"
                st.session_state.modulo_seleccionado = nombre_modulo
                st.session_state.modo_examen = False

            for i, modulo in enumerate(config.HOME_MODULES):
                with cols[i % 3]:
                    self._render_module_card(modulo, ir_a_modulo)
                    
        except Exception as e:
            logger.error(f"Error en página de inicio: {e}")
            st.error("Error al cargar la página de inicio")
    
    def _render_module_card(self, modulo: Dict[str, str], callback):
        """Renderiza una tarjeta de módulo en el home"""
        try:
            card_html = (
                "<div class='modulo-card'>"
                "<div class='card-corner-tl'></div>"
                "<div class='card-corner-br'></div>"
                f"<div class='card-icon'>{modulo['icon']}</div>"
                f"<h3 class='card-title'>{modulo['tit']}</h3>"
                f"<p class='card-sub'>{modulo['sub']}</p>"
                "</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)
            st.button(f"▶ Abrir {modulo['tit']}", 
                      key=f"btn_home_{modulo['id']}", 
                      on_click=callback, 
                      args=(modulo['full'],), 
                      use_container_width=True)
                      
        except Exception as e:
            logger.error(f"Error al renderizar tarjeta de módulo: {e}")
            st.error("Error al mostrar módulo")
    
    def _show_modules(self):
        """Muestra la sección de módulos educativos"""
        try:
            modulo_actual = st.session_state.get('modulo_seleccionado', config.MODULOS_DISPONIBLES[0])
            index_modulo = config.MODULOS_DISPONIBLES.index(modulo_actual) if modulo_actual in config.MODULOS_DISPONIBLES else 0

            def actualizar_modulo():
                st.session_state.modulo_seleccionado = st.session_state.selector_modulo
                st.session_state.modo_examen = False

            modulo_selec = st.selectbox("Seleccione Módulo de Estudio:", 
                                      config.MODULOS_DISPONIBLES, 
                                      index=index_modulo, 
                                      key="selector_modulo", 
                                      on_change=actualizar_modulo)

            # Verificar si está en modo examen
            if st.session_state.get('modo_examen', False):
                self.module_manager.mostrar_examen_modulo(modulo_selec)
            else:
                self.module_manager.mostrar_contenido_modulo(modulo_selec)
                
        except Exception as e:
            logger.error(f"Error en sección de módulos: {e}")
            st.error("Error al cargar los módulos educativos")
    
    def _show_progress(self):
        """Muestra el progreso del usuario actual"""
        try:
            agente_actual = self.auth_manager.get_current_user()
            
            st.markdown(f"""
                <div style="background: linear-gradient(90deg, #001f3f 0%, #003366 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #D4AF37; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                    <h1 style="color: white; margin: 0; font-family: sans-serif;">📊 Mi Expediente Académico</h1>
                    <p style="color: #D4AF37; margin: 5px 0 0 0; font-weight: bold; font-size: 1.1em;">Agente: {agente_actual}</p>
                </div>
            """, unsafe_allow_html=True)

            try:
                df = self.db_manager.cargar_datos_agente(agente_actual)
                
                if not df.empty:
                    promedio = df['nota'].mean()
                    
                    # Estilos de métricas
                    st.markdown("""
                        <style>
                        [data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 3.5rem !important; font-weight: 900 !important; }
                        .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
                        </style>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Mi Promedio", f"{promedio:.1f}%")
                    with col2:
                        st.metric("Evaluaciones", len(df))

                    st.write("---")
                    
                    # Tabla con barra de progreso
                    st.dataframe(
                        df,
                        column_config={
                            "nota": st.column_config.ProgressColumn("Nota Final", format="%d%%", min_value=0, max_value=100),
                            "modulo": "Módulo",
                            "fecha": "Fecha"
                        },
                        use_container_width=True, 
                        hide_index=True
                    )
                else:
                    st.info("Aún no hay evaluaciones registradas para este agente.")

            except DatabaseError as e:
                st.error(f"Error de conexión a la base de datos: {e}")
                st.warning("Por favor, contacte al administrador del sistema.")
                
        except Exception as e:
            logger.error(f"Error en sección de progreso: {e}")
            st.error("Error al cargar el progreso académico")
    
    def _show_dashboard(self):
        """Muestra el dashboard general (solo para administradores)"""
        try:
            if not self.auth_manager.is_admin():
                st.error("🚫 Acceso Denegado: Esta sección requiere credenciales de Administrador.")
                return

            # Título del dashboard
            st.markdown("""
                <div style="background-color: #002b55; padding: 20px; border-radius: 10px; border-bottom: 4px solid #D4AF37; margin-bottom: 25px;">
                    <h1 style="color: white; margin: 0;">🛡️ Centro de Inteligencia Analítica</h1>
                    <p style="color: #D4AF37; margin: 0; font-weight: bold;">Panel de Control y Rendimiento Académico - DIPOL</p>
                </div>
            """, unsafe_allow_html=True)
            
            try:
                df_raw = self.db_manager.cargar_todo_admin()
                
                if not df_raw.empty:
                    self._process_dashboard_data(df_raw)
                else:
                    st.info("ℹ️ No hay registros en la base de datos para generar el análisis.")

            except DatabaseError as e:
                st.error(f"Error de conexión a la base de datos: {e}")
                st.warning("No se pudieron cargar los datos para el dashboard.")
                
        except Exception as e:
            logger.error(f"Error en dashboard: {e}")
            st.error("Error al cargar el dashboard general")
    
    def _process_dashboard_data(self, df_raw: pd.DataFrame):
        """Procesa y muestra los datos del dashboard"""
        try:
            # Procesamiento de datos
            df_raw['fecha'] = pd.to_datetime(df_raw['fecha'])
            df_all = df_raw.sort_values('fecha').drop_duplicates(subset=['funcionario', 'modulo'], keep='last')
            df_all['fecha_display'] = df_all['fecha'].dt.strftime('%Y-%m-%d %H:%M')
            
            # Cálculo de métricas
            promedio = df_all['nota'].mean()
            total_eval = len(df_all)
            aprobados = len(df_all[df_all['nota'] >= 70])
            porcentaje_exito = (aprobados / total_eval) * 100

            # Estilos CSS para tarjetas KPI
            st.markdown("""
                <style>
                .metric-card {
                    background: linear-gradient(145deg, #0d1117, #161b22);
                    border: 1px solid #30363d;
                    border-top: 4px solid #D4AF37;
                    border-radius: 15px;
                    padding: 25px 10px;
                    text-align: center;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
                }
                .metric-title {
                    color: #8b949e;
                    font-size: 0.9rem;
                    font-weight: bold;
                    text-transform: uppercase;
                    letter-spacing: 1.2px;
                    margin-bottom: 10px;
                }
                .metric-value {
                    color: #D4AF37;
                    font-size: 3rem;
                    font-weight: 900;
                    margin: 0;
                    font-family: 'Arial Black', sans-serif;
                }
                </style>
            """, unsafe_allow_html=True)

            # Renderizado de métricas
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Evaluaciones</p><p class="metric-value">{total_eval}</p></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Promedio</p><p class="metric-value">{promedio:.1f}%</p></div>', unsafe_allow_html=True)
            with m3:
                color_tasa = "#2ecc71" if porcentaje_exito >= 70 else "#e74c3c"
                st.markdown(f'<div class="metric-card"><p class="metric-title">Tasa Éxito</p><p class="metric-value" style="color: {color_tasa};">{porcentaje_exito:.1f}%</p></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Agentes</p><p class="metric-value">{df_all["funcionario"].nunique()}</p></div>', unsafe_allow_html=True)

            # Pestañas de análisis
            tab_rend, tab_detalles = st.tabs(["📊 Análisis de Rendimiento", "🔍 Detalle por Agente"])

            with tab_rend:
                self._show_performance_analysis(df_all)
            
            with tab_detalles:
                self._show_agent_details(df_all)

            # Alertas
            self._show_alerts(df_all)
            
        except Exception as e:
            logger.error(f"Error al procesar datos del dashboard: {e}")
            st.error("Error al procesar los datos del dashboard")
    
    def _show_performance_analysis(self, df_all: pd.DataFrame):
        """Muestra el análisis de rendimiento"""
        try:
            c1, c2 = st.columns([1.2, 0.8])
            with c1:
                st.subheader("Promedio por Componente Educativo")
                chart_data = df_all.groupby('modulo')['nota'].mean().reset_index()
                st.bar_chart(data=chart_data, x='modulo', y='nota', color="#D4AF37", use_container_width=True)
            
            with c2:
                st.subheader("Distribución de Niveles")
                bins = [0, 69, 89, 100]
                labels = ['Insuficiente (0-69)', 'Satisfactorio (70-89)', 'Sobresaliente (90-100)']
                df_all['Nivel'] = pd.cut(df_all['nota'], bins=bins, labels=labels)
                dist_data = df_all['Nivel'].value_counts()
                st.bar_chart(dist_data, color="#2ecc71")
                
        except Exception as e:
            logger.error(f"Error en análisis de rendimiento: {e}")
            st.error("Error al mostrar el análisis de rendimiento")
    
    def _show_agent_details(self, df_all: pd.DataFrame):
        """Muestra los detalles por agente"""
        try:
            col_filtro, col_descarga = st.columns([3, 1])
            with col_filtro:
                search = st.text_input("🔍 Buscar funcionario...", placeholder="Ingrese nombre para filtrar")
            with col_descarga:
                csv = df_all.to_csv(index=False).encode('utf-8')
                st.download_button("Descargar Reporte CSV", data=csv, file_name='reporte_analitico_dipol.csv', use_container_width=True)

            display_df = df_all.copy()
            if search:
                display_df = display_df[display_df['funcionario'].str.contains(search, case=False)]
            
            st.dataframe(
                display_df.sort_values(by='fecha', ascending=False),
                column_config={
                    "nota": st.column_config.ProgressColumn("Calificación", format="%d%%", min_value=0, max_value=100),
                    "fecha_display": "Fecha Registro",
                    "funcionario": "Agente",
                    "modulo": "Módulo Evaluado"
                },
                column_order=("funcionario", "modulo", "nota", "fecha_display"),
                use_container_width=True,
                hide_index=True
            )
            
        except Exception as e:
            logger.error(f"Error en detalles por agente: {e}")
            st.error("Error al mostrar los detalles por agente")
    
    def _show_alerts(self, df_all: pd.DataFrame):
        """Muestra alertas sobre rendimiento bajo"""
        try:
            st.divider()
            low_performers = df_all[df_all['nota'] < 70]
            if not low_performers.empty:
                with st.expander("⚠️ Alerta: Personal con necesidad de refuerzo"):
                    st.warning(f"Se detectaron {len(low_performers)} agentes con rendimiento por debajo del 70% en su última evaluación.")
                    st.table(low_performers[['funcionario', 'modulo', 'nota']])
                    
        except Exception as e:
            logger.error(f"Error en alertas: {e}")
            st.error("Error al mostrar las alertas")

# Función principal de ejecución
def main():
    """Función principal que inicia la aplicación"""
    try:
        app = DIPOLApp()
        app.run()
    except AppError as e:
        logger.error(f"Error de aplicación: {e}")
        st.error(f"Error al iniciar la aplicación: {e}")
    except Exception as e:
        logger.error(f"Error inesperado en main: {e}")
        st.error("Error inesperado al iniciar la aplicación")

if __name__ == "__main__":
    main()
