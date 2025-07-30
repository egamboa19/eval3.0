import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from '../common/LoadingSpinner';

function ProtectedRoute({ 
  children, 
  requiredRole = null, 
  requiredRoles = null,
  redirectTo = '/login' 
}) {
  const { 
    isAuthenticated, 
    isLoading, 
    isInitialized, 
    hasRole, 
    user 
  } = useAuth();

  // Mostrar loading mientras se inicializa la autenticación
  if (!isInitialized || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Redirigir al login si no está autenticado
  if (!isAuthenticated()) {
    return <Navigate to={redirectTo} replace />;
  }

  // Verificar rol específico si se requiere
  if (requiredRole && !hasRole(requiredRole)) {
    // Redirigir al dashboard apropiado según el rol actual
    const userRole = user?.role;
    let dashboardPath = '/dashboard';
    
    switch (userRole) {
      case 'admin':
        dashboardPath = '/admin/dashboard';
        break;
      case 'coordinador':
        dashboardPath = '/coordinator/dashboard';
        break;
      case 'maestro':
        dashboardPath = '/teacher/dashboard';
        break;
      default:
        dashboardPath = '/login';
    }
    
    return <Navigate to={dashboardPath} replace />;
  }

  // Verificar múltiples roles si se especifican
  if (requiredRoles && Array.isArray(requiredRoles)) {
    const hasRequiredRole = requiredRoles.some(role => hasRole(role));
    
    if (!hasRequiredRole) {
      const userRole = user?.role;
      let dashboardPath = '/dashboard';
      
      switch (userRole) {
        case 'admin':
          dashboardPath = '/admin/dashboard';
          break;
        case 'coordinador':
          dashboardPath = '/coordinator/dashboard';
          break;
        case 'maestro':
          dashboardPath = '/teacher/dashboard';
          break;
        default:
          dashboardPath = '/login';
      }
      
      return <Navigate to={dashboardPath} replace />;
    }
  }

  // Si pasa todas las verificaciones, renderizar el componente
  return children;
}

export default ProtectedRoute;