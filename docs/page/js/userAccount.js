const API_URL = 'https://micserv1-soc.onrender.com';
// const API_URL = 'http://127.0.0.1:8000';
async function fetchWithAuth(url, options = {}) {
    options.credentials = 'include';
    
    let response = await fetch(url, options);

    if (response.status === 401) {
        console.warn("Token probablemente expirado. Intentando refrescar...");
        
        const refreshResponse = await fetch(`${API_URL}/api/auth/refresh`, {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include' 
        });

        if (refreshResponse.ok) {
            console.log("Token refrescado exitosamente. Reintentando petición original...");
            response = await fetch(url, options);
        } else {
            console.error("No se pudo refrescar el token. Redirigiendo al login.");
            alert('Sesión expirada. Por favor inicie sesión nuevamente.');
            window.location.href = 'login.html';
            throw new Error("Sesión expirada");
        }
    }

    return response;
}

document.addEventListener('DOMContentLoaded', async () => {
    let userData = {};
    
    try {
        const response = await fetchWithAuth(`${API_URL}/api/users/profile`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
            userData = await response.json();
            if (userData.user) userData = userData.user;
        } else {
            console.error('No se pudo obtener el perfil:', response.status);
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
    }

    if (userData.name) document.getElementById('nombre').value = userData.name;
    if (userData.lastName) document.getElementById('apellidoP').value = userData.lastName;
    if (userData.lastName2) document.getElementById('apellidoM').value = userData.lastName2;
    if (userData.email) document.getElementById('correo').value = userData.email;
    
    if (userData.cellPhone) {
        const cleanPhone = userData.cellPhone.replace('tel:', '');
        const parts = cleanPhone.split('-');
        if (parts.length >= 2) {
            document.getElementById('lada').value = parts[0];
            document.getElementById('number').value = parts.slice(1).join('');
        }
    }
});

function validate_UpdateForm() {
    const name = document.getElementById('nombre').value;
    const lastName = document.getElementById('apellidoP').value;
    const lastName2 = document.getElementById('apellidoM').value;
    const email = document.getElementById('correo').value;
    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('confirmacionP').value;
    
    const lada = document.getElementById('lada').value;
    let rawPhone = document.getElementById('number').value.replace(/\D/g, ''); 
    const cellPhone = `tel:${lada}-${rawPhone.substring(0, 3)}-${rawPhone.substring(3, 6)}-${rawPhone.substring(6, 10)}`;
    
    if (rawPhone.length !== 10) {   
        alert('El número debe ser de 10 dígitos');
        return;
    }

    if (password.length > 0) {
        if (password !== passwordConfirm) {
            alert('Las contraseñas no coinciden');
            return;
        }
        if (password.length < 8){
            alert('La nueva contraseña debe tener al menos 8 caracteres');
            return;
        }
    }

    const updateData = { name, lastName, lastName2, email, cellPhone };
    if (password.length > 0) {
        updateData.password = password;
    }

    updateAccount(updateData);
}

async function updateAccount(updateData) {
    try {
        const response = await fetchWithAuth(`${API_URL}/api/users/profile`, {
            method: 'PUT', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updateData)
        });
        const data = await response.json();

        if (!response.ok) {
            alert(data.message || data.detail || 'Ocurrió un error al actualizar');
            throw new Error(`Error en la petición: ${response.status}`);
        }

        alert('Cuenta actualizada correctamente');
    }
    catch (error) {
        console.error('Error:', error);
    }
}

document.getElementById('updateAccount').addEventListener('submit', function(event) {
    event.preventDefault(); 
    validate_UpdateForm();
});

function logout() {
    fetch(`${API_URL}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
    }).then(response => {
        if (response.ok) {
            localStorage.removeItem('user');
            alert('Sesión cerrada exitosamente');
            window.location.href = 'login.html';
        } else {
            alert('Error al cerrar sesión');
        }
    }).catch(error => {
        console.error('Error al cerrar sesión:', error);
        alert('Error al cerrar sesión');
    }
    );
}

function deleteAccount() {
    if (confirm('¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer.')) {
        fetch(`${API_URL}/api/users/profile`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        }).then(response => {
            if (response.ok) {
                localStorage.removeItem('user');
                alert('Cuenta eliminada exitosamente');
                window.location.href = 'login.html';
            } else {
                alert('Error al eliminar la cuenta');
            }
        }).catch(error => {
            console.error('Error al eliminar la cuenta:', error);
            alert('Error al eliminar la cuenta');
        });
    }
}