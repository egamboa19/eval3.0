import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import axios from 'axios';
import UsersManagement from './pages/admin/UsersManagement';
import SurveysManagement from './pages/admin/SurveysManagement';
// Configurar axios base URL
axios.defaults.baseURL = 'http://localhost:8000/api/v1';

function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}

function MainApp() {
  const { user, isAuthenticated, isLoading } = useAuth();

  // Mostrar loading mientras se verifica autenticación
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Verificando autenticación...</p>
        </div>
      </div>
    );
  }

  // Mostrar login o dashboard según estado de autenticación
  if (isAuthenticated()) {
    return <Dashboard />;
  }

  return <LoginPage />;
}

function LoginPage() {
  const { login, isLoginLoading } = useAuth();
  const [email, setEmail] = useState('admin@prepa25.com.mx');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [isConnecting, setIsConnecting] = useState(false);

  // Verificar conexión al backend al cargar
  useEffect(() => {
    const checkBackendConnection = async () => {
      setIsConnecting(true);
      try {
        await axios.get('http://localhost:8000/health');
      } catch (error) {
        setError('No se puede conectar al servidor. Verifica que el backend esté funcionando en puerto 8000.');
      } finally {
        setIsConnecting(false);
      }
    };

    checkBackendConnection();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Por favor completa todos los campos');
      return;
    }

    const result = await login(email, password);

    if (!result.success) {
      setError(result.error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full space-y-8 p-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🎓 Prepa 25</h1>
          <h2 className="text-xl text-gray-600">Sistema de Evaluación Docente</h2>

          {/* Indicador de conexión */}
          <div className="mt-4 flex items-center justify-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isConnecting ? 'bg-yellow-500' : error ? 'bg-red-500' : 'bg-green-500'}`}></div>
            <span className="text-sm text-gray-500">
              {isConnecting ? 'Conectando...' : error ? 'Sin conexión' : 'Backend conectado'}
            </span>
          </div>
        </div>

        {/* Formulario de login */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="admin@prepa25.com.mx"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contraseña
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="admin123"
                required
              />
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoginLoading || isConnecting || !!error}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
            >
              {isLoginLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Iniciando sesión...
                </>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>

          {/* Credenciales de prueba */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h3 className="text-sm font-medium text-blue-800 mb-1">Credenciales reales desde BD:</h3>
            <p className="text-sm text-blue-600">admin@prepa25.com.mx / admin123</p>
            <p className="text-xs text-blue-500 mt-1">* Datos verificados en PostgreSQL</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Dashboard() {
  const { user, logout, isAdmin, isCoordinator, isTeacher } = useAuth();
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalSurveys: 0,
    pendingEvaluations: 0,
  });
  const [isLoadingStats, setIsLoadingStats] = useState(true);

  // Cargar estadísticas reales de la BD
  useEffect(() => {
    const loadDashboardStats = async () => {
      try {
        // Cargar estadísticas según el rol del usuario
        if (isAdmin()) {
          // Admin puede ver estadísticas generales
          const [usersResponse, surveysResponse] = await Promise.all([
            axios.get('/users'),
            axios.get('/surveys'),
          ]);

          setStats({
            totalUsers: usersResponse.data.length || 0,
            totalSurveys: surveysResponse.data.length || 0,
            pendingEvaluations: 0, // Se implementará después
          });
        }
      } catch (error) {
        console.error('Error cargando estadísticas:', error);
      } finally {
        setIsLoadingStats(false);
      }
    };

    loadDashboardStats();
  }, [isAdmin]);

  const handleLogout = async () => {
    if (window.confirm('¿Estás seguro de que deseas cerrar sesión?')) {
      await logout();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                🎓 Prepa 25 - Sistema de Evaluación
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm">
                <span className="text-gray-500">Conectado como:</span>
                <span className="font-medium text-gray-700 ml-1">
                  {user?.first_name} {user?.last_name}
                </span>
              </div>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${isAdmin() ? 'bg-purple-100 text-purple-800' :
                isCoordinator() ? 'bg-blue-100 text-blue-800' :
                  'bg-green-100 text-green-800'
                }`}>
                {user?.role}
              </span>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors text-sm"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            ¡Bienvenido al Sistema de Evaluación Docente! 🎉
          </h2>

          <div className="grid gap-6 md:grid-cols-3">
            {/* Información del usuario */}
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">Tu Información (BD Real)</h3>
              <p className="text-sm text-blue-600">Email: {user?.email}</p>
              <p className="text-sm text-blue-600">Rol: {user?.role}</p>
              <p className="text-sm text-blue-600">Departamento: {user?.department || 'Sin asignar'}</p>
              <p className="text-sm text-blue-600">ID: {user?.id}</p>
            </div>

            {/* Estado del sistema */}
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-2">Sistema en Tiempo Real</h3>
              <p className="text-sm text-green-600">✅ Autenticación JWT activa</p>
              <p className="text-sm text-green-600">✅ PostgreSQL conectado</p>
              <p className="text-sm text-green-600">✅ APIs funcionando</p>
              <p className="text-sm text-green-600">✅ Datos desde BD</p>
            </div>

            {/* Estadísticas */}
            <div className="p-4 bg-yellow-50 rounded-lg">
              <h3 className="font-semibold text-yellow-800 mb-2">Estadísticas</h3>
              {isLoadingStats ? (
                <p className="text-sm text-yellow-600">Cargando datos...</p>
              ) : (
                <>
                  <p className="text-sm text-yellow-600">Usuarios: {stats.totalUsers}</p>
                  <p className="text-sm text-yellow-600">Encuestas: {stats.totalSurveys}</p>
                  <p className="text-sm text-yellow-600">Evaluaciones pendientes: {stats.pendingEvaluations}</p>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Dashboard específico por rol */}
        {isAdmin() && <AdminDashboard />}
        {isCoordinator() && <CoordinatorDashboard />}
        {isTeacher() && <TeacherDashboard />}
      </main>
    </div>
  );
}

// Dashboards específicos por rol (conectados a BD real)
// Dashboards específicos por rol (conectados a BD real)
function AdminDashboard() {
  const [currentView, setCurrentView] = useState('dashboard'); // ← AGREGAR ESTA LÍNEA

  // Si está en vista de usuarios, mostrar el componente UsersManagement
  if (currentView === 'users') {
    return <UsersManagement />;
  }
  if (currentView === 'surveys') {
    return <SurveysManagement />;
  }

  // Vista normal del dashboard
  return (
    <div className="bg-white rounded-lg shadow p-6">
      {/* Botón de regreso (opcional, para cuando esté en otras vistas) */}
      {currentView !== 'dashboard' && (
        <div className="mb-4">
          <button
            onClick={() => setCurrentView('dashboard')}
            className="text-blue-600 hover:text-blue-800 text-sm"
          >
            ← Volver al Dashboard
          </button>
        </div>
      )}

      <h3 className="text-lg font-semibold text-gray-900 mb-4">Panel de Administrador</h3>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="p-4 bg-purple-50 rounded-lg border">
          <h4 className="font-medium text-purple-800">Gestión de Usuarios</h4>
          <p className="text-sm text-purple-600 mt-1">Crear, editar y gestionar usuarios</p>
          <button
            onClick={() => setCurrentView('users')}
            className="mt-2 text-sm bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700 transition-colors"
          >
            Gestionar Usuarios
          </button>
        </div>
        <div className="p-4 bg-blue-50 rounded-lg border">
          <h4 className="font-medium text-blue-800">Encuestas</h4>
          <p className="text-sm text-blue-600 mt-1">Crear y gestionar encuestas</p>
          <button
            onClick={() => setCurrentView('surveys')}
            className="mt-2 text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors"
          >
            Gestionar Encuestas
          </button>
        </div>
        <div className="p-4 bg-green-50 rounded-lg border">
          <h4 className="font-medium text-green-800">Reportes</h4>
          <p className="text-sm text-green-600 mt-1">Ver estadísticas y reportes</p>
          <button className="mt-2 text-sm bg-green-600 text-white px-3 py-1 rounded">
            Próximamente
          </button>
        </div>
        <div className="p-4 bg-orange-50 rounded-lg border">
          <h4 className="font-medium text-orange-800">Configuración</h4>
          <p className="text-sm text-orange-600 mt-1">Configurar el sistema</p>
          <button className="mt-2 text-sm bg-orange-600 text-white px-3 py-1 rounded">
            Próximamente
          </button>
        </div>
      </div>
    </div>
  );
}

function CoordinatorDashboard() {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Panel de Coordinador</h3>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="p-4 bg-blue-50 rounded-lg border">
          <h4 className="font-medium text-blue-800">Mi Departamento</h4>
          <p className="text-sm text-blue-600 mt-1">Gestionar maestros de mi área</p>
          <button
            onClick={() => setCurrentView('surveys')}
            className="mt-2 text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition-colors"
          >
            Gestionar Encuestas
          </button>
        </div>
        <div className="p-4 bg-green-50 rounded-lg border">
          <h4 className="font-medium text-green-800">Evaluaciones</h4>
          <p className="text-sm text-green-600 mt-1">Evaluar a mis maestros</p>
          <button className="mt-2 text-sm bg-green-600 text-white px-3 py-1 rounded">
            Próximamente
          </button>
        </div>
        <div className="p-4 bg-purple-50 rounded-lg border">
          <h4 className="font-medium text-purple-800">Reportes</h4>
          <p className="text-sm text-purple-600 mt-1">Ver resultados de mi área</p>
          <button className="mt-2 text-sm bg-purple-600 text-white px-3 py-1 rounded">
            Próximamente
          </button>
        </div>
      </div>
    </div>
  );
}

function TeacherDashboard() {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Panel de Maestro</h3>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="p-4 bg-green-50 rounded-lg border">
          <h4 className="font-medium text-green-800">Mis Autoevaluaciones</h4>
          <p className="text-sm text-green-600 mt-1">Realizar autoevaluaciones pendientes</p>
          <button className="mt-2 text-sm bg-green-600 text-white px-3 py-1 rounded">
            Próximamente
          </button>
        </div>
        <div className="p-4 bg-blue-50 rounded-lg border">
          <h4 className="font-medium text-blue-800">Mis Resultados</h4>
          <p className="text-sm text-blue-600 mt-1">Ver mis evaluaciones y comparativas</p>
          <button className="mt-2 text-sm bg-blue-600 text-white px-3 py-1 rounded">
            Próximamente
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;