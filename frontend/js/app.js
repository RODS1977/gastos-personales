// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:5000';

// Estado global de la aplicación
let currentUser = null;
let categorias = [];
let gastos = [];

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Aplicación iniciada');
    checkAuthStatus();
    setupEventListeners();
    setDefaultDate();
});

// Verificar estado de autenticación
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    console.log('🔐 Verificando autenticación:', { token: !!token, userData: !!userData });
    
    if (token && userData && userData !== 'undefined') {
        try {
            currentUser = JSON.parse(userData);
            console.log('👤 Usuario autenticado:', currentUser);
            showDashboard();
            loadCategorias();
            loadGastos();
            return;
        } catch (e) {
            console.warn('⚠️ userData inválido en localStorage, limpiando autenticación:', e);
            // limpiar entradas inválidas
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
        }
    }

    console.log('🔓 Usuario no autenticado, mostrando login');
    showAuth();
}

// Cargar categorías desde la API
async function loadCategorias() {
    console.log('📋 Cargando categorías...');
    
    try {
        const response = await apiFetch('/api/categorias');
        console.log('📡 Response categorías:', response);
        
        const data = await handleApiResponse(response);
        console.log('✅ Datos categorías:', data);
        
        categorias = data.data;
        populateCategoriaSelects();
        
    } catch (error) {
        console.error('❌ Error cargando categorías:', error);
        showNotification('Error al cargar categorías: ' + error.message, 'error');
    }
}

// Llenar los selects de categorías
function populateCategoriaSelects() {
    console.log('🔄 Llenando selects con categorías:', categorias);
    
    const selects = [
        document.getElementById('categoria'),
        document.getElementById('editCategoria'),
        document.getElementById('filterCategoria')
    ];
    
    selects.forEach(select => {
        if (!select) {
            console.error('❌ Select no encontrado:', select);
            return;
        }
        
        // Limpiar opciones existentes (excepto la primera)
        while (select.children.length > 1) {
            select.removeChild(select.lastChild);
        }
        
        // Agregar categorías
        categorias.forEach(categoria => {
            const option = document.createElement('option');
            option.value = categoria.id;
            option.textContent = categoria.nombre;
            select.appendChild(option);
        });
    });
    
    console.log('✅ Selects de categorías actualizados');
}

// Mostrar notificación mejorada
function showNotification(message, type = 'success') {
    console.log(`📢 Notificación [${type}]:`, message);
    
    const notification = document.getElementById('notification');
    if (!notification) {
        console.error('❌ Elemento de notificación no encontrado');
        return;
    }
    
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}

// Mostrar zona de autenticación (login/registro)
function showAuth() {
    const authSection = document.getElementById('authSection');
    const dashboard = document.getElementById('dashboard');
    const userInfo = document.getElementById('userInfo');

    if (authSection) authSection.style.display = 'block';
    if (dashboard) dashboard.style.display = 'none';
    if (userInfo) userInfo.style.display = 'none';
}

// Mostrar dashboard (usuario autenticado)
function showDashboard() {
    const authSection = document.getElementById('authSection');
    const dashboard = document.getElementById('dashboard');
    const userInfo = document.getElementById('userInfo');

    if (authSection) authSection.style.display = 'none';
    if (dashboard) dashboard.style.display = 'block';
    if (userInfo) userInfo.style.display = 'block';

    const userNameEl = document.getElementById('userName');
    if (userNameEl && currentUser) userNameEl.textContent = currentUser.nombre || currentUser.name || '';
}

// Mostrar formularios de login/registro
function showLogin() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (loginForm) loginForm.style.display = 'block';
    if (registerForm) registerForm.style.display = 'none';
}

function showRegister() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (loginForm) loginForm.style.display = 'none';
    if (registerForm) registerForm.style.display = 'block';
}

// Mostrar/ocultar el loading global
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (!loading) return;
    loading.style.display = show ? 'block' : 'none';
}

// Manejo genérico de respuestas de la API
async function handleApiResponse(response) {
    const text = await response.text();
    let data = null;
    try {
        data = text ? JSON.parse(text) : null;
    } catch (e) {
        // no-op
    }

    if (!response.ok) {
        const message = (data && (data.message || data.error)) || `Error HTTP: ${response.status}`;
        throw new Error(message);
    }

    return data;
}

// Encabezados con token si está disponible
function getAuthHeaders() {
    const token = localStorage.getItem('authToken');
    const headers = {
        'Content-Type': 'application/json'
    };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
}

// Fecha por defecto en inputs de tipo date
function setDefaultDate() {
    const today = new Date().toISOString().slice(0, 10);
    const fecha = document.getElementById('fecha');
    const editFecha = document.getElementById('editFecha');
    if (fecha && !fecha.value) fecha.value = today;
    if (editFecha && !editFecha.value) editFecha.value = today;
}

// Registrar listeners de eventos del DOM
function setupEventListeners() {
    const loginForm = document.getElementById('loginFormElement');
    const registerForm = document.getElementById('registerFormElement');
    const gastoForm = document.getElementById('gastoForm');
    const editGastoForm = document.getElementById('editGastoForm');
    const filterCategoria = document.getElementById('filterCategoria');
    const filterMes = document.getElementById('filterMes');

    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (registerForm) registerForm.addEventListener('submit', handleRegister);
    if (gastoForm) gastoForm.addEventListener('submit', handleCreateGasto);
    if (editGastoForm) editGastoForm.addEventListener('submit', handleUpdateGasto);
    if (filterCategoria) filterCategoria.addEventListener('change', applyFilters);
    if (filterMes) filterMes.addEventListener('change', applyFilters);
}

// Central fetch wrapper that automatically adds Authorization header
// and handles 401/422 by clearing auth and redirecting to login view.
async function apiFetch(pathOrUrl, options = {}) {
    const isAbsolute = /^https?:\/\//i.test(pathOrUrl);
    const url = isAbsolute ? pathOrUrl : `${API_BASE_URL}${pathOrUrl.startsWith('/') ? '' : '/'}${pathOrUrl}`;

    const headers = Object.assign({}, options.headers || {});
    // Do not force Content-Type when body is FormData
    if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    const token = localStorage.getItem('authToken');
    if (token && !headers['Authorization']) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const opts = Object.assign({}, options, { headers });

    const resp = await fetch(url, opts);

    if (resp.status === 401 || resp.status === 422) {
        let msg = 'Autenticación requerida';
        try {
            const body = await resp.json();
            if (body && body.message) msg = body.message;
        } catch (e) {
            // ignore JSON parse errors
        }

        // Clear local auth and show login
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        showNotification(msg, 'error');
        showAuth();
        showLogin();

        // Throw to allow callers to handle it too
        throw new Error(msg);
    }

    return resp;
}