const API_URL = 'https://micserv1-soc.onrender.com';
// const API_URL = 'http://127.0.0.1:8000';

 async function enviar(event) {
    const email = document.getElementById('email').value;
    
    try {
        const response = await fetch(`${API_URL}/api/auth/forgot-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.message || data.detail || 'Ocurrió un error. Verifica el correo.');
            return;
        }
        
        alert(data.message || 'Si el correo está registrado, recibirás instrucciones.');
        
        if (data.token) {
            const simulationContainer = document.getElementById('simulation-container');
            const resetLink = document.getElementById('reset-link');
            
            resetLink.href = `cambioContrasena.html?token=${data.token}`;
            simulationContainer.style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al conectar con el servidor.');
    }
}