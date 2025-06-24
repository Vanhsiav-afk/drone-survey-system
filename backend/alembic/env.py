from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Import models and metadata
from app.db_base import Base
from app.models import drone  # Import other models here too

# Alembic config
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Use model metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
