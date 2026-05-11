const API_REF = 'https://nt189.github.io/MicServ1-SOC/Contrato.yaml';

if (!window.location.hash && localStorage.getItem('API_DOC')) {
    window.location.replace(localStorage.getItem('API_DOC'));
}

function router() {
    const hash = window.location.hash;
    const viewerContainer = document.getElementById('body');

    if (!hash || hash === '#inicio') {
        document.getElementById('header').innerHTML = '<h1>Urban Market Identify Service API Documentación</h1>';
        viewerContainer.innerHTML = `
        <div id="content">
            <h2>Herramientas visualizacion API</h2>
            <div class="links-container">
                <a href="#swagger">Swagger UI</a>
                <a href="#redoc">Redoc</a>
                <a href="#scalar">Scalar</a>
                <a href="#elements">Stoplight Elements</a>
            </div>
        </div>
        `;
        return;
    }

    document.getElementById('header').innerHTML = `
        <nav id="navbar" class="navbar">
            <a href="#inicio">🏠 Inicio</a>
            <a href="#swagger">Swagger</a>
            <a href="#redoc">Redoc</a>
            <a href="#scalar">Scalar</a>
            <a href="#elements">Elements</a>
        </nav>
    `;

    switch (hash) {
        case '#swagger':
            viewerContainer.innerHTML = `
                <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
                <div id="swagger-ui"></div>
            `;
            
            var scriptSwagger = document.createElement('script');
            scriptSwagger.src = "https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js";
            scriptSwagger.async = true;
            scriptSwagger.onload = function() {
                window.ui = SwaggerUIBundle({
                    url: API_REF,
                    dom_id: '#swagger-ui',
                });
            };
            document.body.appendChild(scriptSwagger);
            localStorage.setItem('API_DOC', '#swagger');
            break;
        case '#redoc':
            viewerContainer.innerHTML = `
                <redoc spec-url="${API_REF}"></redoc>
            `;

            var script = document.createElement('script');

            script.id = 'redoc-script';
            script.src = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js";
            script.async = true;
            document.body.appendChild(script);

            localStorage.setItem('API_DOC', '#redoc');
            break;
        case '#scalar':
            viewerContainer.innerHTML = '<div id="app"></div>';

            var script = document.createElement('script');

            script.id = 'scalar-script';
            script.src = "https://cdn.jsdelivr.net/npm/@scalar/api-reference";
            script.async = true;
            script.onload = function() {
                Scalar.createApiReference('#app', {
                    url: API_REF,
                    proxyUrl: 'https://proxy.scalar.com',
                    showDeveloperTools: "never",
                    hideDarkModeToggle: true
                });
            };
            document.body.appendChild(script)
            localStorage.setItem('API_DOC', '#scalar');
            break;
        case '#elements':
            viewerContainer.innerHTML = `
                <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
                <elements-api
                    apiDescriptionUrl="${API_REF}"
                    router="hash"
                    layout="sidebar"
                />
            `;

            
            var script = document.createElement('script');

            script.id = 'elements-script';
            script.src = "https://unpkg.com/@stoplight/elements/web-components.min.js";
            script.async = true;
            document.body.appendChild(script);
            localStorage.setItem('API_DOC', '#elements');
            break;
        default:
            viewerContainer.innerHTML = '<h1>404</h1><p>Página no encontrada.</p>';
    }
}

window.addEventListener('hashchange', router);

window.addEventListener('load', router);