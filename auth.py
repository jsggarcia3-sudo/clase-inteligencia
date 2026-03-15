"""
Módulo de Autenticación y Gestión de Sesiones
Funciones centralizadas para login, logout y gestión de usuarios
"""

import streamlit as st
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AuthenticationError(Exception):
    """Excepción personalizada para errores de autenticación"""
    pass

class AuthenticationManager:
    """Gestor centralizado de autenticación"""
    
    def __init__(self):
        self.credenciales = {
            "admin": {"usuario": "Jsantos", "clave": "Inteligencia2026"},
            "estudiante": {"usuario": "User", "clave": "ESTUDIANTE2026"}
        }
    
    def initialize_session_state(self):
        """Inicializa el estado de sesión si no existe"""
        session_defaults = {
            'autenticado': False,
            'agente_nombre': "",
            'es_admin': False,
            'modo_examen': False,
            'modulo_seleccionado': "Módulo 1: Conceptualización",
            'menu_seccion': "🏠 Inicio"
        }
        
        for key, default_value in session_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def validate_credentials(self, usuario: str, clave: str, nombre: str) -> Dict[str, Any]:
        """
        Valida las credenciales del usuario
        Retorna diccionario con resultado de autenticación
        """
        try:
            # Validación Admin
            if usuario == self.credenciales["admin"]["usuario"] and clave == self.credenciales["admin"]["clave"]:
                return {
                    "success": True,
                    "es_admin": True,
                    "agente_nombre": nombre if nombre else "Admin",
                    "message": "Acceso Administrativo Correcto"
                }
            
            # Validación Estudiante (requiere nombre)
            elif (nombre and 
                  usuario == self.credenciales["estudiante"]["usuario"] and 
                  clave == self.credenciales["estudiante"]["clave"]):
                return {
                    "success": True,
                    "es_admin": False,
                    "agente_nombre": nombre,
                    "message": f"Bienvenido Agente {nombre}"
                }
            
            else:
                return {
                    "success": False,
                    "message": "Credenciales inválidas o campos vacíos"
                }
                
        except Exception as e:
            logger.error(f"Error en validación de credenciales: {e}")
            raise AuthenticationError(f"Error en autenticación: {e}")
    
    def login_user(self, usuario: str, clave: str, nombre: str) -> bool:
        """
        Proceso completo de login del usuario
        Retorna True si el login fue exitoso
        """
        try:
            result = self.validate_credentials(usuario, clave, nombre)
            
            if result["success"]:
                # Actualizar estado de sesión
                st.session_state.update({
                    'autenticado': True,
                    'es_admin': result["es_admin"],
                    'agente_nombre': result["agente_nombre"]
                })
                logger.info(f"Login exitoso: {result['agente_nombre']} - Admin: {result['es_admin']}")
                return True
            else:
                logger.warning(f"Login fallido: {usuario}")
                return False
                
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Error en proceso de login: {e}")
            raise AuthenticationError(f"Error en proceso de autenticación: {e}")
    
    def logout_user(self):
        """Cierra la sesión del usuario"""
        try:
            user_name = st.session_state.get('agente_nombre', 'Usuario')
            st.session_state.clear()
            self.initialize_session_state()  # Reinicializar con valores por defecto
            logger.info(f"Logout exitoso: {user_name}")
        except Exception as e:
            logger.error(f"Error en proceso de logout: {e}")
    
    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado"""
        return st.session_state.get('autenticado', False)
    
    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return st.session_state.get('es_admin', False)
    
    def get_current_user(self) -> str:
        """Retorna el nombre del usuario actual"""
        return st.session_state.get('agente_nombre', 'Usuario No Identificado')
    
    def require_authentication(self):
        """Redirige a login si el usuario no está autenticado"""
        if not self.is_authenticated():
            return False
        return True
    
    def require_admin(self):
        """Verifica si el usuario tiene permisos de administrador"""
        if not self.is_authenticated():
            return False
        return self.is_admin()

# Instancia global del gestor de autenticación
auth_manager = AuthenticationManager()

# Funciones de compatibilidad para código existente
def initialize_session():
    """Inicializa el estado de sesión"""
    auth_manager.initialize_session_state()

def login(usuario: str, clave: str, nombre: str) -> bool:
    """Función de login simplificada"""
    return auth_manager.login_user(usuario, clave, nombre)

def logout():
    """Función de logout simplificada"""
    auth_manager.logout_user()

def is_authenticated() -> bool:
    """Verifica si está autenticado"""
    return auth_manager.is_authenticated()

def is_admin() -> bool:
    """Verifica si es administrador"""
    return auth_manager.is_admin()

def get_current_user() -> str:
    """Retorna el usuario actual"""
    return auth_manager.get_current_user()
