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
    
    if (token && userData) {
        currentUser = JSON.parse(userData);
        console.log('👤 Usuario autenticado:', currentUser);
        showDashboard();
        loadCategorias();
        loadGastos();
    } else {
        console.log('🔓 Usuario no autenticado, mostrando login');
        showAuth();
    }
}

// Cargar categorías desde la API
async function loadCategorias() {
    console.log('📋 Cargando categorías...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/categorias`);
        console.log('📡 Response categorías:', response);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
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