import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

function LoadingSpinner({ 
  size = 'md', 
  text = null, 
  className = '',
  fullScreen = false 
}) {
  const { isDark } = useTheme();

  // Configuración de tamaños
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
  };

  const spinnerClass = `
    ${sizeClasses[size]} 
    border-2 
    ${isDark() ? 'border-gray-600' : 'border-gray-300'}
    ${isDark() ? 'border-t-blue-400' : 'border-t-blue-600'}
    rounded-full 
    animate-spin
    ${className}
  `;

  const content = (
    <div className="flex flex-col items-center justify-center space-y-3">
      <div className={spinnerClass}></div>
      {text && (
        <p className={`${textSizeClasses[size]} text-gray-600 dark:text-gray-400 animate-pulse`}>
          {text}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 flex items-center justify-center z-50">
        {content}
      </div>
    );
  }

  return content;
}

// Variantes específicas para casos comunes
export function PageLoadingSpinner({ text = "Cargando..." }) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <LoadingSpinner size="lg" text={text} />
    </div>
  );
}

export function ButtonLoadingSpinner({ size = 'sm' }) {
  return <LoadingSpinner size={size} />;
}

export function TableLoadingSpinner() {
  return (
    <div className="flex justify-center py-8">
      <LoadingSpinner size="md" text="Cargando datos..." />
    </div>
  );
}

export function CardLoadingSpinner({ text = "Cargando..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <LoadingSpinner size="md" text={text} />
    </div>
  );
}

export default LoadingSpinner;