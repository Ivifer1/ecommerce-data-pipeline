# 🛒 E-Commerce Data Pipeline

&gt; Pipeline ETL end-to-end: extracción de API REST, transformación con Pandas, carga a PostgreSQL y orquestación con Apache Airflow en Docker. Incluye dashboard de visualización.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Airflow](https://img.shields.io/badge/Airflow-2.7+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)

---

## 📋 Arquitectura del Proyecto
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Fake      │────▶│   Python    │────▶│  PostgreSQL │────▶│   Metabase  │
│   Store API │     │   (Pandas)  │     │   (Raw+Mart)│     │  (Dashboard) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
│
┌──────┴──────┐
│ Apache Airflow│
│  (Orquesta)   │
└───────────────┘


---

## Estructura del Proyecto

| Carpeta | Descripción |
|---------|-------------|
| `dags/` | DAGs de Apache Airflow |
| `scripts/` | Módulos Python (extract, transform, load) |
| `sql/` | Esquemas y scripts SQL |
| `data/` | Datos crudos y procesados |
| `tests/` | Tests unitarios |
| `docs/` | Documentación de arquitectura |

---

## Cómo ejecutar el proyecto

### Prerrequisitos
- Docker Desktop
- Python 3.9+
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline