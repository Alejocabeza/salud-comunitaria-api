# Salud Comunitaria API

API para la gestión de salud comunitaria, diseñada para administrar pacientes, profesionales, centros ambulatorios, recursos médicos, roles y permisos, entre otros. Construida con **FastAPI**, **SQLModel** y **Alembic**.

## Características

- **Gestión de usuarios, roles y permisos**: Control de acceso seguro y flexible.
- **Administración de pacientes y médicos**: Registro, actualización y seguimiento.
- **Gestión de centros ambulatorios**: Alta, edición y baja de centros.
- **Recursos y solicitudes médicas**: Control de inventario y solicitudes de medicamentos.
- **Autenticación JWT**: Inicio de sesión seguro y recuperación de contraseñas.
- **Notificaciones por email**: Soporte para recuperación de contraseña vía correo electrónico.
- **Migraciones de base de datos**: Versionado y actualización del esquema con Alembic.
- **Semillas iniciales**: Scripts para poblar la base de datos con roles, permisos y usuarios.

## Tecnologías principales

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Passlib](https://passlib.readthedocs.io/)
- [python-jose](https://python-jose.readthedocs.io/)
- [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/)

## Estructura del proyecto

```
src/
  core/           # Configuración, seguridad, dependencias
  models/         # Modelos ORM (SQLModel)
  routes/         # Endpoints de la API
  schemas/        # Esquemas Pydantic
  test/           # Pruebas automáticas
migrations/       # Migraciones Alembic
seeders/          # Scripts de carga inicial de datos
database.db       # Base de datos SQLite (por defecto)
.env              # Variables de entorno
requirements.txt  # Dependencias del proyecto
```

## Instalación

1. **Clona el repositorio**  
   ```sh
   git clone <URL_DEL_REPO>
   cd salud-comunitaria-api
   ```

2. **Crea un entorno virtual e instala dependencias**  
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configura las variables de entorno**  
   Copia el archivo `.env` y ajusta los valores según tu entorno.

4. **Aplica las migraciones**  
   ```sh
   alembic upgrade head
   ```

5. **Carga los datos iniciales (roles, permisos, admin, etc.)**  
   ```sh
   python seeders/main.py
   ```

6. **Inicia el servidor**  
   ```sh
   uvicorn src.main:app --reload
   ```

7. **Accede a la documentación interactiva**  
   [http://localhost:8000/](http://localhost:8000/)

## Pruebas

Ejecuta los tests con pytest:

```sh
pytest src/test/
```

## Endpoints principales

- `/api/v1/auth/login` — Autenticación de usuarios
- `/api/v1/users/` — Gestión de usuarios
- `/api/v1/roles/` — Gestión de roles
- `/api/v1/permissions/` — Gestión de permisos
- `/api/v1/outpatient_center/` — Centros ambulatorios
- `/api/v1/doctors/` — Médicos
- `/api/v1/patients/` — Pacientes
- `/api/v1/medical_resource/` — Recursos médicos
- `/api/v1/medication_request/` — Solicitudes de medicamentos

Consulta la documentación Swagger para ver todos los endpoints y sus detalles.

## Contribución

1. Haz un fork del repositorio.
2. Crea una rama para tu feature o fix.
3. Haz tus cambios y escribe pruebas.
4. Haz un pull request describiendo tu aporte.

## Licencia

MIT

---

**Desarrollado por el equipo de Salud