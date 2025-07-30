import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Temas disponibles
const themes = {
  LIGHT: 'light',
  DARK: 'dark',
};

// Acciones del reducer
const themeActions = {
  SET_THEME: 'SET_THEME',
  TOGGLE_THEME: 'TOGGLE_THEME',
  SET_SYSTEM_PREFERENCE: 'SET_SYSTEM_PREFERENCE',
};

// Estado inicial
const initialState = {
  currentTheme: themes.LIGHT,
  systemPreference: 'light',
  useSystemPreference: false,
};

// Reducer para manejar el estado del tema
function themeReducer(state, action) {
  switch (action.type) {
    case themeActions.SET_THEME:
      return {
        ...state,
        currentTheme: action.payload,
        useSystemPreference: false,
      };

    case themeActions.TOGGLE_THEME:
      const newTheme = state.currentTheme === themes.LIGHT ? themes.DARK : themes.LIGHT;
      return {
        ...state,
        currentTheme: newTheme,
        useSystemPreference: false,
      };

    case themeActions.SET_SYSTEM_PREFERENCE:
      return {
        ...state,
        systemPreference: action.payload,
        currentTheme: state.useSystemPreference ? action.payload : state.currentTheme,
      };

    default:
      return state;
  }
}

// Crear contexto
const ThemeContext = createContext(null);

// Provider del contexto de tema
export function ThemeProvider({ children }) {
  const [state, dispatch] = useReducer(themeReducer, initialState);

  // Detectar preferencia del sistema
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      const systemPreference = e.matches ? themes.DARK : themes.LIGHT;
      dispatch({
        type: themeActions.SET_SYSTEM_PREFERENCE,
        payload: systemPreference,
      });
    };

    // Establecer preferencia inicial
    handleChange(mediaQuery);

    // Escuchar cambios
    mediaQuery.addEventListener('change', handleChange);

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, []);

  // Cargar tema guardado al inicializar
  useEffect(() => {
    const savedTheme = localStorage.getItem('app_theme');
    const useSystemPref = localStorage.getItem('use_system_theme') === 'true';

    if (useSystemPref) {
      dispatch({
        type: themeActions.SET_SYSTEM_PREFERENCE,
        payload: state.systemPreference,
      });
    } else if (savedTheme && Object.values(themes).includes(savedTheme)) {
      dispatch({
        type: themeActions.SET_THEME,
        payload: savedTheme,
      });
    }
  }, []);

  // Aplicar tema al DOM
  useEffect(() => {
    const root = document.documentElement;
    
    if (state.currentTheme === themes.DARK) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }

    // Guardar en localStorage si no está usando preferencia del sistema
    if (!state.useSystemPreference) {
      localStorage.setItem('app_theme', state.currentTheme);
    }
  }, [state.currentTheme, state.useSystemPreference]);

  // Función para cambiar tema
  const setTheme = (theme) => {
    if (Object.values(themes).includes(theme)) {
      dispatch({
        type: themeActions.SET_THEME,
        payload: theme,
      });
      localStorage.setItem('app_theme', theme);
      localStorage.setItem('use_system_theme', 'false');
    }
  };

  // Función para alternar tema
  const toggleTheme = () => {
    dispatch({ type: themeActions.TOGGLE_THEME });
    localStorage.setItem('use_system_theme', 'false');
  };

  // Función para usar preferencia del sistema
  const useSystemTheme = () => {
    dispatch({
      type: themeActions.SET_SYSTEM_PREFERENCE,
      payload: state.systemPreference,
    });
    localStorage.setItem('use_system_theme', 'true');
    localStorage.removeItem('app_theme');
  };

  // Funciones de utilidad
  const isDark = () => state.currentTheme === themes.DARK;
  const isLight = () => state.currentTheme === themes.LIGHT;

  // Obtener íconos para el tema
  const getThemeIcon = (theme = state.currentTheme) => {
    switch (theme) {
      case themes.LIGHT:
        return '☀️';
      case themes.DARK:
        return '🌙';
      default:
        return '💡';
    }
  };

  // Obtener nombre del tema
  const getThemeName = (theme = state.currentTheme) => {
    switch (theme) {
      case themes.LIGHT:
        return 'Claro';
      case themes.DARK:
        return 'Oscuro';
      default:
        return 'Desconocido';
    }
  };

  // Valores del contexto
  const contextValue = {
    // Estado
    ...state,
    
    // Temas disponibles
    themes,
    
    // Funciones de tema
    setTheme,
    toggleTheme,
    useSystemTheme,
    
    // Funciones de utilidad
    isDark,
    isLight,
    getThemeIcon,
    getThemeName,
    
    // Estados derivados
    effectiveTheme: state.currentTheme,
    isUsingSystemPreference: state.useSystemPreference,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

// Hook para usar el contexto de tema
export function useTheme() {
  const context = useContext(ThemeContext);
  
  if (!context) {
    throw new Error('useTheme debe ser usado dentro de un ThemeProvider');
  }
  
  return context;
}

// Hook para obtener clases CSS basadas en el tema
export function useThemeClasses() {
  const { isDark } = useTheme();
  
  return {
    // Clases base
    background: isDark() ? 'bg-gray-900' : 'bg-white',
    surface: isDark() ? 'bg-gray-800' : 'bg-gray-50',
    text: isDark() ? 'text-gray-100' : 'text-gray-900',
    textSecondary: isDark() ? 'text-gray-300' : 'text-gray-600',
    border: isDark() ? 'border-gray-700' : 'border-gray-200',
    
    // Componentes específicos
    card: isDark() ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200',
    input: isDark() ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-900',
    button: {
      primary: isDark() ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-600 hover:bg-blue-700',
      secondary: isDark() ? 'bg-gray-700 hover:bg-gray-600 text-gray-100' : 'bg-gray-100 hover:bg-gray-200 text-gray-900',
    },
    
    // Estados
    hover: isDark() ? 'hover:bg-gray-700' : 'hover:bg-gray-50',
    active: isDark() ? 'bg-gray-700' : 'bg-gray-100',
    focus: 'focus:ring-blue-500 focus:border-blue-500',
  };
}

export default ThemeContext;