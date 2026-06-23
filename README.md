# 🛒 E-Commerce Data Pipeline

&gt; Pipeline ETL end-to-end: extracción de API REST, transformación con Pandas, carga a PostgreSQL y orquestación con Apache Airflow en Docker. Incluye dashboard de visualización.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Airflow](https://img.shields.io/badge/Airflow-2.7+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)

---

## 📋 Arquitectura del Proyecto

┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Fake Store │────▶│   Python    │────▶│  PostgreSQL │────▶│  Metabase   │
│    API      │     │  (Pandas)   │     │  (Raw+Mart) │     │ (Dashboard) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
│
┌──────┴──────┐
│Apache Airflow│
│ (Orquesta)   │
└──────────────┘


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
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- [Git](https://git-scm.com/) instalado
- Python 3.9+ (solo para desarrollo local)

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline

Paso 2: Levantar los servicios con Docker

bash
docker-compose up -d

Esto creará y ejecutará:
PostgreSQL (base de datos)
Apache Airflow (webserver + scheduler)
Metabase (dashboard)

Paso 3: Verificar que los contenedores estén corriendo
bash
docker ps

Deberías ver 5 contenedores activos: ecommerce_postgres, airflow_postgres, airflow_webserver, airflow_scheduler y ecommerce_metabase.

Paso 4: Acceder a Apache Airflow
Abre tu navegador: http://localhost:8080
Usuario: admin
Contraseña: admin

Paso 5: Activar el DAG
En la interfaz de Airflow, busca el DAG llamado ecommerce_pipeline
Actívalo con el switch a la izquierda
Ejecútalo manualmente con el botón ▶️ (Play)

Paso 6: Verificar los datos en PostgreSQL
bash
docker exec -it ecommerce_postgres psql -U admin -d ecommerce -c "SELECT * FROM products LIMIT 5;"

Paso 7: Acceder al Dashboard (Metabase)
Abre tu navegador: http://localhost:3000
Completa el registro inicial
Conecta la base de datos PostgreSQL:
Host: postgres
Puerto: 5432
Base de datos: ecommerce
Usuario: admin
Contraseña: admin123