# Documentación de Arquitectura

## Decisiones Técnicas

### ¿Por qué PostgreSQL?
- Base de datos relacional robusta y gratuita
- Compatible con Metabase para visualización
- Estándar en la industria para Data Warehousing

### ¿Por qué Apache Airflow?
- Orquestación de pipelines con dependencias entre tareas
- Interfaz web para monitoreo y logs
- Programación automática (cron jobs)

### ¿Por qué Metabase?
- Open source y gratuito
- Conexión directa a PostgreSQL
- No requiere código para crear dashboards

### ¿Por qué Docker?
- Portabilidad: cualquiera puede levantar el proyecto
- Aislamiento: no contamina el sistema operativo
- Versionado: todos usan las mismas versiones de herramientas

## Flujo de Datos
API (Fake Store) → Python/Pandas → PostgreSQL → Metabase
↓
Apache Airflow


## Esquema de Base de Datos

| Tabla | Descripción | Relaciones |
|-------|-------------|------------|
| categories | Categorías de productos | Padre de products |
| products | Productos de la tienda | Hijo de categories |
| users | Usuarios registrados | Padre de carts |
| carts | Carritos de compra | Hijo de users |
| cart_items | Líneas de cada carrito | Hijo de carts y products |

## Consideraciones

- Los datos de la API son estáticos (20 productos, 10 usuarios)
- En producción, el DAG se ejecutaría diariamente para obtener datos nuevos
- Los precios históricos se guardan en cart_items para análisis temporal