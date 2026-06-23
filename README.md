# 🛒 E-Commerce Data Pipeline

> Pipeline ETL end-to-end: extracción de API REST, transformación con Pandas, carga a PostgreSQL y orquestación con Apache Airflow en Docker. Incluye dashboard de visualización.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Airflow](https://img.shields.io/badge/Airflow-2.7+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Tabla de Contenidos

- [Arquitectura](#-arquitectura-del-proyecto)
- [Estructura](#-estructura-del-proyecto)
- [Prerrequisitos](#-prerrequisitos)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [Uso](#-uso)
- [Tecnologías](#-tecnologías-utilizadas)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)

---

## 🏗️ Arquitectura del Proyecto

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Fake Store │────▶│   Python    │────▶│  PostgreSQL │────▶│  Metabase   │
│    API      │     │  (Pandas)   │     │  (Raw+Mart) │     │ (Dashboard) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │Apache Airflow│
                    │ (Orquesta)   │
                    └──────────────┘
```

**Flujo de datos:**

1. **Extract** — Se consume la API pública [Fake Store API](https://fakestoreapi.com/) para obtener productos, usuarios y pedidos.
2. **Transform** — Se limpian y normalizan los datos con **Pandas** (tipos de datos, duplicados, nulos).
3. **Load** — Se cargan los datos limpios a **PostgreSQL** en tablas normalizadas.
4. **Orchestrate** — **Apache Airflow** ejecuta el pipeline de forma automatizada y programada.
5. **Visualize** — **Metabase** se conecta a PostgreSQL para generar dashboards interactivos.

---

## 🗂️ Estructura del Proyecto

```
ecommerce-data-pipeline/
├── dags/
│   └── ecommerce_pipeline.py          # DAG de Apache Airflow
├── scripts/
│   ├── __init__.py
│   ├── config.py                      # Configuraciones centralizadas
│   ├── extract.py                     # Extracción desde API REST
│   ├── transform.py                   # Limpieza y transformación
│   └── load.py                        # Carga a PostgreSQL
├── sql/
│   ├── schema.sql                     # Creación de tablas (DDL)
│   └── seed_data.sql                  # Datos de prueba
├── data/
│   ├── raw/                           # Datos crudos descargados
│   └── processed/                     # Datos limpios generados
├── tests/
│   ├── test_extract.py                # Tests unitarios de extracción
│   ├── test_transform.py              # Tests unitarios de transformación
│   └── test_load.py                   # Tests unitarios de carga
├── docs/
│   └── architecture.md                # Documentación técnica detallada
├── images/                            # Capturas de pantalla del dashboard
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias de Python
├── docker-compose.yml                 # Orquestación de servicios
└── .gitignore                         # Archivos ignorados por Git
```

| Carpeta | Propósito |
|---------|-----------|
| `dags/` | Definición de DAGs para Apache Airflow |
| `scripts/` | Módulos Python reutilizables del pipeline ETL |
| `sql/` | Scripts SQL para creación de esquemas y datos iniciales |
| `data/` | Almacenamiento local de datos crudos y procesados |
| `tests/` | Suite de tests unitarios con pytest |
| `docs/` | Documentación adicional de arquitectura y decisiones |

---

## ⚙️ Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

| Herramienta | Versión mínima | Enlace de descarga |
|-------------|----------------|--------------------|
| Docker Desktop | 4.0+ | [Descargar](https://www.docker.com/products/docker-desktop/) |
| Git | 2.30+ | [Descargar](https://git-scm.com/) |
| Python | 3.9+ | [Descargar](https://www.python.org/downloads/) |

> **Nota para Mac con Apple Silicon (M1/M2/M3):** Docker Desktop ya es compatible nativo. No se requieren pasos adicionales.

---

## 🚀 Instalación y Ejecución

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/Ivifer1/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### Paso 2 — Levantar los servicios con Docker Compose

```bash
docker-compose up -d
```

Este comando descarga las imágenes y crea los siguientes contenedores:

| Servicio | Contenedor | Puerto | Descripción |
|----------|------------|--------|-------------|
| PostgreSQL | `ecommerce_postgres` | `5432` | Base de datos principal |
| Airflow DB | `airflow_postgres` | — | Metadatos de Airflow |
| Airflow Init | `airflow_init` | — | Inicialización de Airflow |
| Airflow Webserver | `airflow_webserver` | `8080` | Interfaz web de Airflow |
| Airflow Scheduler | `airflow_scheduler` | — | Programador de tareas |
| Metabase | `ecommerce_metabase` | `3000` | Dashboard y visualización |

### Paso 3 — Verificar que los contenedores estén activos

```bash
docker ps
```

Deberías ver **5 contenedores** en estado `Up`.

Si alguno no levantó, revisa los logs:

```bash
docker-compose logs
```

### Paso 4 — Acceder a Apache Airflow

- **URL:** http://localhost:8080
- **Usuario:** `admin`
- **Contraseña:** `admin`

Una vez dentro:

1. Localiza el DAG llamado `ecommerce_pipeline`.
2. Actívalo con el switch a la izquierda.
3. Ejecútalo manualmente con el botón ▶️ (Trigger DAG).

### Paso 5 — Verificar los datos en PostgreSQL

```bash
docker exec -it ecommerce_postgres psql -U admin -d ecommerce -c "SELECT COUNT(*) FROM products;"
```

Si el pipeline funcionó correctamente, verás el conteo de registros cargados.

### Paso 6 — Configurar el Dashboard en Metabase

- **URL:** http://localhost:3000
- Completa el registro inicial (nombre, email, contraseña).
- Agrega una base de datos con estos datos:

| Campo | Valor |
|-------|-------|
| Tipo de base de datos | PostgreSQL |
| Host | `postgres` |
| Puerto | `5432` |
| Base de datos | `ecommerce` |
| Usuario | `admin` |
| Contraseña | `admin123` |

- Guarda y crea tus preguntas/visualizaciones.

---

## 📊 Uso

### Ejecutar el pipeline manualmente (sin Airflow)

Si deseas probar los scripts individualmente:

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar cada etapa
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

### Ejecutar tests

```bash
pytest tests/
```

### Detener todos los servicios

```bash
docker-compose down
```

Para eliminar también los volúmenes (borra los datos):

```bash
docker-compose down -v
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.9+ | Lógica del pipeline ETL |
| **Pandas** | 2.0+ | Transformación y limpieza de datos |
| **SQLAlchemy** | 2.0+ | ORM para conexión a PostgreSQL |
| **Psycopg2** | 2.9+ | Driver PostgreSQL para Python |
| **Requests** | 2.31+ | Consumo de API REST |
| **Apache Airflow** | 2.7+ | Orquestación y programación de tareas |
| **PostgreSQL** | 15+ | Base de datos relacional |
| **Docker** | 24+ | Contenerización de servicios |
| **Docker Compose** | 2.20+ | Orquestación multi-contenedor |
| **Metabase** | Latest | Visualización y dashboards |
| **Pytest** | 7.4+ | Tests unitarios |

---

## 🗺️ Roadmap

- [x] Estructura inicial del proyecto
- [x] Docker Compose con PostgreSQL, Airflow y Metabase
- [ ] Script de extracción (`extract.py`)
- [ ] Script de transformación (`transform.py`)
- [ ] Script de carga (`load.py`)
- [ ] Esquema SQL (`schema.sql`)
- [ ] DAG de Airflow (`ecommerce_pipeline.py`)
- [ ] Tests unitarios
- [ ] Dashboard en Metabase
- [ ] Documentación de arquitectura

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.

> Proyecto educativo desarrollado para portafolio de Data Engineering Junior.

---

## 👤 Autor

**Ivifer Pita** — [LinkedIn](https://www.linkedin.com/in/ivifer-pita-322527380/) — [GitHub](https://github.com/Ivifer1)

> ¿Preguntas o sugerencias? Abre un [Issue](https://github.com/Ivifer1/ecommerce-data-pipeline/issues).
