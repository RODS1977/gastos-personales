// Manejar login
async function handleLogin(e) {
    e.preventDefault();
    showLoading(true);
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                correo: email,
                password: password
            })
        });
        
        const data = await handleApiResponse(response);
        
        // Guardar datos de usuario
        localStorage.setItem('authToken', data.data.access_token);
        localStorage.setItem('userData', JSON.stringify(data.data.user));
        currentUser = data.data.user;
        
        showDashboard();
        loadCategorias();
        loadGastos();
        showNotification('¡Bienvenido! Sesión iniciada correctamente');
        
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Manejar registro
async function handleRegister(e) {
    e.preventDefault();
    showLoading(true);
    
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/registro`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: name,
                correo: email,
                password: password
            })
        });
        
        const data = await handleApiResponse(response);
        
        // Guardar datos y mostrar login
        localStorage.setItem('authToken', data.data.access_token);
        localStorage.setItem('userData', JSON.stringify(data.data.user));
        currentUser = data.data.user;
        
        showDashboard();
        loadCategorias();
        loadGastos();
        showNotification('¡Cuenta creada exitosamente!');
        
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Cerrar sesión
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    currentUser = null;
    gastos = [];
    categorias = [];
    
    // Limpiar formularios
    document.getElementById('loginFormElement').reset();
    document.getElementById('registerFormElement').reset();
    
    showAuth();
    showLogin();
    showNotification('Sesión cerrada correctamente');
}