"""
Módulo de Gestión de Base de Datos
Funciones centralizadas para operaciones de base de datos
"""

import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from typing import Optional, Dict, Any
import streamlit as st
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Excepción personalizada para errores de base de datos"""
    pass

class DatabaseManager:
    """Gestor centralizado de operaciones de base de datos"""
    
    def __init__(self):
        self.engine = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Inicializa la conexión a la base de datos"""
        try:
            db_s = st.secrets["connections"]["postgresql"]
            pass_clean = quote_plus(db_s['password'])
            conn_str = f"postgresql://{db_s['username']}:{pass_clean}@{db_s['host']}:{db_s['port']}/{db_s['database']}"
            self.engine = create_engine(conn_str)
            logger.info("Conexión a base de datos establecida exitosamente")
        except KeyError as e:
            logger.error(f"Error de configuración de BD: {e}")
            raise DatabaseError(f"Configuración de base de datos incompleta: {e}")
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise DatabaseError(f"No se pudo conectar a la base de datos: {e}")
    
    @st.cache_data(ttl=60)
    def cargar_datos_agente(self, nombre_agente: str) -> pd.DataFrame:
        """Carga datos de un agente específico con caché"""
        try:
            with self.engine.connect() as conn:
                query = text("SELECT modulo, nota, fecha FROM calificaciones WHERE funcionario = :n ORDER BY fecha DESC")
                return pd.read_sql(query, conn, params={"n": nombre_agente})
        except Exception as e:
            logger.error(f"Error al cargar datos del agente {nombre_agente}: {e}")
            raise DatabaseError(f"No se pudieron cargar los datos del agente: {e}")
    
    @st.cache_data(ttl=60)
    def cargar_todo_admin(self) -> pd.DataFrame:
        """Carga todos los datos para administración con caché"""
        try:
            with self.engine.connect() as conn:
                query = text("SELECT funcionario, modulo, nota, fecha FROM calificaciones")
                return pd.read_sql(query, conn)
        except Exception as e:
            logger.error(f"Error al cargar datos administrativos: {e}")
            raise DatabaseError(f"No se pudieron cargar los datos administrativos: {e}")
    
    def verificar_intento(self, funcionario: str, modulo: str) -> Optional[float]:
        """
        Verifica si el agente ya tiene una nota para este módulo en el último intento.
        Retorna la nota si existe, None en caso contrario.
        """
        try:
            with self.engine.connect() as conn:
                query = text("SELECT nota FROM calificaciones WHERE funcionario = :f AND modulo = :m ORDER BY fecha DESC LIMIT 1")
                result = conn.execute(query, {"f": funcionario, "m": modulo}).fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Error al verificar intento para {funcionario} en {modulo}: {e}")
            raise DatabaseError(f"No se pudo verificar el intento: {e}")
    
    def guardar_calificacion(self, funcionario: str, modulo: str, nota: float) -> bool:
        """
        Guarda una calificación en la base de datos.
        Retorna True si fue exitoso, False en caso contrario.
        """
        try:
            with self.engine.begin() as conn:
                query = text("INSERT INTO calificaciones (funcionario, nota, modulo) VALUES (:f, :n, :m)")
                conn.execute(query, {"f": funcionario, "n": nota, "m": modulo})
                logger.info(f"Calificación guardada: {funcionario} - {modulo} - {nota}%")
                return True
        except Exception as e:
            logger.error(f"Error al guardar calificación para {funcionario} en {modulo}: {e}")
            raise DatabaseError(f"No se pudo guardar la calificación: {e}")
    
    def guardar_calificacion_con_fecha(self, funcionario: str, modulo: str, nota: float, fecha) -> bool:
        """
        Guarda una calificación con fecha específica en la base de datos.
        Retorna True si fue exitoso, False en caso contrario.
        """
        try:
            with self.engine.begin() as conn:
                query = text("INSERT INTO calificaciones (funcionario, modulo, nota, fecha) VALUES (:f, :m, :n, :d)")
                conn.execute(query, {"f": funcionario, "m": modulo, "n": nota, "d": fecha})
                logger.info(f"Calificación guardada con fecha: {funcionario} - {modulo} - {nota}%")
                return True
        except Exception as e:
            logger.error(f"Error al guardar calificación con fecha para {funcionario} en {modulo}: {e}")
            raise DatabaseError(f"No se pudo guardar la calificación con fecha: {e}")
    
    def get_engine(self):
        """Retorna el motor de base de datos"""
        if self.engine is None:
            self._initialize_connection()
        return self.engine

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

# Funciones de compatibilidad para código existente
def cargar_datos_agente(nombre_agente: str) -> pd.DataFrame:
    """Función de compatibilidad para cargar_datos_agente"""
    return db_manager.cargar_datos_agente(nombre_agente)

def cargar_todo_admin() -> pd.DataFrame:
    """Función de compatibilidad para cargar_todo_admin"""
    return db_manager.cargar_todo_admin()

def verificar_intento(funcionario: str, modulo: str, engine=None) -> Optional[float]:
    """Función de compatibilidad para verificar_intento"""
    return db_manager.verificar_intento(funcionario, modulo)

def get_database_engine():
    """Retorna el motor de base de datos"""
    return db_manager.get_engine()
