"""
app.py
Dashboard interactivo con Streamlit para el pipeline ETL de e-commerce.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from scripts.config import DB_CONNECTION_STRING


# ─── Configuración de la página ───
st.set_page_config(
    page_title="E-Commerce Data Pipeline",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Data Pipeline Dashboard")
st.markdown("---")


# ─── Conexión a la base de datos ───
@st.cache_data(ttl=60)
def load_data():
    """Carga datos desde PostgreSQL."""
    engine = create_engine(DB_CONNECTION_STRING)
    
    products = pd.read_sql("SELECT * FROM products", engine)
    categories = pd.read_sql("SELECT * FROM categories", engine)
    users = pd.read_sql("SELECT * FROM users", engine)
    carts = pd.read_sql("SELECT * FROM carts", engine)
    cart_items = pd.read_sql("SELECT * FROM cart_items", engine)
    
    return products, categories, users, carts, cart_items


# ─── Cargar datos ───
try:
    products, categories, users, carts, cart_items = load_data()
except Exception as e:
    st.error(f"❌ Error conectando a la base de datos: {e}")
    st.info("Asegúrate de que PostgreSQL esté corriendo en Docker.")
    st.stop()


# ─── Métricas principales ───
st.subheader("📊 Métricas Clave")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Productos", len(products))
with col2:
    st.metric("Categorías", len(categories))
with col3:
    st.metric("Usuarios", len(users))
with col4:
    st.metric("Carritos", len(carts))
with col5:
    st.metric("Items", len(cart_items))

st.markdown("---")


# ─── Gráfico 1: Productos por categoría ───
st.subheader("📦 Productos por Categoría")

# Merge para obtener nombres de categorías
products_with_cat = products.merge(categories, left_on="category_id", right_on="id", suffixes=("_product", "_category"))

fig1, ax1 = plt.subplots(figsize=(10, 5))
products_with_cat["name"].value_counts().plot(kind="bar", ax=ax1, color="#4CAF50")
ax1.set_xlabel("Categoría")
ax1.set_ylabel("Cantidad de Productos")
ax1.set_title("Productos por Categoría")
plt.xticks(rotation=45)
st.pyplot(fig1)


# ─── Gráfico 2: Precio promedio por categoría ───
st.subheader("💰 Precio Promedio por Categoría")

avg_price = products_with_cat.groupby("name")["price"].mean().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10, 5))
avg_price.plot(kind="bar", ax=ax2, color="#2196F3")
ax2.set_xlabel("Categoría")
ax2.set_ylabel("Precio Promedio ($)")
ax2.set_title("Precio Promedio por Categoría")
plt.xticks(rotation=45)
st.pyplot(fig2)


# ─── Tabla de productos ───
st.subheader("📋 Tabla de Productos")

# Filtro por categoría
selected_category = st.selectbox(
    "Filtrar por categoría:",
    options=["Todas"] + list(categories["name"])
)

if selected_category != "Todas":
    filtered = products_with_cat[products_with_cat["name"] == selected_category]
else:
    filtered = products_with_cat

st.dataframe(
    filtered[["id_product", "title", "price", "name", "rating_rate", "rating_count"]],
    use_container_width=True
)


# ─── Footer ───
st.markdown("---")
st.caption("🔧 Pipeline ETL | Python · PostgreSQL · Airflow · Docker · Streamlit")