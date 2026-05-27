function header(){
    const header = document.getElementById('header');

    header.innerHTML = `
        <div class="nav-container">
            <div class="logo">
                <img src="img/UMA.png" alt="Urban Market" class="logo-image">
                <span class="logo-text">URBAN MARKET</span>
            </div>
            <div class="nav-links">
                <a href="#">Inicio</a>
                <a href="#">Productos</a>
                <a href="userAccount.html">Mi Cuenta</a>
                <a href="#footer">Contacto</a>
            </div>
        </div>
    `;
}
header();

function footer(){
    const footer = document.getElementById('footer');
    footer.innerHTML = `
        <div class="footer-container">
            <div class="footer-section">
                <h4>Urban Market</h4>
                <p>Tu tienda de confianza</p>
                <p>✨ Calidad y estilo ✨</p>
            </div>
            <div class="footer-section">
                <h4>Atención al cliente</h4>
                <p>📞 800-URBAN-MK</p>
                <p>✉️ soporte@urbanmarket.com</p>
            </div>
            <div class="footer-section">
                <h4>Horario</h4>
                <p>Lun a Vie: 9am - 7pm</p>
                <p>Sábado: 10am - 2pm</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>Urban Market 2026 - Todos los derechos reservados</p>
        </div>
    `;
}
footer();