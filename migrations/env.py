# migrations/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Esto es necesario para que Alembic pueda importar módulos de tu aplicación
# Añade el directorio raíz de tu proyecto (donde está `app/`) al sys.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Importa tus settings y modelos
from src.core.settings import settings # Para obtener DATABASE_URL
from sqlmodel import SQLModel  # Importa SQLModel desde el paquete correcto
from src.models.user import User, Role, UserRoleLink, Permission, RolePermissionLink
from src.models.outpatient_center import OutpatientCenter
# Importa aquí otros modelos según sea necesario

# Configuración de Alembic, lee la configuración desde alembic.ini
config = context.config

# Interpreta el archivo de configuración para logging de Python.
# Esta línea básicamente configura los loggers solo una vez.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establece la URL de la base de datos desde tus settings
# Esto sobreescribe cualquier valor de sqlalchemy.url en alembic.ini
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# target_metadata para operaciones de 'autogenerate'
# SQLModel.metadata contiene la metadata de todas tus tablas definidas con SQLModel
target_metadata = SQLModel.metadata
# Para SQLAlchemy puro sería:
# from myapp.mymodel import Base
# target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True # IMPORTANTE para SQLite y algunas alteraciones
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True # IMPORTANTE para SQLite y algunas alteraciones
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()