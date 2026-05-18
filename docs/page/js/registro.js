function validate_Form() {
    const name = document.getElementById('nombre').value;
        const lastName = document.getElementById('apellidoP').value;
        const lastName2 = document.getElementById('apellidoM').value;
        const email = document.getElementById('correo').value;
        const password = document.getElementById('password').value;
        const passwordConfirm = document.getElementById('confirmacionP').value;
        const lada = document.getElementById('lada').value;
        let rawPhone = document.getElementById('number').value.replace(/\D/g, ''); 
        const cellPhone = `${lada} ${rawPhone.substring(0, 3)}-${rawPhone.substring(3, 6)}-${rawPhone.substring(6, 10)}`;
        
        if (rawPhone.length !== 10) {
            alert('El número debe ser de 10 dígitos');
            return;
        }

        if (password !== passwordConfirm) {
            alert('Las contraseñas no coinciden');
            return;
        }
        else if (password.length == 0){
            alert('La contraseña no puede estar vacía');
            return;
        }
        else if (passwordConfirm.length == 0){
            alert('La confirmación de contraseña no puede estar vacía');
            return;
        }
        else if(password.length < 8){
            alert('La contraseña debe tener al menos 8 caracteres');
            return;
        }
        else if (!/\d/.test(password)) {
            alert('La contraseña debe contener al menos un número');
            return;
        }
        else if (!/[A-Z]/.test(password)) {
            alert('La contraseña debe contener al menos una letra mayúscula');
            return;
        }
        else if (!/[a-z]/.test(password)) {
            alert('La contraseña debe contener al menos una letra minúscula');
            return;
        }
        else if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            alert('La contraseña debe contener al menos un carácter especial');
            return;
        }

        // Obtener el token de Turnstile
        const cfToken = document.querySelector('[name="cf-turnstile-response"]')?.value;
        console.log('Token de Turnstile:', cfToken);
        if (!cfToken) {
            alert("Por favor completa la verificación de seguridad (Captcha).");
            return;
        }

        const loginData = { name, lastName, lastName2, email, password, cellPhone, cfToken };

        register(loginData);
}

async function register(loginData) {
    try {
        const API_URL = 'https://micserv1-soc.onrender.com';
        // const API_URL = 'http://127.0.0.1:8000';
        const response = await fetch(`${API_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(loginData)
        });
        const data = await response.json();

        if (!response.ok) {
            alert(data.message || data.errors || data.detail || 'Ocurrió un error');
            throw new Error(`Error en la petición: ${response.status}`);
        }

        if (data.statusCode === 201) {
            alert(data.message);
        }
        window.location.href = 'userAccount.html';
    }
    catch (error) {
        console.error('Error:', error);
    }
}


document.getElementById('registro').addEventListener('submit', function(event) {
    event.preventDefault(); 
    validate_Form();
});



if (localStorage.getItem('user') != null) {
    window.location.href = 'userAccount.html';
}