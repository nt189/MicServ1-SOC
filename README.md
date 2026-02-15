# MicServ1-SOC - Identity Service

## 📋 Descripción General

Microservicio REST profesional encargado de la **Gestión de Identidad y Clientes (Identity Service)** dentro de la arquitectura SOC (Service-Oriented Computing). Este servicio constituye el componente central para la administración del ciclo de vida completo de los usuarios en el sistema.

## 🎯 Objetivos del Servicio

Este microservicio proporciona funcionalidades críticas para:

### 1. **Gestión del Ciclo de Vida de Usuarios**
- Registro y onboarding de nuevos usuarios
- Actualización de información de perfil
- Desactivación y eliminación de cuentas
- Auditoría completa de actividades del usuario

### 2. **Diferenciación de Tipos de Usuario**
- **Clientes Registrados**: Usuarios autenticados con perfiles completos y acceso a todas las funcionalidades
- **Usuarios Invitados**: Acceso temporal limitado con restricciones específicas para exploración del sistema
- Gestión de permisos y privilegios según tipo de usuario

### 3. **Gestión Segura de Perfiles**
- Almacenamiento encriptado de información sensible
- Validación de datos de usuario
- Gestión de preferencias y configuraciones personales
- Protección de datos según normativas (GDPR, LOPD)

### 4. **Gestión de Libretas de Direcciones**
- Almacenamiento de múltiples direcciones por usuario
- Validación de direcciones postales
- Direcciones de facturación y envío
- Historial de direcciones utilizadas

### 5. **Autenticación Centralizada mediante Tokens**
- Implementación de JWT (JSON Web Tokens) para autenticación stateless
- Generación y validación de tokens de acceso
- Refresh tokens para sesiones extendidas
- Gestión de expiración y renovación de tokens
- Single Sign-On (SSO) capabilities

### 6. **Detección de Bots y Seguridad**
- Análisis de patrones de comportamiento sospechoso
- Implementación de CAPTCHA y mecanismos anti-bot
- Rate limiting para prevenir ataques de fuerza bruta
- Detección de actividad anómala mediante machine learning
- Bloqueo automático de cuentas comprometidas

## 🏗️ Estructura del Proyecto

```
MicServ1-SOC/
│
├── routes/          # Definiciones de rutas y endpoints del API
│   └── .gitkeep
│
├── controllers/     # Lógica de negocio y controladores
│   └── .gitkeep
│
├── models/          # Modelos de datos y esquemas
│   └── .gitkeep
│
├── middleware/      # Middleware para autenticación, validación y procesamiento
│   └── .gitkeep
│
├── config/          # Archivos de configuración del servicio
│   └── .gitkeep
│
└── README.md        # Documentación del proyecto
```

## 🔧 Tecnologías Previstas

- **Framework**: Node.js con Express.js / Python con FastAPI (a definir)
- **Base de Datos**: PostgreSQL / MongoDB (a definir)
- **Autenticación**: JWT (JSON Web Tokens)
- **Seguridad**: bcrypt, helmet, rate-limiting
- **Validación**: Joi / express-validator
- **Documentación API**: Swagger/OpenAPI

## 🚀 Características Principales

### Endpoints API (Planificados)

#### Autenticación
- `POST /api/auth/register` - Registro de nuevos usuarios
- `POST /api/auth/login` - Inicio de sesión
- `POST /api/auth/logout` - Cierre de sesión
- `POST /api/auth/refresh` - Renovación de token
- `POST /api/auth/forgot-password` - Recuperación de contraseña

#### Gestión de Usuarios
- `GET /api/users/profile` - Obtener perfil del usuario
- `PUT /api/users/profile` - Actualizar perfil
- `DELETE /api/users/profile` - Eliminar cuenta
- `GET /api/users/:id` - Obtener usuario por ID (admin)

#### Gestión de Direcciones
- `GET /api/addresses` - Listar direcciones del usuario
- `POST /api/addresses` - Crear nueva dirección
- `PUT /api/addresses/:id` - Actualizar dirección
- `DELETE /api/addresses/:id` - Eliminar dirección

#### Usuarios Invitados
- `POST /api/guest/session` - Crear sesión de invitado
- `GET /api/guest/features` - Obtener funcionalidades disponibles

## 🔒 Seguridad

### Medidas Implementadas
- Encriptación de contraseñas con bcrypt
- Validación de entrada en todos los endpoints
- Rate limiting para prevenir ataques DDoS
- Headers de seguridad con Helmet
- Protección CSRF
- Sanitización de datos
- Logging de auditoría

### Detección de Bots
- Análisis de User-Agent
- Verificación de patrones de tráfico
- CAPTCHA en operaciones sensibles
- Blacklisting de IPs sospechosas
- Análisis de tiempo de respuesta

## 📝 Estado del Proyecto

**Versión**: 0.1.0 (Estructura Inicial)
**Estado**: En Desarrollo

### Próximos Pasos
1. Implementación de modelos de datos
2. Configuración de base de datos
3. Desarrollo de controladores principales
4. Implementación de middleware de autenticación
5. Creación de rutas y endpoints
6. Pruebas unitarias e integración
7. Documentación API con Swagger

## 👥 Contribución

Este proyecto sigue las mejores prácticas de desarrollo de microservicios y arquitectura REST. Las contribuciones deben seguir los estándares de código establecidos.

## 📄 Licencia

[Definir licencia del proyecto]

---

**Nota**: Este es un microservicio en desarrollo activo. La documentación se actualizará conforme se implementen nuevas funcionalidades.