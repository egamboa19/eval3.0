import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Configurar axios con la URL base del backend
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Configurar interceptor para incluir token automáticamente
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_data');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoginLoading, setIsLoginLoading] = useState(false);

  // Verificar si hay un token guardado al cargar la aplicación
  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('access_token');
      const userData = localStorage.getItem('user_data');

      if (token && userData) {
        try {
          // Verificar que el token sigue siendo válido
          const response = await axios.get(`${API_BASE_URL}/auth/me`);
          setUser(response.data);
        } catch (error) {
          console.error('Token inválido:', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_data');
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    setIsLoginLoading(true);
    try {
      // Crear FormData como espera el backend
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      if (response.data.access_token) {
        // Guardar token y datos de usuario
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user_data', JSON.stringify(response.data.user));
        setUser(response.data.user);
        
        return { success: true, user: response.data.user };
      }
    } catch (error) {
      console.error('Error de login:', error);
      const errorMessage = error.response?.data?.detail || 'Error de conexión al servidor';
      return { success: false, error: errorMessage };
    } finally {
      setIsLoginLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Notificar al backend del logout
      await axios.post(`${API_BASE_URL}/auth/logout`);
    } catch (error) {
      console.error('Error en logout:', error);
    } finally {
      // Limpiar datos locales
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_data');
      setUser(null);
    }
  };

  const getCurrentUser = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/auth/me`);
      setUser(response.data);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo usuario:', error);
      return null;
    }
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      await axios.post(`${API_BASE_URL}/auth/change-password`, {
        current_password: currentPassword,
        new_password: newPassword,
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error cambiando contraseña';
      return { success: false, error: errorMessage };
    }
  };

  // Funciones de utilidad para roles
  const isAdmin = () => user?.role === 'admin';
  const isCoordinator = () => user?.role === 'coordinador';
  const isTeacher = () => user?.role === 'maestro';
  const isAuthenticated = () => !!user;

  const canAccessAdminPanel = () => isAdmin();
  const canAccessCoordinatorPanel = () => isAdmin() || isCoordinator();

  const value = {
    // Estado
    user,
    isLoading,
    isLoginLoading,
    
    // Funciones de autenticación
    login,
    logout,
    getCurrentUser,
    changePassword,
    
    // Funciones de utilidad
    isAuthenticated,
    isAdmin,
    isCoordinator,
    isTeacher,
    canAccessAdminPanel,
    canAccessCoordinatorPanel,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};