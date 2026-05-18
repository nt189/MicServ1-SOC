const API_URL = 'https://micserv1-soc.onrender.com';
// const API_URL = 'http://127.0.0.1:8000';

document.getElementById('resetPassword').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    
    if (!token) {
        alert("Enlace inválido o ha expirado. (No se encontró el token de seguridad).");
        return;
    }
    
    const new_password = document.getElementById('new_password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    
    if (new_password !== confirm_password) {
        alert("Las contraseñas no coinciden.");
        return;
    }
    
    if (new_password.length < 8) {
        alert("La contraseña debe tener al menos 8 caracteres.");
        return;
    }
    else if (!/\d/.test(new_password)) {
        alert('La contraseña debe contener al menos un número');
        return;
    }
    else if (!/[A-Z]/.test(new_password)) {
        alert('La contraseña debe contener al menos una letra mayúscula');
        return;
    }
    else if (!/[a-z]/.test(new_password)) {
        alert('La contraseña debe contener al menos una letra minúscula');
        return;
    }
    else if (!/[!@#$%^&*(),.?":{}|<>]/.test(new_password)) {
        alert('La contraseña debe contener al menos un carácter especial');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/auth/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token, new_password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.message || data.detail || 'Ocurrió un error al restablecer la contraseña');
            return;
        }
        
        alert("¡Tu contraseña ha sido restablecida exitosamente! Ahora puedes iniciar sesión.");
        
        window.location.href = 'login.html';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al conectar con el servidor.');
    }
});