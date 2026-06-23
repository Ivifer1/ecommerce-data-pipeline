"""
Configuraciones centralizadas del pipeline ETL.
Todas las constantes y conexiones se definen aquí para facilitar mantenimiento.
"""

import os
from pathlib import Path

# ─── Rutas del proyecto ───
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

# ─── API Fake Store ───
API_BASE_URL = "https://fakestoreapi.com"
API_ENDPOINTS = {
    "products": "/products",
    "users": "/users",
    "carts": "/carts",
}

# ─── Base de datos PostgreSQL ───
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5433"),  # Puerto externo de Docker
    "database": os.getenv("DB_NAME", "ecommerce"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
}

DB_CONNECTION_STRING = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# ─── Base de datos PostgreSQL (desde dentro de Docker) ───
DB_CONFIG_DOCKER = {
    "host": "postgres",
    "port": "5432",  # Puerto interno de Docker 
    "database": "ecommerce",
    "user": "admin",
    "password": "admin123",
}

DB_CONNECTION_STRING_DOCKER = (
    f"postgresql://{DB_CONFIG_DOCKER['user']}:{DB_CONFIG_DOCKER['password']}"
    f"@{DB_CONFIG_DOCKER['host']}:{DB_CONFIG_DOCKER['port']}"
    f"/{DB_CONFIG_DOCKER['database']}"
)