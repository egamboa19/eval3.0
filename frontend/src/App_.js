import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

// Contexts
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';

// Components
import ProtectedRoute from './components/auth/ProtectedRoute';
import Layout from './components/layout/Layout';
import LoadingSpinner from './components/common/LoadingSpinner';

// Pages
import Login from './pages/Login';
import AdminDashboard from './pages/admin/Dashboard';
import CoordinatorDashboard from './pages/coordinator/Dashboard';
import TeacherDashboard from './pages/teacher/Dashboard';
import NotFound from './pages/NotFound';

// Lazy loading para optimización
const AdminUsers = React.lazy(() => import('./pages/admin/Users'));
const AdminSurveys = React.lazy(() => import('./pages/admin/Surveys'));
const AdminReports = React.lazy(() => import('./pages/admin/Reports'));
const CoordinatorEvaluations = React.lazy(() => import('./pages/coordinator/Evaluations'));
const TeacherEvaluations = React.lazy(() => import('./pages/teacher/Evaluations'));
const Profile = React.lazy(() => import('./pages/common/Profile'));

// Configuración de React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
    mutations: {
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <Router>
            <div className="App min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
              {/* Configuración de toasts */}
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  className: 'dark:bg-gray-800 dark:text-white',
                  success: {
                    className: 'dark:bg-green-800 dark:text-green-100',
                  },
                  error: {
                    className: 'dark:bg-red-800 dark:text-red-100',
                  },
                }}
              />

              <Routes>
                {/* Ruta pública de login */}
                <Route path="/login" element={<Login />} />

                {/* Rutas protegidas con layout */}
                <Route path="/" element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }>
                  {/* Redireccionamiento automático basado en rol */}
                  <Route index element={<Navigate to="/dashboard" replace />} />

                  {/* Dashboard dinámico */}
                  <Route path="dashboard" element={<DynamicDashboard />} />

                  {/* Rutas de administrador */}
                  <Route path="admin" element={
                    <ProtectedRoute requiredRole="admin">
                      <React.Suspense fallback={<LoadingSpinner />}>
                        <Routes>
                          <Route path="dashboard" element={<AdminDashboard />} />
                          <Route path="users" element={<AdminUsers />} />
                          <Route path="surveys" element={<AdminSurveys />} />
                          <Route path="reports" element={<AdminReports />} />
                        </Routes>
                      </React.Suspense>
                    </ProtectedRoute>
                  } />

                  {/* Rutas de coordinador */}
                  <Route path="coordinator" element={
                    <ProtectedRoute requiredRoles={["admin", "coordinador"]}>
                      <React.Suspense fallback={<LoadingSpinner />}>
                        <Routes>
                          <Route path="dashboard" element={<CoordinatorDashboard />} />
                          <Route path="evaluations" element={<CoordinatorEvaluations />} />
                        </Routes>
                      </React.Suspense>
                    </ProtectedRoute>
                  } />

                  {/* Rutas de maestro */}
                  <Route path="teacher" element={
                    <ProtectedRoute requiredRole="maestro">
                      <React.Suspense fallback={<LoadingSpinner />}>
                        <Routes>
                          <Route path="dashboard" element={<TeacherDashboard />} />
                          <Route path="evaluations" element={<TeacherEvaluations />} />
                        </Routes>
                      </React.Suspense>
                    </ProtectedRoute>
                  } />

                  {/* Rutas comunes */}
                  <Route path="profile" element={
                    <React.Suspense fallback={<LoadingSpinner />}>
                      <Profile />
                    </React.Suspense>
                  } />
                </Route>

                {/* Ruta 404 */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </div>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

// Componente para dashboard dinámico basado en rol
function DynamicDashboard() {
  const { user, isAdmin, isCoordinator, isTeacher } = useAuth();

  if (!user) {
    return <LoadingSpinner />;
  }

  // Redirigir al dashboard apropiado según el rol
  if (isAdmin()) {
    return <Navigate to="/admin/dashboard" replace />;
  } else if (isCoordinator()) {
    return <Navigate to="/coordinator/dashboard" replace />;
  } else if (isTeacher()) {
    return <Navigate to="/teacher/dashboard" replace />;
  } else {
    return <Navigate to="/login" replace />;
  }
}

// Componente Login simple por ahora
function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sistema de Evaluación Docente
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Prepa 25
          </p>
        </div>
        <form className="mt-8 space-y-6">
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                type="email"
                required
                className="relative block w-full px-3 py-2 border border-gray-300 rounded-t-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Email"
                defaultValue="admin@prepa25.com.mx"
              />
            </div>
            <div>
              <input
                type="password"
                required
                className="relative block w-full px-3 py-2 border border-gray-300 rounded-b-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Password"
                defaultValue="admin123"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Iniciar Sesión
            </button>
          </div>
        </form>
        
        <div className="mt-6 p-4 bg-blue-50 rounded-md">
          <h3 className="text-sm font-medium text-blue-800">Credenciales de Prueba:</h3>
          <p className="text-sm text-blue-600">Email: admin@prepa25.com.mx</p>
          <p className="text-sm text-blue-600">Password: admin123</p>
        </div>
      </div>
    </div>
  );
}

// Hook para usar autenticación (simplificado por ahora)
function useAuth() {
  return {
    user: null,
    isAdmin: () => false,
    isCoordinator: () => false,
    isTeacher: () => false
  };
}

export default App;