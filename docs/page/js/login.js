async function login() {
    try {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Obtener el token de Turnstile
        const cfToken = document.querySelector('[name="cf-turnstile-response"]')?.value;
        
        if (!cfToken) {
            alert("Por favor completa la verificación de seguridad (Captcha).");
            return;
        }

        const loginData = { email, password, cfToken };
        const API_URL = 'https://micserv1-soc.onrender.com';
        // const API_URL = 'http://127.0.0.1:8000';


        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Necesario para que el navegador acepte y guarde las cookies (Set-Cookie) del servidor
            body: JSON.stringify(loginData)
        });
        const data = await response.json();

        if (!response.ok) {
            alert(data.message || data.detail || 'Ocurrió un error');
            throw new Error(`Error en la petición: ${response.status}`);
        }

        if (data.statusCode === 200) {
            alert(data.message);
            window.location.href = 'userAccount.html';

            localStorage.setItem('user', JSON.stringify(data.user));
        }
    }
    catch (error) {
        console.error('Error:', error);
    }
}


document.getElementById('login').addEventListener('submit', function(event) {
    event.preventDefault(); 
    login();
});

if (localStorage.getItem('user') != null) {
    window.location.href = 'userAccount.html';
}
