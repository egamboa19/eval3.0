import axios from 'axios';
import toast from 'react-hot-toast';

// Configuración base de la API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

// Crear instancia de axios
const api = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token a las requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const { response } = error;
    
    if (response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_data');
      window.location.href = '/login';
      toast.error('Sesión expirada. Por favor inicia sesión nuevamente.');
    } else if (response?.status === 403) {
      toast.error('No tienes permisos para realizar esta acción.');
    } else if (response?.status === 404) {
      toast.error('Recurso no encontrado.');
    } else if (response?.status >= 500) {
      toast.error('Error del servidor. Por favor intenta más tarde.');
    } else if (error.code === 'ECONNABORTED') {
      toast.error('Tiempo de espera agotado. Verifica tu conexión.');
    } else if (!navigator.onLine) {
      toast.error('Sin conexión a internet.');
    }
    
    return Promise.reject(error);
  }
);

// Servicios de autenticación
export const authService = {
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Guardar token y datos de usuario
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user_data', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  async logout() {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.warn('Error en logout:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_data');
    }
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  async changePassword(currentPassword, newPassword) {
    const response = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  },

  async verifyToken() {
    const response = await api.get('/auth/verify-token');
    return response.data;
  },

  // Verificar si el usuario está autenticado
  isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return !!token;
  },

  // Obtener datos del usuario desde localStorage
  getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
  },
};

// Servicios de usuarios
export const userService = {
  async getUsers(page = 1, limit = 10, search = '') {
    const params = { page, limit };
    if (search) params.search = search;
    
    const response = await api.get('/users', { params });
    return response.data;
  },

  async getUserById(id) {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },

  async createUser(userData) {
    const response = await api.post('/users', userData);
    return response.data;
  },

  async updateUser(id, userData) {
    const response = await api.put(`/users/${id}`, userData);
    return response.data;
  },

  async deleteUser(id) {
    const response = await api.delete(`/users/${id}`);
    return response.data;
  },

  async updateUserStatus(id, isActive) {
    const response = await api.patch(`/users/${id}/status`, { is_active: isActive });
    return response.data;
  },
};

// Servicios de encuestas
export const surveyService = {
  async getSurveys(page = 1, limit = 10) {
    const response = await api.get('/surveys', { 
      params: { page, limit } 
    });
    return response.data;
  },

  async getSurveyById(id) {
    const response = await api.get(`/surveys/${id}`);
    return response.data;
  },

  async createSurvey(surveyData) {
    const response = await api.post('/surveys', surveyData);
    return response.data;
  },

  async updateSurvey(id, surveyData) {
    const response = await api.put(`/surveys/${id}`, surveyData);
    return response.data;
  },

  async deleteSurvey(id) {
    const response = await api.delete(`/surveys/${id}`);
    return response.data;
  },

  async getSurveyQuestions(surveyId) {
    const response = await api.get(`/surveys/${surveyId}/questions`);
    return response.data;
  },
};

// Servicios de evaluaciones
export const evaluationService = {
  async getEvaluations(page = 1, limit = 10, filters = {}) {
    const params = { page, limit, ...filters };
    const response = await api.get('/evaluations', { params });
    return response.data;
  },

  async getEvaluationById(id) {
    const response = await api.get(`/evaluations/${id}`);
    return response.data;
  },

  async startEvaluation(assignmentId) {
    const response = await api.post(`/evaluations/start/${assignmentId}`);
    return response.data;
  },

  async saveEvaluationAnswers(evaluationId, answers) {
    const response = await api.post(`/evaluations/${evaluationId}/answers`, { answers });
    return response.data;
  },

  async completeEvaluation(evaluationId) {
    const response = await api.post(`/evaluations/${evaluationId}/complete`);
    return response.data;
  },

  async getMyEvaluations() {
    const response = await api.get('/evaluations/my-evaluations');
    return response.data;
  },

  async getPendingAssignments() {
    const response = await api.get('/evaluations/pending-assignments');
    return response.data;
  },
};

// Servicios de dashboard
export const dashboardService = {
  async getAdminStats() {
    const response = await api.get('/dashboard/admin-stats');
    return response.data;
  },

  async getCoordinatorStats() {
    const response = await api.get('/dashboard/coordinator-stats');
    return response.data;
  },

  async getTeacherStats() {
    const response = await api.get('/dashboard/teacher-stats');
    return response.data;
  },

  async getEvaluationComparisons(filters = {}) {
    const response = await api.get('/dashboard/comparisons', { params: filters });
    return response.data;
  },
};

// Servicios de configuración
export const configService = {
  async getSystemConfig() {
    const response = await api.get('/config');
    return response.data;
  },

  async updateSystemConfig(config) {
    const response = await api.put('/config', config);
    return response.data;
  },

  async getInstitutionInfo() {
    const response = await axios.get(`${API_BASE_URL}/config`);
    return response.data;
  },
};

// Servicios de departamentos
export const departmentService = {
  async getDepartments() {
    const response = await api.get('/departments');
    return response.data;
  },

  async createDepartment(departmentData) {
    const response = await api.post('/departments', departmentData);
    return response.data;
  },

  async updateDepartment(id, departmentData) {
    const response = await api.put(`/departments/${id}`, departmentData);
    return response.data;
  },

  async deleteDepartment(id) {
    const response = await api.delete(`/departments/${id}`);
    return response.data;
  },
};

// Servicios de reportes
export const reportService = {
  async generateEvaluationReport(filters = {}) {
    const response = await api.get('/reports/evaluation-report', { 
      params: filters,
      responseType: 'blob'
    });
    return response.data;
  },

  async generateComparisonReport(filters = {}) {
    const response = await api.get('/reports/comparison-report', { 
      params: filters,
      responseType: 'blob'
    });
    return response.data;
  },

  async exportEvaluationData(format = 'excel', filters = {}) {
    const response = await api.get('/reports/export', { 
      params: { format, ...filters },
      responseType: 'blob'
    });
    return response.data;
  },
};

// Utility functions
export const apiUtils = {
  // Función para descargar archivos blob
  downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  },

  // Función para formatear errores de la API
  formatApiError(error) {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    } else if (error.response?.data?.message) {
      return error.response.data.message;
    } else if (error.message) {
      return error.message;
    } else {
      return 'Error desconocido';
    }
  },

  // Función para verificar conectividad
  async checkConnection() {
    try {
      await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 });
      return true;
    } catch (error) {
      return false;
    }
  },
};

export default api;