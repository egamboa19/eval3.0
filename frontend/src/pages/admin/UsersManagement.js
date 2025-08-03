// frontend/src/pages/admin/UsersManagement.js

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';

const UsersManagement = () => {
  const { user, isAdmin, isCoordinator } = useAuth();
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Estados para filtros y búsqueda
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const limit = 10;

  // Estados para el modal de usuario
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState('create'); // 'create' o 'edit'
  const [selectedUser, setSelectedUser] = useState(null);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    employee_code: '',
    phone: '',
    role_id: '',
    department_id: '',
    is_active: true

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
  // Cargar datos iniciales
  useEffect(() => {
    loadInitialData();
  }, []);

  // Cargar usuarios cuando cambien los filtros
  useEffect(() => {
    loadUsers();
  }, [currentPage, search, roleFilter, departmentFilter, statusFilter]);
  const showConfirmation = (title, message, onConfirm, type = 'danger', confirmText = 'Confirmar') => {
    setConfirmData({
      title,
      message,
      confirmText,
      cancelText: 'Cancelar',
      type
    });
    setConfirmAction(() => onConfirm);
    setShowConfirmModal(true);
  };

  // Función para manejar confirmación
  const handleConfirm = () => {
    if (confirmAction) {
      confirmAction();
    }
    setShowConfirmModal(false);
    setConfirmAction(null);
  };

  // Función para cancelar
  const handleCancel = () => {
    setShowConfirmModal(false);
    setConfirmAction(null);
  };

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [rolesRes, departmentsRes] = await Promise.all([
        axios.get('/users/roles/'),
        axios.get('/users/departments/')
      ]);

      setRoles(rolesRes.data);
      setDepartments(departmentsRes.data);
      await loadUsers();
    } catch (error) {
      setError('Error cargando datos iniciales');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const params = {
        skip: (currentPage - 1) * limit,
        limit: limit
      };

      if (search) params.search = search;
      if (roleFilter) params.role = roleFilter;
      if (departmentFilter) params.department_id = departmentFilter;
      if (statusFilter !== '') params.is_active = statusFilter === 'true';

      const response = await axios.get('/users/', { params });
      setUsers(response.data.users);
      setTotalUsers(response.data.total);
    } catch (error) {
      setError('Error cargando usuarios');
      console.error('Error:', error);
    }
  };

  const handleSearch = (e) => {
    setSearch(e.target.value);
    setCurrentPage(1); // Reset a primera página
  };

  const handleFilterChange = (type, value) => {
    setCurrentPage(1);
    switch (type) {
      case 'role':
        setRoleFilter(value);
        break;
      case 'department':
        setDepartmentFilter(value);
        break;
      case 'status':
        setStatusFilter(value);
        break;
    }
  };

  const openCreateModal = () => {
    setModalMode('create');
    setFormData({
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      employee_code: '',
      phone: '',
      role_id: '',
      department_id: '',
      is_active: true
    });
    setSelectedUser(null);
    setShowModal(true);
  };

  const openEditModal = (user) => {
    setModalMode('edit');
    setFormData({
      email: user.email,
      password: '', // No prellenar password
      first_name: user.first_name,
      last_name: user.last_name,
      employee_code: user.employee_code || '',
      phone: user.phone || '',
      role_id: roles.find(r => r.name === user.role)?.id || '',
      department_id: departments.find(d => d.name === user.department)?.id || '',
      is_active: user.is_active
    });
    setSelectedUser(user);
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = { ...formData };

      // No enviar password vacío en edición
      if (modalMode === 'edit' && !submitData.password) {
        delete submitData.password;
      }

      if (modalMode === 'create') {
        await axios.post('/users/', submitData);
      } else {
        await axios.put(`/users/${selectedUser.id}`, submitData);
      }

      setShowModal(false);
      loadUsers();
      setError('');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error guardando usuario');
    }
  };

  const toggleUserStatus = async (userId, currentStatus) => {
    const actionText = currentStatus ? 'desactivar' : 'activar';
    const user = users.find(u => u.id === userId);

    showConfirmation(
      `${currentStatus ? 'Desactivar' : 'Activar'} Usuario`,
      `¿Estás seguro de ${actionText} a ${user?.first_name} ${user?.last_name}?`,
      async () => {
        try {
          await axios.patch(`/users/${userId}/toggle-status`);
          loadUsers();
          setError('');
        } catch (error) {
          setError(error.response?.data?.detail || 'Error cambiando estado');
        }
      },
      currentStatus ? 'danger' : 'success',
      currentStatus ? 'Desactivar' : 'Activar'
    );
  };


  const totalPages = Math.ceil(totalUsers / limit);

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
          Gestión de Usuarios
        </h1>
        <p className="text-gray-600">
          Administra usuarios del sistema - {totalUsers} usuarios totales
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
              placeholder="Buscar por nombre, email o código..."
              value={search}
              onChange={handleSearch}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Filtros */}
          <div className="flex gap-3">
            <select
              value={roleFilter}
              onChange={(e) => handleFilterChange('role', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los roles</option>
              {roles.map(role => (
                <option key={role.id} value={role.name}>{role.name}</option>
              ))}
            </select>

            <select
              value={departmentFilter}
              onChange={(e) => handleFilterChange('department', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los departamentos</option>
              {departments.map(dept => (
                <option key={dept.id} value={dept.id}>{dept.name}</option>
              ))}
            </select>

            <select
              value={statusFilter}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los estados</option>
              <option value="true">Activos</option>
              <option value="false">Inactivos</option>
            </select>
          </div>

          {/* Botón crear */}
          {isAdmin() && (
            <button
              onClick={openCreateModal}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center"
            >
              <span className="mr-2">+</span>
              Crear Usuario
            </button>
          )}
        </div>
      </div>

      {/* Tabla de usuarios */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuario
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rol
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Departamento
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Último Login
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((userItem) => (
                <tr key={userItem.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {userItem.first_name} {userItem.last_name}
                      </div>
                      <div className="text-sm text-gray-500">{userItem.email}</div>
                      {userItem.employee_code && (
                        <div className="text-xs text-gray-400">Código: {userItem.employee_code}</div>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${userItem.role === 'admin' ? 'bg-purple-100 text-purple-800' :
                      userItem.role === 'coordinador' ? 'bg-blue-100 text-blue-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                      {userItem.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {userItem.department || 'Sin asignar'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${userItem.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                      {userItem.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {userItem.last_login ?
                      new Date(userItem.last_login).toLocaleDateString() :
                      'Nunca'
                    }
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => openEditModal(userItem)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Editar
                      </button>
                      {isAdmin() && userItem.id !== user.id && (
                        <>
                          <button
                            onClick={() => toggleUserStatus(userItem.id, userItem.is_active)}
                            className={`${userItem.is_active ? 'text-orange-600 hover:text-orange-900' : 'text-green-600 hover:text-green-900'
                              }`}
                          >
                            {userItem.is_active ? 'Desactivar' : 'Activar'}
                          </button>

                        </>
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
              Mostrando {(currentPage - 1) * limit + 1} a {Math.min(currentPage * limit, totalUsers)} de {totalUsers} usuarios
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

      {/* Modal de crear/editar usuario */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {modalMode === 'create' ? 'Crear Usuario' : 'Editar Usuario'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Apellido
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contraseña {modalMode === 'edit' && '(dejar vacío para no cambiar)'}
                </label>
                <input
                  type="password"
                  required={modalMode === 'create'}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Código Empleado
                  </label>
                  <input
                    type="text"
                    value={formData.employee_code}
                    onChange={(e) => setFormData({ ...formData, employee_code: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Teléfono
                  </label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Rol
                  </label>
                  <select
                    required
                    value={formData.role_id}
                    onChange={(e) => setFormData({ ...formData, role_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Seleccionar rol</option>
                    {roles.map(role => (
                      <option key={role.id} value={role.id}>{role.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Departamento
                  </label>
                  <select
                    value={formData.department_id}
                    onChange={(e) => setFormData({ ...formData, department_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Sin departamento</option>
                    {departments.map(dept => (
                      <option key={dept.id} value={dept.id}>{dept.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              {isAdmin() && (
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="is_active"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
                    Usuario activo
                  </label>
                </div>
              )}

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded transition-colors"
                >
                  {modalMode === 'create' ? 'Crear Usuario' : 'Actualizar Usuario'}
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
          </div>
        </div>
      )}
      {/* Modal de confirmación */}
      {showConfirmModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className={`${confirmData.type === 'danger' ? 'bg-red-50' :
                confirmData.type === 'success' ? 'bg-green-50' :
                  confirmData.type === 'warning' ? 'bg-yellow-50' : 'bg-gray-50'
              } px-6 py-4 rounded-t-lg`}>
              <div className="flex items-center">
                <div className={`${confirmData.type === 'danger' ? 'bg-red-100 text-red-600' :
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
                className={`px-4 py-2 text-sm font-medium text-white ${confirmData.type === 'danger' ? 'bg-red-600 hover:bg-red-700' :
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

export default UsersManagement;