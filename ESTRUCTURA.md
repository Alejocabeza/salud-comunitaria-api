# ESTRUCTURA.md

## Estructura del Proyecto

Este documento describe la estructura de carpetas y archivos del sistema de salud comunitaria basado en FastAPI.

migrations/
seeders/
src/
models/
schemas/
routes/
services/
repositories/
core/
utils/
tests/
.env
.gitignore
alembic.ini
code_base.md
structure.md
requirement.txt


### Descripción de cada elemento

- **migrations/**  
  Archivos de migraciones de la base de datos gestionados por Alembic.

- **seeders/**  
  Scripts para la carga inicial de datos (usuarios, roles, datos de prueba, etc.).

- **src/**  
  Carpeta principal del código fuente de la aplicación.

  - **models/**  
    Definición de los modelos de base de datos (ORM).

  - **schemas/**  
    Esquemas de validación y serialización de datos usando Pydantic.

  - **routes/**  
    Definición de los endpoints de la API.

  - **services/**  
    Lógica de negocio y servicios de la aplicación.

  - **repositories/**  
    Acceso a datos y consultas a la base de datos.

  - **core/**  
    Configuración general, utilidades de seguridad, autenticación, inicialización, etc.

  - **utils/**  
    Funciones auxiliares y utilidades generales.

  - **tests/**  
    Pruebas unitarias y de integración para asegurar la calidad del código.

- **.env**  
  Variables de entorno para la configuración del proyecto.

- **.gitignore**  
  Archivos y carpetas que deben ser ignorados por Git.

- **alembic.ini**  
  Archivo de configuración principal para Alembic.

- **code_base.md**  
  Documento que describe el sistema, sus módulos y funcionalidades principales.

- **structure.md**  
  Este documento, que explica la estructura del proyecto.

- **requirement.txt**  
  Lista de dependencias y librerías necesarias para ejecutar el proyecto.

---

Esta estructura está diseñada para mantener el código organizado, facilitar el mantenimiento y permitir una escalabilidad sencilla a medida que el sistema crece.