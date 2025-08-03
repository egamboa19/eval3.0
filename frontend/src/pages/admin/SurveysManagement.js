// frontend/src/pages/admin/SurveysManagement.js

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';

const SurveysManagement = () => {
  const { user, isAdmin, isCoordinator } = useAuth();
  const [surveys, setSurveys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Estados para filtros y búsqueda
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalSurveys, setTotalSurveys] = useState(0);
  const limit = 10;
  
  // Estados para el modal de encuesta
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState('create'); // 'create', 'edit', 'view'
  const [selectedSurvey, setSelectedSurvey] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    instructions: '',
    is_active: true,
    questions: []
  });

  // Estados para el modal de confirmación
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [confirmAction, setConfirmAction] = useState(null);
  const [confirmData, setConfirmData] = useState({
    title: '',
    message: '',
    confirmText: '',
    cancelText: 'Cancelar',
    type: 'danger'
  });

  // Cargar encuestas al inicio y cuando cambien filtros
  useEffect(() => {
    loadSurveys();
  }, [currentPage, search, statusFilter]);

  const loadSurveys = async () => {
    try {
      setLoading(true);
      const params = {
        skip: (currentPage - 1) * limit,
        limit: limit
      };
      
      if (search) params.search = search;
      if (statusFilter !== '') params.is_active = statusFilter === 'true';

      const response = await axios.get('/surveys/', { params });
      setSurveys(response.data.surveys);
      setTotalSurveys(response.data.total);
    } catch (error) {
      setError('Error cargando encuestas');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Funciones de confirmación
  const showConfirmation = (title, message, onConfirm, type = 'danger', confirmText = 'Confirmar') => {
    setConfirmData({ title, message, confirmText, cancelText: 'Cancelar', type });
    setConfirmAction(() => onConfirm);
    setShowConfirmModal(true);
  };

  const handleConfirm = () => {
    if (confirmAction) confirmAction();
    setShowConfirmModal(false);
    setConfirmAction(null);
  };

  const handleCancel = () => {
    setShowConfirmModal(false);
    setConfirmAction(null);
  };

  // Funciones de búsqueda y filtros
  const handleSearch = (e) => {
    setSearch(e.target.value);
    setCurrentPage(1);
  };

  const handleFilterChange = (value) => {
    setStatusFilter(value);
    setCurrentPage(1);
  };

  // Funciones del modal
  const openCreateModal = () => {
    setModalMode('create');
    setFormData({
      title: '',
      description: '',
      instructions: '',
      is_active: true,
      questions: []
    });
    setSelectedSurvey(null);
    setShowModal(true);
  };

  const openEditModal = async (survey) => {
    try {
      // Cargar encuesta completa con preguntas
      const response = await axios.get(`/surveys/${survey.id}`);
      setModalMode('edit');
      setFormData({
        title: response.data.title,
        description: response.data.description || '',
        instructions: response.data.instructions || '',
        is_active: response.data.is_active,
        questions: response.data.questions || []
      });
      setSelectedSurvey(response.data);
      setShowModal(true);
    } catch (error) {
      setError('Error cargando detalles de la encuesta');
    }
  };

  const openViewModal = async (survey) => {
    try {
      const response = await axios.get(`/surveys/${survey.id}`);
      setModalMode('view');
      setSelectedSurvey(response.data);
      setShowModal(true);
    } catch (error) {
      setError('Error cargando detalles de la encuesta');
    }
  };

  // Función para guardar encuesta
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = { ...formData };

      if (modalMode === 'create') {
        await axios.post('/surveys/', submitData);
      } else {
        await axios.put(`/surveys/${selectedSurvey.id}`, submitData);
      }

      setShowModal(false);
      await loadSurveys();
      setError('');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error guardando encuesta');
    }
  };

  // Función para cambiar estado de encuesta
  const toggleSurveyStatus = async (surveyId, currentStatus) => {
    const actionText = currentStatus ? 'desactivar' : 'activar';
    const survey = surveys.find(s => s.id === surveyId);
    
    showConfirmation(
      `${currentStatus ? 'Desactivar' : 'Activar'} Encuesta`,
      `¿Estás seguro de ${actionText} la encuesta "${survey?.title}"?`,
      async () => {
        try {
          await axios.patch(`/surveys/${surveyId}/toggle-status`);
          loadSurveys();
          setError('');
        } catch (error) {
          setError(error.response?.data?.detail || 'Error cambiando estado');
        }
      },
      currentStatus ? 'danger' : 'success',
      currentStatus ? 'Desactivar' : 'Activar'
    );
  };

  // Funciones para manejo de preguntas
  const addQuestion = () => {
    const newQuestion = {
      question_text: '',
      question_type: 'scale',
      is_required: true,
      min_value: 1,
      max_value: 10,

      order_number: formData.questions.length + 1
    };
    setFormData({
      ...formData,
      questions: [...formData.questions, newQuestion]
    });
  };

  const updateQuestion = (index, field, value) => {
    const updatedQuestions = [...formData.questions];
    updatedQuestions[index] = { ...updatedQuestions[index], [field]: value };
    setFormData({ ...formData, questions: updatedQuestions });
  };

  const removeQuestion = (index) => {
    const updatedQuestions = formData.questions.filter((_, i) => i !== index);
    // Reordenar números
    updatedQuestions.forEach((q, i) => q.order_number = i + 1);
    setFormData({ ...formData, questions: updatedQuestions });
  };

  const moveQuestion = (index, direction) => {
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= formData.questions.length) return;

    const updatedQuestions = [...formData.questions];
    [updatedQuestions[index], updatedQuestions[newIndex]] = [updatedQuestions[newIndex], updatedQuestions[index]];
    
    // Actualizar order_number
    updatedQuestions.forEach((q, i) => q.order_number = i + 1);
    
    setFormData({ ...formData, questions: updatedQuestions });
  };

  const totalPages = Math.ceil(totalSurveys / limit);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto py-6 px-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Gestión de Encuestas
        </h1>
        <p className="text-gray-600">
          Administra encuestas de evaluación - {totalSurveys} encuestas totales
        </p>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* Controles superiores */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          {/* Búsqueda */}
          <div className="flex-1 max-w-md">
            <input
              type="text"
              placeholder="Buscar por título o descripción..."
              value={search}
              onChange={handleSearch}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Filtros */}
          <div className="flex gap-3">
            <select
              value={statusFilter}
              onChange={(e) => handleFilterChange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los estados</option>
              <option value="true">Activas</option>
              <option value="false">Inactivas</option>
            </select>
          </div>

          {/* Botón crear */}
          {(isAdmin() || isCoordinator()) && (
            <button
              onClick={openCreateModal}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center"
            >
              <span className="mr-2">+</span>
              Crear Encuesta
            </button>
          )}
        </div>
      </div>

      {/* Tabla de encuestas */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Encuesta
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Preguntas
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Creada
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {surveys.map((survey) => (
                <tr key={survey.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {survey.title}
                      </div>
                      {survey.description && (
                        <div className="text-sm text-gray-500 mt-1 line-clamp-2">
                          {survey.description}
                        </div>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {survey.questions?.length || 0} preguntas
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      survey.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {survey.is_active ? 'Activa' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(survey.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => openViewModal(survey)}
                        className="text-indigo-600 hover:text-indigo-900"
                      >
                        Ver
                      </button>
                      <button
                        onClick={() => openEditModal(survey)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Editar
                      </button>
                      {(isAdmin() || isCoordinator()) && (
                        <button
                          onClick={() => toggleSurveyStatus(survey.id, survey.is_active)}
                          className={`${
                            survey.is_active ? 'text-orange-600 hover:text-orange-900' : 'text-green-600 hover:text-green-900'
                          }`}
                        >
                          {survey.is_active ? 'Desactivar' : 'Activar'}
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Paginación */}
        {totalPages > 1 && (
          <div className="bg-white px-4 py-3 border-t border-gray-200 flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Mostrando {(currentPage - 1) * limit + 1} a {Math.min(currentPage * limit, totalSurveys)} de {totalSurveys} encuestas
            </div>
            <div className="flex gap-1">
              <button
                onClick={() => setCurrentPage(1)}
                disabled={currentPage === 1}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded disabled:opacity-50"
              >
                Primera
              </button>
              <button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded disabled:opacity-50"
              >
                Anterior
              </button>
              <span className="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded">
                {currentPage} de {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded disabled:opacity-50"
              >
                Siguiente
              </button>
              <button
                onClick={() => setCurrentPage(totalPages)}
                disabled={currentPage === totalPages}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded disabled:opacity-50"
              >
                Última
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modal de crear/editar/ver encuesta */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {modalMode === 'create' ? 'Crear Encuesta' : 
               modalMode === 'edit' ? 'Editar Encuesta' : 'Ver Encuesta'}
            </h2>
            
            {modalMode === 'view' ? (
              // Vista de solo lectura
              <div className="space-y-6">
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{selectedSurvey?.title}</h3>
                    {selectedSurvey?.description && (
                      <p className="text-gray-600 mt-2">{selectedSurvey.description}</p>
                    )}
                    {selectedSurvey?.instructions && (
                      <div className="mt-4">
                        <h4 className="font-medium text-gray-700">Instrucciones:</h4>
                        <p className="text-gray-600 mt-1">{selectedSurvey.instructions}</p>
                      </div>
                    )}
                  </div>
                </div>

                {selectedSurvey?.questions && selectedSurvey.questions.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-3">
                      Preguntas ({selectedSurvey.questions.length})
                    </h4>
                    <div className="space-y-3">
                      {selectedSurvey.questions.map((question, index) => (
                        <div key={question.id || index} className="p-4 bg-gray-50 rounded-lg">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <span className="text-sm font-medium text-gray-500">
                                Pregunta {question.order_number}
                              </span>
                              <p className="text-gray-800 mt-1">{question.question_text}</p>
                              <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                                <span>Tipo: {question.question_type}</span>
                                {question.question_type === 'scale' && (
                                  <span>Escala: {question.min_value} - {question.max_value}</span>
                                )}
                                <span>{question.is_required ? 'Obligatoria' : 'Opcional'}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex justify-end">
                  <button
                    onClick={() => setShowModal(false)}
                    className="bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded transition-colors"
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            ) : (
              // Formulario de crear/editar
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Información básica */}
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Título de la Encuesta *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.title}
                      onChange={(e) => setFormData({...formData, title: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                      placeholder="Ej: Evaluación Docente 2024"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Descripción
                    </label>
                    <textarea
                      rows={3}
                      value={formData.description}
                      onChange={(e) => setFormData({...formData, description: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                      placeholder="Breve descripción del propósito de la encuesta..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Instrucciones
                    </label>
                    <textarea
                      rows={4}
                      value={formData.instructions}
                      onChange={(e) => setFormData({...formData, instructions: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                      placeholder="Instrucciones detalladas para completar la encuesta..."
                    />
                  </div>

                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="is_active"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
                      Encuesta activa
                    </label>
                  </div>
                </div>

                {/* Sección de preguntas */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Preguntas ({formData.questions.length})
                    </h3>
                    <button
                      type="button"
                      onClick={addQuestion}
                      className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm transition-colors"
                    >
                      + Agregar Pregunta
                    </button>
                  </div>

                  {formData.questions.length === 0 ? (
                    <div className="text-center py-8 bg-gray-50 rounded-lg">
                      <p className="text-gray-500">No hay preguntas agregadas</p>
                      <button
                        type="button"
                        onClick={addQuestion}
                        className="mt-2 text-blue-600 hover:text-blue-800"
                      >
                        Agregar la primera pregunta
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {formData.questions.map((question, index) => (
                        <div key={index} className="p-4 border border-gray-200 rounded-lg">
                          <div className="flex items-start justify-between mb-3">
                            <span className="text-sm font-medium text-gray-500">
                              Pregunta {index + 1}
                            </span>
                            <div className="flex gap-1">
                              <button
                                type="button"
                                onClick={() => moveQuestion(index, 'up')}
                                disabled={index === 0}
                                className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-50"
                              >
                                ↑
                              </button>
                              <button
                                type="button"
                                onClick={() => moveQuestion(index, 'down')}
                                disabled={index === formData.questions.length - 1}
                                className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-50"
                              >
                                ↓
                              </button>
                              <button
                                type="button"
                                onClick={() => removeQuestion(index)}
                                className="p-1 text-red-400 hover:text-red-600"
                              >
                                ✕
                              </button>
                            </div>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <div className="md:col-span-2">
                              <input
                                type="text"
                                placeholder="Texto de la pregunta..."
                                value={question.question_text}
                                onChange={(e) => updateQuestion(index, 'question_text', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                              />
                            </div>
                            <div>
                              <select
                                value={question.question_type}
                                onChange={(e) => updateQuestion(index, 'question_type', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                              >
                                <option value="scale">Escala (1-10)</option>
                                <option value="text">Texto libre</option>
                                <option value="yes_no">Sí/No</option>
                                <option value="multiple_choice">Opción múltiple</option>
                              </select>
                            </div>
                          </div>

                          {question.question_type === 'scale' && (
                            <div className="grid grid-cols-2 gap-3 mt-3">
                              <div>
                                <label className="block text-xs text-gray-500 mb-1">Valor mínimo</label>
                                <input
                                  type="number"
                                  min="1"
                                  max="10"
                                  value={question.min_value}
                                  onChange={(e) => updateQuestion(index, 'min_value', parseInt(e.target.value))}
                                  className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                                />
                              </div>
                              <div>
                                <label className="block text-xs text-gray-500 mb-1">Valor máximo</label>
                                <input
                                  type="number"
                                  min="1"
                                  max="10"
                                  value={question.max_value}
                                  onChange={(e) => updateQuestion(index, 'max_value', parseInt(e.target.value))}
                                  className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                                />
                              </div>
                            </div>
                          )}

                          <div className="flex items-center mt-3">
                            <input
                              type="checkbox"
                              id={`required_${index}`}
                              checked={question.is_required}
                              onChange={(e) => updateQuestion(index, 'is_required', e.target.checked)}
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                            />
                            <label htmlFor={`required_${index}`} className="ml-2 block text-sm text-gray-700">
                              Pregunta obligatoria
                            </label>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded transition-colors"
                  >
                    {modalMode === 'create' ? 'Crear Encuesta' : 'Actualizar Encuesta'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded transition-colors"
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* Modal de confirmación */}
      {showConfirmModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className={`${
              confirmData.type === 'danger' ? 'bg-red-50' :
              confirmData.type === 'success' ? 'bg-green-50' :
              confirmData.type === 'warning' ? 'bg-yellow-50' : 'bg-gray-50'
            } px-6 py-4 rounded-t-lg`}>
              <div className="flex items-center">
                <div className={`${
                  confirmData.type === 'danger' ? 'bg-red-100 text-red-600' :
                  confirmData.type === 'success' ? 'bg-green-100 text-green-600' :
                  confirmData.type === 'warning' ? 'bg-yellow-100 text-yellow-600' : 'bg-gray-100 text-gray-600'
                } rounded-full p-3 flex items-center justify-center`}>
                  <span className="text-xl">
                    {confirmData.type === 'danger' ? '⚠️' :
                     confirmData.type === 'success' ? '✅' :
                     confirmData.type === 'warning' ? '⚠️' : '❓'}
                  </span>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {confirmData.title}
                  </h3>
                </div>
              </div>
            </div>
            
            <div className="px-6 py-4">
              <p className="text-gray-700 text-sm leading-relaxed">
                {confirmData.message}
              </p>
            </div>
            
            <div className="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end gap-3">
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
              >
                {confirmData.cancelText}
              </button>
              <button
                onClick={handleConfirm}
                className={`px-4 py-2 text-sm font-medium text-white ${
                  confirmData.type === 'danger' ? 'bg-red-600 hover:bg-red-700' :
                  confirmData.type === 'success' ? 'bg-green-600 hover:bg-green-700' :
                  confirmData.type === 'warning' ? 'bg-yellow-600 hover:bg-yellow-700' : 'bg-gray-600 hover:bg-gray-700'
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors`}
              >
                {confirmData.confirmText}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default SurveysManagement;