"""
extract.py
Descarga datos de la Fake Store API y los guarda como JSON crudo.
Compatible con Python 3.9
"""

import json
import requests
from pathlib import Path
from typing import List, Dict, Union

from config import API_BASE_URL, API_ENDPOINTS, DATA_RAW_DIR


def fetch_data(endpoint: str) -> Union[List, Dict]:
    """
    Realiza una petición GET a la API y devuelve los datos en formato JSON.
    
    Args:
        endpoint: Ruta del endpoint (ej: '/products')
    
    Returns:
        Datos parseados de la API (lista o diccionario)
    
    Raises:
        requests.RequestException: Si falla la conexión o el status no es 200
    """
    url = f"{API_BASE_URL}{endpoint}"
    print(f"Descargando: {url}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    print(f"Descargados {len(data) if isinstance(data, list) else 1} registros")
    
    return data


def save_raw_data(data: Union[List, Dict], filename: str) -> Path:
    """
    Guarda los datos crudos en un archivo JSON dentro de data/raw/.
    
    Args:
        data: Datos a guardar
        filename: Nombre del archivo (ej: 'products.json')
    
    Returns:
        Ruta completa donde se guardó el archivo
    """
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    filepath = DATA_RAW_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Guardado en: {filepath}")
    return filepath


def extract_all():
    """
    Ejecuta la extracción completa: descarga todos los endpoints
    y guarda los archivos JSON.
    """
    print("=" * 50)
    print("INICIANDO EXTRACCIÓN DE DATOS")
    print("=" * 50)
    
    for name, endpoint in API_ENDPOINTS.items():
        print(f"\n--- Extrayendo: {name} ---")
        try:
            data = fetch_data(endpoint)
            filename = f"{name}.json"
            save_raw_data(data, filename)
        except requests.RequestException as e:
            print(f"Error extrayendo {name}: {e}")
            raise
    
    print("\n" + "=" * 50)
    print("EXTRACCIÓN COMPLETADA")
    print("=" * 50)


if __name__ == "__main__":
    extract_all()