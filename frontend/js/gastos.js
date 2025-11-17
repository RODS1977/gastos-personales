// Cargar categorías desde la API
async function loadCategorias() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/categorias`);
        const data = await handleApiResponse(response);
        categorias = data.data;
        
        // Llenar select de categorías
        const categoriaSelect = document.getElementById('categoria');
        const editCategoriaSelect = document.getElementById('editCategoria');
        const filterCategoriaSelect = document.getElementById('filterCategoria');
        
        // Limpiar opciones existentes (excepto la primera)
        [categoriaSelect, editCategoriaSelect, filterCategoriaSelect].forEach(select => {
            while (select.children.length > 1) {
                select.removeChild(select.lastChild);
            }
        });
        
        // Agregar categorías
        categorias.forEach(categoria => {
            const option = new Option(categoria.nombre, categoria.id);
            const editOption = new Option(categoria.nombre, categoria.id);
            const filterOption = new Option(categoria.nombre, categoria.id);
            
            categoriaSelect.add(option);
            editCategoriaSelect.add(editOption.cloneNode(true));
            filterCategoriaSelect.add(filterOption.cloneNode(true));
        });
        
    } catch (error) {
        showNotification('Error al cargar categorías', 'error');
    }
}

// Cargar gastos del usuario
async function loadGastos() {
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/gastos`, {
            headers: getAuthHeaders()
        });
        
        const data = await handleApiResponse(response);
        gastos = data.data;
        
        updateGastosTable();
        updateSummaryCards();
        
    } catch (error) {
        showNotification('Error al cargar gastos', 'error');
    } finally {
        showLoading(false);
    }
}

// Crear nuevo gasto
async function handleCreateGasto(e) {
    e.preventDefault();
    showLoading(true);
    
    const formData = new FormData(e.target);
    const gastoData = {
        categoria_id: parseInt(document.getElementById('categoria').value),
        monto: parseFloat(document.getElementById('monto').value),
        fecha: document.getElementById('fecha').value,
        descripcion: document.getElementById('descripcion').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/gastos`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(gastoData)
        });
        
        const data = await handleApiResponse(response);
        
        // Recargar gastos y limpiar formulario
        await loadGastos();
        e.target.reset();
        setDefaultDate();
        
        showNotification('Gasto agregado correctamente');
        
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Actualizar gasto existente
async function handleUpdateGasto(e) {
    e.preventDefault();
    showLoading(true);
    
    const gastoId = document.getElementById('editGastoId').value;
    const gastoData = {
        categoria_id: parseInt(document.getElementById('editCategoria').value),
        monto: parseFloat(document.getElementById('editMonto').value),
        fecha: document.getElementById('editFecha').value,
        descripcion: document.getElementById('editDescripcion').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/gastos/${gastoId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(gastoData)
        });
        
        await handleApiResponse(response);
        
        // Recargar gastos y cerrar modal
        await loadGastos();
        closeEditModal();
        
        showNotification('Gasto actualizado correctamente');
        
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Eliminar gasto
async function deleteGasto(gastoId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este gasto?')) {
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/gastos/${gastoId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        await handleApiResponse(response);
        
        // Recargar gastos
        await loadGastos();
        
        showNotification('Gasto eliminado correctamente');
        
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Abrir modal para editar gasto
function openEditModal(gastoId) {
    const gasto = gastos.find(g => g.id == gastoId);
    
    if (!gasto) return;
    
    // Llenar formulario con datos del gasto
    document.getElementById('editGastoId').value = gasto.id;
    document.getElementById('editCategoria').value = categorias.find(c => c.nombre === gasto.categoria)?.id || '';
    document.getElementById('editMonto').value = gasto.monto;
    document.getElementById('editFecha').value = gasto.fecha;
    document.getElementById('editDescripcion').value = gasto.descripcion || '';
    
    // Mostrar modal
    document.getElementById('editModal').style.display = 'block';
}

// Cerrar modal de edición
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
    document.getElementById('editGastoForm').reset();
}

// Actualizar tabla de gastos
function updateGastosTable() {
    const tbody = document.getElementById('gastosTableBody');
    const emptyState = document.getElementById('emptyState');
    
    if (gastos.length === 0) {
        tbody.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    const filteredGastos = getFilteredGastos();
    
    tbody.innerHTML = filteredGastos.map(gasto => `
        <tr>
            <td>${formatDate(gasto.fecha)}</td>
            <td>
                <span class="categoria-badge">${gasto.categoria}</span>
            </td>
            <td>${gasto.descripcion || '-'}</td>
            <td class="monto">$${gasto.monto.toFixed(2)}</td>
            <td class="actions">
                <button class="btn btn-edit" onclick="openEditModal(${gasto.id})">
                    <i class="fas fa-edit"></i> Editar
                </button>
                <button class="btn btn-danger" onclick="deleteGasto(${gasto.id})">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </td>
        </tr>
    `).join('');
}

// Aplicar filtros
function applyFilters() {
    updateGastosTable();
    updateSummaryCards();
}

// Obtener gastos filtrados
function getFilteredGastos() {
    let filtered = [...gastos];
    
    // Filtrar por categoría
    const categoriaFilter = document.getElementById('filterCategoria').value;
    if (categoriaFilter) {
        const categoriaNombre = categorias.find(c => c.id == categoriaFilter)?.nombre;
        filtered = filtered.filter(gasto => gasto.categoria === categoriaNombre);
    }
    
    // Filtrar por mes
    const mesFilter = document.getElementById('filterMes').value;
    if (mesFilter) {
        filtered = filtered.filter(gasto => gasto.fecha.startsWith(mesFilter));
    }
    
    return filtered;
}

// Actualizar tarjetas de resumen
function updateSummaryCards() {
    const filteredGastos = getFilteredGastos();
    const currentMonth = new Date().toISOString().slice(0, 7);
    
    // Gastos del mes actual
    const gastosMes = filteredGastos.filter(gasto => 
        gasto.fecha.startsWith(currentMonth)
    );
    const totalMes = gastosMes.reduce((sum, gasto) => sum + gasto.monto, 0);
    
    // Categorías usadas
    const categoriasUsadas = new Set(filteredGastos.map(gasto => gasto.categoria)).size;
    
    // Actualizar UI
    document.getElementById('totalGastosMes').textContent = `$${totalMes.toFixed(2)}`;
    document.getElementById('totalCategorias').textContent = categoriasUsadas;
    document.getElementById('totalGastos').textContent = filteredGastos.length;
}

// Formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target === modal) {
        closeEditModal();
    }
}