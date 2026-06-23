-- ============================================================
-- Esquema de base de datos: ecommerce
-- Tablas para el pipeline ETL de Fake Store API
-- ============================================================

-- ─── Tabla: categorías ───
-- Normalizamos las categorías para evitar repetir texto
CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── Tabla: productos ───
CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    price           DECIMAL(10, 2) NOT NULL,
    description     TEXT,
    category_id     INTEGER REFERENCES categories(id),
    image_url       VARCHAR(500),
    rating_rate     DECIMAL(3, 2),
    rating_count    INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── Tabla: usuarios ───
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY,
    email       VARCHAR(255) NOT NULL UNIQUE,
    username    VARCHAR(100) NOT NULL,
    password    VARCHAR(100),  -- hash desde la API (no real)
    firstname   VARCHAR(100),
    lastname    VARCHAR(100),
    phone       VARCHAR(50),
    city        VARCHAR(100),
    street      VARCHAR(255),
    number      VARCHAR(20),
    zipcode     VARCHAR(20),
    lat         VARCHAR(20),
    long        VARCHAR(20),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── Tabla: carritos / pedidos ───
CREATE TABLE IF NOT EXISTS carts (
    id          INTEGER PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id),
    date        TIMESTAMP,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── Tabla: items de carrito (líneas de pedido) ───
CREATE TABLE IF NOT EXISTS cart_items (
    id          SERIAL PRIMARY KEY,
    cart_id     INTEGER REFERENCES carts(id),
    product_id  INTEGER REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    price_at_time DECIMAL(10, 2) NOT NULL  -- precio histórico
);

-- ─── Índices para consultas rápidas ───
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_carts_user ON carts(user_id);
CREATE INDEX IF NOT EXISTS idx_cart_items_cart ON cart_items(cart_id);