"""
Archivo de Configuración
Variables de configuración centralizadas para la aplicación
"""

import os
from typing import Dict, Any

class Config:
    """Clase de configuración centralizada"""
    
    # Configuración de la aplicación
    APP_TITLE = "Plataforma Educativa DIPOL"
    APP_ICON = "🛡️"
    APP_LAYOUT = "wide"
    
    # Configuración de caché
    CACHE_TTL = 60  # segundos
    
    # Configuración de base de datos
    DB_SECRETS_PATH = "connections.postgresql"
    
    # Configuración de estilos
    CSS_FILE = "styles.css"
    
    # Configuración de módulos
    MODULOS_DISPONIBLES = [
        "Módulo 1: Conceptualización",
        "Módulo 2: Ciclo de Inteligencia", 
        "Módulo 3: Recolección",
        "Módulo 4: Tratamiento",
        "Módulo 5: Análisis",
        "Módulo 6: Comunicación",
        "Módulo 7: Evaluación"
    ]
    
    # Configuración de autenticación
    # NOTA: En producción, estas credenciales deberían estar en variables de entorno
    CREDENCIALES = {
        "admin": {
            "usuario": os.getenv("ADMIN_USER", "Jsantos"),
            "clave": os.getenv("ADMIN_PASS", "Inteligencia2026")
        },
        "estudiante": {
            "usuario": os.getenv("STUDENT_USER", "User"),
            "clave": os.getenv("STUDENT_PASS", "ESTUDIANTE2026")
        }
    }
    
    # Configuración de logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de sesión
    SESSION_DEFAULTS = {
        'autenticado': False,
        'agente_nombre': "",
        'es_admin': False,
        'modo_examen': False,
        'modulo_seleccionado': "Módulo 1: Conceptualización",
        'menu_seccion': "🏠 Inicio"
    }
    
    # Configuración de UI
    HOME_MODULES = [
        {"id": "M1", "tit": "Módulo 1", "sub": "Conceptualización", "icon": "📖", "full": "Módulo 1: Conceptualización"},
        {"id": "M2", "tit": "Módulo 2", "sub": "Ciclo de Inteligencia", "icon": "🔄", "full": "Módulo 2: Ciclo de Inteligencia"},
        {"id": "M3", "tit": "Módulo 3", "sub": "Recolección", "icon": "🕵️", "full": "Módulo 3: Recolección"},
        {"id": "M4", "tit": "Módulo 4", "sub": "Tratamiento", "icon": "📊", "full": "Módulo 4: Tratamiento"},
        {"id": "M5", "tit": "Módulo 5", "sub": "Análisis", "icon": "🧠", "full": "Módulo 5: Análisis"},
        {"id": "M6", "tit": "Módulo 6", "sub": "Comunicación", "icon": "📢", "full": "Módulo 6: Comunicación"},
        {"id": "M7", "tit": "Módulo 7", "sub": "Evaluación", "icon": "🔄", "full": "Módulo 7: Evaluación"}
    ]
    
    # Configuración de colores y estilos
    COLORS = {
        "primary": "#00f0ff",
        "secondary": "#D4AF37", 
        "success": "#00e676",
        "warning": "#f1c40f",
        "error": "#ff1744",
        "background": "#000000",
        "card_bg": "#0a0a0f"
    }
    
    @classmethod
    def get_db_secrets_path(cls) -> str:
        """Retorna la ruta de los secretos de la base de datos"""
        return cls.DB_SECRETS_PATH
    
    @classmethod
    def get_credentials(cls, user_type: str) -> Dict[str, str]:
        """Retorna las credenciales para un tipo de usuario"""
        return cls.CREDENCIALES.get(user_type, {})
    
    @classmethod
    def is_production(cls) -> bool:
        """Verifica si estamos en entorno de producción"""
        return os.getenv("ENVIRONMENT", "development") == "production"
    
    @classmethod
    def get_cache_ttl(cls) -> int:
        """Retorna el TTL para caché"""
        return cls.CACHE_TTL

# Variables globales de configuración
config = Config()
