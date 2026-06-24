"""
transform.py
Limpia y normaliza los datos crudos de la Fake Store API
para que encajen en el esquema de 5 tablas de PostgreSQL.
Compatible con Python 3.9
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict

try:
    from config import DATA_RAW_DIR, DATA_PROCESSED_DIR
except ImportError:
    from scripts.config import DATA_RAW_DIR, DATA_PROCESSED_DIR


def load_raw(filename: str) -> List[Dict]:
    """Carga un archivo JSON crudo desde data/raw/."""
    filepath = DATA_RAW_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_categories(products_raw: List[Dict]) -> pd.DataFrame:
    """
    Extrae categorías únicas de los productos y les asigna un ID numérico.
    """
    categories = sorted({p["category"] for p in products_raw})
    
    df = pd.DataFrame({
        "id": range(1, len(categories) + 1),
        "name": categories
    })
    
    print(f"Categorías únicas encontradas: {len(df)}")
    return df


def transform_products(products_raw: List[Dict], categories_df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia productos y mapea category (string) → category_id (int).
    """
    cat_map = dict(zip(categories_df["name"], categories_df["id"]))
    
    records = []
    for p in products_raw:
        records.append({
            "id": p["id"],
            "title": p["title"],
            "price": float(p["price"]),
            "description": p.get("description", ""),
            "category_id": cat_map.get(p["category"]),
            "image_url": p.get("image", ""),
            "rating_rate": float(p["rating"]["rate"]) if "rating" in p else None,
            "rating_count": int(p["rating"]["count"]) if "rating" in p else None,
        })
    
    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["id"])
    
    print(f"Productos procesados: {len(df)}")
    return df


def transform_users(users_raw: List[Dict]) -> pd.DataFrame:
    """
    Aplana la estructura anidada de address (city, street, etc.)
    """
    records = []
    for u in users_raw:
        address = u.get("address", {})
        geo = address.get("geolocation", {})
        
        records.append({
            "id": u["id"],
            "email": u["email"],
            "username": u["username"],
            "password": u.get("password", ""),
            "firstname": u.get("name", {}).get("firstname", ""),
            "lastname": u.get("name", {}).get("lastname", ""),
            "phone": u.get("phone", ""),
            "city": address.get("city", ""),
            "street": address.get("street", ""),
            "number": str(address.get("number", "")),
            "zipcode": address.get("zipcode", ""),
            "lat": geo.get("lat", ""),
            "long": geo.get("long", ""),
        })
    
    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["id"])
    
    print(f"Usuarios procesados: {len(df)}")
    return df


def transform_carts(carts_raw: List[Dict]) -> pd.DataFrame:
    """
    Extrae los carritos (pedidos) principales.
    """
    records = []
    for c in carts_raw:
        records.append({
            "id": c["id"],
            "user_id": c["userId"],
            "date": c.get("date", None),
        })
    
    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["id"])
    
    print(f"Carritos procesados: {len(df)}")
    return df


def transform_cart_items(carts_raw: List[Dict]) -> pd.DataFrame:
    """
    Extrae las líneas de cada carrito (qué producto, cuántos).
    """
    records = []
    for c in carts_raw:
        for item in c.get("products", []):
            records.append({
                "cart_id": c["id"],
                "product_id": item["productId"],
                "quantity": item["quantity"],
                "price_at_time": 0.0,
            })
    
    df = pd.DataFrame(records)
    df.insert(0, "id", range(1, len(df) + 1))
    
    print(f"Items de carrito procesados: {len(df)}")
    return df


def save_processed(df: pd.DataFrame, filename: str):
    """Guarda un DataFrame limpio como CSV en data/processed/."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_PROCESSED_DIR / filename
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"Guardado: {filepath}")


def transform_all():
    """
    Ejecuta la transformación completa: carga crudo → limpia → guarda CSV.
    """
    print("=" * 50)
    print("INICIANDO TRANSFORMACIÓN DE DATOS")
    print("=" * 50)
    
    print("\nCargando datos crudos...")
    products_raw = load_raw("products.json")
    users_raw = load_raw("users.json")
    carts_raw = load_raw("carts.json")
    
    print("\n--- Transformando categorías ---")
    categories_df = transform_categories(products_raw)
    
    print("\n--- Transformando productos ---")
    products_df = transform_products(products_raw, categories_df)
    
    print("\n--- Transformando usuarios ---")
    users_df = transform_users(users_raw)
    
    print("\n--- Transformando carritos ---")
    carts_df = transform_carts(carts_raw)
    
    print("\n--- Transformando items de carrito ---")
    cart_items_df = transform_cart_items(carts_raw)
    
    print("\n" + "=" * 50)
    print("GUARDANDO DATOS LIMPIOS")
    print("=" * 50)
    
    save_processed(categories_df, "categories_clean.csv")
    save_processed(products_df, "products_clean.csv")
    save_processed(users_df, "users_clean.csv")
    save_processed(carts_df, "carts_clean.csv")
    save_processed(cart_items_df, "cart_items_clean.csv")
    
    print("\n" + "=" * 50)
    print("TRANSFORMACIÓN COMPLETADA")
    print("=" * 50)
    
    return {
        "categories": categories_df,
        "products": products_df,
        "users": users_df,
        "carts": carts_df,
        "cart_items": cart_items_df,
    }


if __name__ == "__main__":
    transform_all()