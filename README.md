# 🏥 VitaClinic - Gestión de Médicos (CRUD)

VitaClinic es un sistema de administración para clínicas de salud que permite gestionar el equipo médico de forma eficiente. La aplicación permite registrar, listar, editar y eliminar médicos, garantizando la integridad de los datos mediante validaciones estrictas tanto en el backend como en la base de datos.

## 🛠️ Dependencias Principales
De la lista total de librerías, estas son las esenciales que hacen funcionar el núcleo del proyecto:

* **FastAPI (0.121.0):** Framework principal para la creación de rutas y lógica del servidor.
* **MySQL Connector Python (9.5.0):** Driver para la comunicación con la base de datos MySQL.
* **Pydantic (2.12.4):** Validación de esquemas de datos y tipos de entrada.
* **Jinja2 (3.1.6):** Motor de plantillas para renderizar el frontend dinámico.
* **Uvicorn (0.38.0):** Servidor de alto rendimiento para ejecutar la aplicación.
* **Python-dotenv (1.2.1):** Gestión segura de variables de entorno (credenciales).
* **Email-validator (2.1.0):** Validación de formato profesional para correos institucionales.

---

## 🏗️ Arquitectura de la Solución
El sistema sigue un patrón de diseño desacoplado para facilitar el mantenimiento:



1.  **Capa de Datos (`database.py`):** Gestión de conexiones y consultas SQL puras.
2.  **Capa de Aplicación (`main.py`):** Controladores de FastAPI que gestionan las peticiones del usuario.
3.  **Capa de Presentación (`templates/`):** Vistas dinámicas creadas con HTML5, CSS3 y Jinja2.

---

## ⚠️ Gestión de Errores de Conexión
Para garantizar una experiencia de usuario fluida, el sistema cuenta con un sistema de captura de excepciones global para la base de datos.

Si el servidor de base de datos no está disponible o la conexión falla, el sistema intercepta el error y **renderiza automáticamente la página `404.html`**. 

> **Nota:** Aunque técnicamente es un error de conexión, se redirige a este template amigable para evitar mostrar errores técnicos internos y ofrecer al usuario una vía de escape segura (como un botón para volver al inicio).

---

## 📋 Funcionalidades Destacadas
* **Prevención de Duplicados:** Validación en tiempo real para impedir correos duplicados en la base de datos.
* **Edición Inteligente:** Permite actualizar datos de un médico sin que el sistema bloquee el proceso por detectar su propio correo como "existente".
* **Interfaz Dinámica:** Carrusel de doctores con una tarjeta especial centrada para añadir nuevos registros de forma intuitiva.
* **Validación de Formatos:** Solo se permiten nombres y especialidades con caracteres alfabéticos válidos.

---

## 🚀 Instalación y Uso

1. **Configurar Entorno:**
   Crea un archivo `.env` con los datos de tu MySQL:
   ```env
   DB_HOST=localhost
   DB_USER
   DB_PASSWORD=
   DB_NAME=cenit_salud_db
