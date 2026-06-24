"""
load.py
Carga los datos limpios (CSV) en PostgreSQL.
Compatible con Python 3.9
"""

import pandas as pd
from sqlalchemy import create_engine, text
from typing import List

try:
    from config import DB_CONNECTION_STRING
except ImportError:
    from scripts.config import DB_CONNECTION_STRING


def get_engine():
    """Crea y retorna el motor de conexión a PostgreSQL."""
    return create_engine(DB_CONNECTION_STRING)


def load_csv_to_table(csv_filename: str, table_name: str, engine):
    """
    Lee un CSV y lo inserta en una tabla de PostgreSQL.
    """
    # Leer CSV
    df = pd.read_csv(f"data/processed/{csv_filename}")
    
    print(f"\n Cargando {table_name}...")
    print(f"   Registros a insertar: {len(df)}")
    
    # Insertar en PostgreSQL (reemplaza si ya existe)
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",  # Agrega datos sin borrar existentes
        index=False
    )
    
    print(f"    {table_name} cargado exitosamente")


def verify_table(table_name: str, engine):
    """Verifica cuántos registros hay en una tabla."""
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        print(f"    {table_name}: {count} registros")


def load_all():
    """
    Ejecuta la carga completa: inserta todos los CSV en PostgreSQL.
    """
    print("=" * 50)
    print("INICIANDO CARGA A POSTGRESQL")
    print("=" * 50)
    
    engine = get_engine()
    
    # Orden importante: tablas padre primero, luego hijas
    tables = [
        ("categories_clean.csv", "categories"),
        ("products_clean.csv", "products"),
        ("users_clean.csv", "users"),
        ("carts_clean.csv", "carts"),
        ("cart_items_clean.csv", "cart_items"),
    ]
    
    for csv_file, table_name in tables:
        load_csv_to_table(csv_file, table_name, engine)
    
    print("\n" + "=" * 50)
    print("VERIFICANDO DATOS CARGADOS")
    print("=" * 50)
    
    for _, table_name in tables:
        verify_table(table_name, engine)
    
    print("\n" + "=" * 50)
    print("CARGA COMPLETADA")
    print("=" * 50)


if __name__ == "__main__":
    load_all()